from flask import Flask
from app.models import db

app = Flask(__name__)
app.secret_key = '1010dba9d636960e7f19d92abab8f6c9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Import routes to register them with the app
from app import routes