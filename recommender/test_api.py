import httpx
import random
import json
import asyncio

async def test_api_connection():
    api_key = "54a2541709252b5e3de68b7642666940"
    base_url = "https://api.themoviedb.org/3"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
    }
    
    # Создаем клиент с таймаутом и лимитами
    async with httpx.AsyncClient(
        timeout=30.0,
        headers=headers,
        limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
    ) as client:
        print("Тест: Получение популярных фильмов")
        try:
            # Используем случайную страницу
            random_page = random.randint(1, 50)
            
            response = await client.get(
                f"{base_url}/movie/popular",
                params={
                    'api_key': api_key,
                    'language': 'ru-RU',
                    'page': random_page
                }
            )
            response.raise_for_status()
            
            # Получаем базовый список фильмов
            basic_movies = response.json().get('results', [])[:10]
            print(f"✅ Получено {len(basic_movies)} базовых фильмов")
            
            # Получаем детальную информацию о каждом фильме
            detailed_movies = []
            for movie in basic_movies:
                try:
                    movie_id = movie['id']
                    detailed_response = await client.get(
                        f"{base_url}/movie/{movie_id}",
                        params={
                            'api_key': api_key,
                            'language': 'ru-RU',
                            'append_to_response': 'credits'
                        }
                    )
                    detailed_response.raise_for_status()
                    detailed_movie = detailed_response.json()
                    detailed_movies.append(detailed_movie)
                    print(f"✅ Получены детали фильма: {detailed_movie.get('title', 'Нет названия')}")
                except Exception as e:
                    print(f"❌ Ошибка при получении деталей фильма {movie_id}: {str(e)}")
                    continue
            
            # Выводим результаты
            print("\nПолученные фильмы:")
            for movie in detailed_movies:
                print(f"- {movie.get('title')} ({movie.get('release_date', 'Нет даты')})")
                print(f"  Описание: {movie.get('overview', 'Нет описания')[:100]}...")
                print()
            
            # Сохраняем результаты в файл
            with open('movies_test.json', 'w', encoding='utf-8') as f:
                json.dump(detailed_movies, f, ensure_ascii=False, indent=2)
            print("\nРезультаты сохранены в файл movies_test.json")
                
        except Exception as e:
            print(f"❌ Ошибка при получении фильмов: {str(e)}")

def main():
    print("Начинаем тестирование API TMDB...\n")
    asyncio.run(test_api_connection())

if __name__ == "__main__":
    main() 