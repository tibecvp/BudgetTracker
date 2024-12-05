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
    Tests the user registration functionality.
    """
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword',
        'confirm_password': 'testpassword'
    }, follow_redirects=True)
    assert b'Registration successful' in response.data
    assert User.query.filter_by(username='testuser').first() is not None

def test_login(client):
    """
    Tests the user login functionality.
    """
    user = User(username='testuser')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert b'Login successful!' in response.data

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
    transaction = Transaction.query.filter_by(description='Test Income').first()
    assert transaction is not None

def test_delete_transaction(client):
    """
    Tests deleting a transaction functionality.
    """
    user = User(username='testuser')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    transaction = Transaction(description='Test Expense', amount=50.0, type='expense', user_id=user.id)
    db.session.add(transaction)
    db.session.commit()

    with client.session_transaction() as session:
        session['user_id'] = user.id

    response = client.post(f'/delete_transaction/{transaction.id}', follow_redirects=True)
    assert b'Transaction deleted successfully!' in response.data
    assert Transaction.query.filter_by(id=transaction.id).first() is None

def test_edit_transaction(client):
    """
    Tests editing a transaction functionality.
    """
    user = User(username='testuser')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    transaction = Transaction(description='Test Expense', amount=50.0, type='expense', user_id=user.id)
    db.session.add(transaction)
    db.session.commit()

    with client.session_transaction() as session:
        session['user_id'] = user.id

    response = client.post(f'/edit_transaction/{transaction.id}', data={
        'description': 'Updated Expense',
        'amount': 75.0,
        'type': 'expense'
    }, follow_redirects=True)
    assert b'Transaction updated successfully!' in response.data
    updated_transaction = Transaction.query.get(transaction.id)
    assert updated_transaction.description == 'Updated Expense'
    assert updated_transaction.amount == 75.0

def test_report_generation(client):
    """
    Tests the report page generation.
    """
    user = User(username='testuser')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    transaction1 = Transaction(description='Income', amount=200.0, type='income', user_id=user.id)
    transaction2 = Transaction(description='Expense', amount=100.0, type='expense', user_id=user.id)
    db.session.add_all([transaction1, transaction2])
    db.session.commit()

    with client.session_transaction() as session:
        session['user_id'] = user.id

    response = client.get('/report')
    assert response.status_code == 200
    assert b'Financial Report' in response.data
    assert b'Income' in response.data
    assert b'Expense' in response.data
