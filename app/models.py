from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The user's username.
        password (str): The hashed password for the user.
        transactions (Relationship): The list of transactions associated with the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        """
        Hashes the user's password and sets it.

        Args:
            password (str): The plaintext password.
        """
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """
        Checks if the given password matches the stored hashed password.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)
    
class Transaction(db.Model):
    """
    Represents a financial transaction.

    Attributes:
        id (int): The unique identifier for the transaction.
        description (str): The description of the transaction.
        amount (float): The monetary amount of the transaction.
        type (str): The type of transaction ('income' or 'expense').
        date (datetime): The date the transaction was created.
        user_id (int): The ID of the user who owns the transaction.
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'income' or 'expense'
    # date = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('transactions', lazy=True))