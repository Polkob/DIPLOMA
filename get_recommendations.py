import requests

# Create a session to maintain cookies
session = requests.Session()

# First login
login_response = session.post(
    'http://localhost:5000/api/auth/login',
    json={
        'username': 'test_user',
        'password': 'test_password_hash'
    }
)

print('Login response status:', login_response.status_code)
print('Login response body:', login_response.text)

# Build similarity matrices
response = session.post(
    'http://localhost:5000/api/recommendations/build-matrices'
)

print('\nBuild matrices response status:', response.status_code)
print('Build matrices response body:', response.text)

# Get recommendations for movie "Твоё имя" (ID: 3)
response = session.get(
    'http://localhost:5000/api/recommendations/recommendations',
    params={'movie_id': 3}
)

print('\nGet recommendations response status:', response.status_code)
print('Get recommendations response body:', response.text)

# Get similar movies for "Твоё имя"
response = session.get(
    'http://localhost:5000/api/recommendations/similar-movies/3'
)

print('\nGet similar movies response status:', response.status_code)
print('Get similar movies response body:', response.text) 