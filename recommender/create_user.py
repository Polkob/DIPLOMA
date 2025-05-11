from app import create_app, db
from app.models import User
import argparse

def create_user(username, password, email=None):
    """Создает нового пользователя в базе данных"""
    app = create_app()
    
    with app.app_context():
        try:
            # Проверяем, существует ли пользователь с таким username
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print(f"Пользователь с именем {username} уже существует")
                return
            
            # Создаем нового пользователя
            user = User(username=username, email=email)
            user.set_password(password)
            
            # Добавляем пользователя в базу данных
            db.session.add(user)
            db.session.commit()
            
            print(f"Пользователь {username} успешно создан")
            
        except Exception as e:
            db.session.rollback()
            print(f"Произошла ошибка: {str(e)}")
            raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Создание нового пользователя')
    parser.add_argument('--username', required=True, help='Имя пользователя')
    parser.add_argument('--password', required=True, help='Пароль пользователя')
    parser.add_argument('--email', help='Email пользователя (необязательно)')
    
    args = parser.parse_args()
    
    create_user(args.username, args.password, args.email) 