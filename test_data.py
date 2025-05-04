from app import create_app, db
from app.models import User, Movie, Genre, Actor, Director, Country
from datetime import datetime

def add_test_data():
    app = create_app()
    
    with app.app_context():
        try:
            # Добавляем тестового пользователя
            test_user = User(
                username="test_user",
                password_hash="test_password_hash",
                email="test@example.com"
            )
            db.session.add(test_user)
            
            # Добавляем жанры
            action = Genre(name="Action")
            comedy = Genre(name="Comedy")
            drama = Genre(name="Drama")
            db.session.add_all([action, comedy, drama])
            
            # Добавляем актеров
            actor1 = Actor(name="Tom Hanks")
            actor2 = Actor(name="Morgan Freeman")
            db.session.add_all([actor1, actor2])
            
            # Добавляем режиссеров
            director1 = Director(name="Christopher Nolan")
            director2 = Director(name="Steven Spielberg")
            db.session.add_all([director1, director2])
            
            # Добавляем страны
            usa = Country(name="USA")
            uk = Country(name="UK")
            db.session.add_all([usa, uk])
            
            # Добавляем тестовый фильм
            test_movie = Movie(
                tmdb_id=123,
                title="Test Movie",
                overview="This is a test movie description",
                poster_url="https://example.com/poster.jpg",
                release_date=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
                rating=8.5
            )
            
            # Связываем фильм с жанрами, актерами, режиссерами и странами
            test_movie.genres.extend([action, drama])
            test_movie.actors.extend([actor1, actor2])
            test_movie.directors.append(director1)
            test_movie.countries.append(usa)
            
            db.session.add(test_movie)
            
            # Сохраняем все изменения
            db.session.commit()
            print("Test data added successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    add_test_data() 