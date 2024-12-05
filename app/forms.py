from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class RegistrationForm(FlaskForm):
    """
    A form for user registration.

    Attributes:
        username (StringField): The desired username.
        password (PasswordField): The user's password.
        confirm_password (PasswordField): Confirmation of the user's password.
        submit (SubmitField): The submit button for the form.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """
    A form for user login.

    Attributes:
        username (StringField): The user's username.
        password (PasswordField): The user's password.
        submit (SubmitField): The submit button for the form.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TransactionForm(FlaskForm):
    """
    A form for adding or editing financial transactions.

    Attributes:
        description (StringField): The description of the transaction.
        amount (FloatField): The monetary amount of the transaction.
        type (SelectField): The type of transaction ('income' or 'expense').
        submit (SubmitField): The submit button for the form.
    """
    description = StringField('Description', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[DataRequired()])
    submit = SubmitField('Add Transaction')

class FilterForm(FlaskForm):
    """
    A form for filtering transactions based on date range and transaction type.

    Attributes:
        start_date (DateField): The starting date of the filter range (optional).
        end_date (DateField): The ending date of the filter range (optional).
        transaction_type (SelectField): The type of transaction to filter ('income', 'expense', or 'all').
        submit (SubmitField): The submit button for the form.
    """
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    transaction_type = SelectField('Type', choices=[('', 'All'), ('income', 'Income'), ('expense', 'Expense')], validators=[Optional()])
    submit = SubmitField('Filter')