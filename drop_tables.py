from app import create_app, db

app = create_app()

with app.app_context():
    # Удаляем все таблицы
    db.drop_all()
    # Создаем таблицы заново
    db.create_all()
    print("All tables have been dropped and recreated.") 