from flask import render_template, redirect, url_for, flash, session
from app import app, db
from app.models import User, Transaction
from app.forms import RegistrationForm, LoginForm, TransactionForm

# @app.route('/')
# def home():
#     return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None) # Remove the user_id from the session
    flash('Logged out successfully!', 'success') # Show a success message
    return redirect(url_for('login')) # Redirect to the login page

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get all transactions for the logged-in user
    transactions = Transaction.query.filter_by(user_id=session['user_id']).all()

    # Calculate financial summary
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expenses

    # Get the 5 most recent transactions
    recent_transactions = Transaction.query.filter_by(user_id=session['user_id']).order_by(Transaction.date.desc()).limit(5).all()

    return render_template('dashboard.html', total_income=total_income, total_expenses=total_expenses, balance=balance, recent_transactions=recent_transactions)

# Route to check the user is logged in
@app.route('/check_session')
def check_session():
    if 'user_id' in session:
        return f"Logged in as user {session['user_id']}"
    return "No user logged in"

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            description=form.description.data,
            amount=form.amount.data,
            type=form.type.data,
            user_id=session['user_id']
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_transaction.html', form=form)

@app.route('/transactions')
def transactions():
    transactions = Transaction.query.filter_by(user_id=session['user_id']).all()
    return render_template('transactions.html', transactions=transactions)