from app import create_app, db
from app.models import User, Favorite, Movie
from datetime import datetime

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='test_user').first()
    if user:
        # Добавим первые 3 фильма в избранное
        movies = Movie.query.limit(3).all()
        for movie in movies:
            favorite = Favorite(
                user_id=user.id,
                movie_id=movie.id,
                added_at=datetime.now()
            )
            db.session.add(favorite)
        
        db.session.commit()
        print("Added movies to favorites successfully")
    else:
        print("User not found") 