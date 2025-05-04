import unittest
from app import create_app, db
from app.models import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        response = self.client.post('/users', json={
            'username': 'testuser',
            'password_hash': 'hashedpassword',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('user', response.json)

    def test_get_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main
