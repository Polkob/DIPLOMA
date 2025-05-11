import httpx
import pandas as pd
import time
import os
import asyncio
from tqdm import tqdm
import json
from datetime import datetime
import random
import signal
import sys

class TMDBDownloader:
    def __init__(self, api_key):
        # Убираем кавычки из API ключа, если они есть
        self.api_key = api_key.strip('"\'')
        self.base_url = "https://api.themoviedb.org/3"
        self.language = "ru-RU"
        self.movies_data = []
        self.error_log = []
        self.max_retries = 5
        self.retry_delay = 5
        self.current_page = 1
        
        # Создаем абсолютные пути для файлов
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.progress_file = os.path.join(self.script_dir, 'download_progress.json')
        self.error_log_file = os.path.join(self.script_dir, 'error_log.json')
        self.data_dir = os.path.join(self.script_dir, 'data')
        
        self.last_save_time = time.time()
        self.save_interval = 30  # сохранять каждые 30 секунд
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json'
        }
        
        # Регистрируем обработчик сигналов
        signal.signal(signal.SIGINT, self.handle_interrupt)
        signal.signal(signal.SIGTERM, self.handle_interrupt)
    
    def handle_interrupt(self, signum, frame):
        """Обработчик прерывания"""
        print("\nПолучен сигнал прерывания. Сохраняем прогресс...")
        self.save_progress()
        print("Прогресс сохранен. Завершение работы...")
        sys.exit(0)
    
    def save_progress(self):
        """Сохранение прогресса"""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'last_page': self.current_page,
                    'total_movies': len(self.movies_data),
                    'movies_data': self.movies_data,
                    'timestamp': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            print(f"\nПрогресс сохранен: {len(self.movies_data)} фильмов")
        except Exception as e:
            print(f"Ошибка при сохранении прогресса: {str(e)}")
    
    def log_error(self, error_type, details):
        """Логирование ошибок"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'details': details
        }
        self.error_log.append(error_entry)
        
        try:
            with open(self.error_log_file, 'w', encoding='utf-8') as f:
                json.dump(self.error_log, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении лога ошибок: {str(e)}")
    
    async def get_popular_movies(self, client, page=1):
        """Получение списка популярных фильмов"""
        try:
            response = await client.get(
                f"{self.base_url}/movie/popular",
                params={
                    'api_key': self.api_key,
                    'language': self.language,
                    'page': page
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log_error('POPULAR_MOVIES_ERROR', {
                'page': page,
                'error': str(e)
            })
            raise

    async def get_movie_details(self, client, movie_id):
        """Получение детальной информации о фильме"""
        try:
            response = await client.get(
                f"{self.base_url}/movie/{movie_id}",
                params={
                    'api_key': self.api_key,
                    'language': self.language,
                    'append_to_response': 'credits,release_dates,external_ids,keywords,videos,images'
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log_error('MOVIE_DETAILS_ERROR', {
                'movie_id': movie_id,
                'error': str(e)
            })
            raise

    async def process_movie_batch(self, client, movie_ids):
        """Обработка пакета фильмов"""
        tasks = []
        for movie_id in movie_ids:
            tasks.append(self.get_movie_details(client, movie_id))
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def download_data(self, num_movies=5000):
        """Скачивание данных о фильмах"""
        print("Начинаем скачивание данных...")
        
        # Создаем директорию для данных, если её нет
        os.makedirs(self.data_dir, exist_ok=True)
        
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                    self.movies_data = progress.get('movies_data', [])
                    self.current_page = progress.get('last_page', 1)
                    total_movies = len(self.movies_data)
                    print(f"Продолжаем с сохраненного прогресса: {total_movies} фильмов, страница {self.current_page}")
            except Exception as e:
                print(f"Ошибка при загрузке прогресса: {str(e)}")
                self.current_page = 1
                total_movies = 0
        else:
            self.current_page = 1
            total_movies = 0
        
        # Увеличиваем лимиты для более быстрой загрузки
        async with httpx.AsyncClient(
            timeout=60.0,
            headers=self.headers,
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=40)
        ) as client:
            with tqdm(total=num_movies, initial=total_movies, desc="Скачивание фильмов") as pbar:
                while total_movies < num_movies:
                    try:
                        print(f"\nПолучение страницы {self.current_page}...")
                        popular_movies = await self.get_popular_movies(client, self.current_page)
                        
                        if not popular_movies or not popular_movies.get('results'):
                            print(f"Нет результатов на странице {self.current_page}")
                            break
                        
                        # Собираем ID фильмов для пакетной обработки
                        movie_ids = [movie['id'] for movie in popular_movies['results']]
                        
                        # Обрабатываем фильмы пакетами по 10
                        batch_size = 10
                        for i in range(0, len(movie_ids), batch_size):
                            batch_ids = movie_ids[i:i + batch_size]
                            results = await self.process_movie_batch(client, batch_ids)
                            
                            for movie_details in results:
                                if isinstance(movie_details, Exception):
                                    continue
                                
                                if not movie_details:
                                    continue
                                
                                # Сохраняем полные данные фильма
                                self.movies_data.append(movie_details)
                                
                                total_movies += 1
                                pbar.update(1)
                                
                                if total_movies >= num_movies:
                                    break
                            
                            # Сохраняем прогресс после каждого пакета
                            self.save_progress()
                            
                            # Минимальная задержка между пакетами
                            await asyncio.sleep(0.1)
                            
                            if total_movies >= num_movies:
                                break
                        
                        self.current_page += 1
                        
                    except Exception as e:
                        print(f"\nОшибка при получении страницы {self.current_page}: {str(e)}")
                        self.log_error('PAGE_ERROR', {
                            'page': self.current_page,
                            'error': str(e)
                        })
                        await asyncio.sleep(self.retry_delay)
                        continue
            
            if not self.movies_data:
                print("Не удалось скачать данные о фильмах")
                return
                
            print("\nСохранение данных...")
            # Сохраняем полные данные в JSON
            json_file = os.path.join(self.data_dir, 'movies_data.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.movies_data, f, ensure_ascii=False, indent=2)
            
            print("Данные успешно сохранены!")
            print(f"Скачано {len(self.movies_data)} фильмов")
            
            if os.path.exists(self.progress_file):
                os.remove(self.progress_file)

async def main():
    print("Для работы скрипта необходим API ключ от TMDB.")
    print("Получить ключ можно на сайте: https://www.themoviedb.org/settings/api")
    print("После регистрации перейдите в настройки профиля -> API и запросите ключ")
    print("\nВведите ваш API ключ от TMDB:")
    api_key = input().strip()
    
    if not api_key:
        print("API ключ не может быть пустым")
        return
    
    downloader = TMDBDownloader(api_key)
    await downloader.download_data()

if __name__ == "__main__":
    asyncio.run(main())