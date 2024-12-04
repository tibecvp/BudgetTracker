import pytest
from app import app, db
from app.models import User, Transaction

@pytest.fixture
def client():
    """
    Sets up a test client with an in-memory SQLite database.

    Yields:
        FlaskClient: The test client for making requests.
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    """
    Tests user registration functionality.
    """
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword',
        'confirm_password': 'testpassword'
    }, follow_redirects=True)
    assert b'Registration successful' in response.data

def test_add_transaction(client):
    """
    Tests adding a transaction functionality.
    """
    user = User(username='testuser')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    with client.session_transaction() as session:
        session['user_id'] = user.id

    response = client.post('/add_transaction', data={
        'description': 'Test Income',
        'amount': 100.0,
        'type': 'income'
    }, follow_redirects=True)
    assert b'Transaction added successfully!' in response.data
