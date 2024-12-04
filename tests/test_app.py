import pytest
from app import app, db
from app.models import User, Transaction

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword',
        'confirm_password': 'testpassword'
    }, follow_redirects=True)
    assert b'Registration successful' in response.data

def test_login(client):
    user = User(username='testuser')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert b'Login successful!' in response.data
