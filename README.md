# BudgetTracker
A web-based Budget Tracker built with Python (Flask), SQLite, and Bootstrap. This app allows users to securely track income and expenses, generate financial reports, and manage transactions (add/remove) with a modern UI. Features include user authentication, transaction categorization, and balance summaries.

## Project Overview
The **Budget Tracker** is a Python-based web application designed to help users manage their income and expenses effectively. It allows secure user authentication, transaction management, and financial report generation.

## Technologies Used
- **Python 3.9.6**
- **Flask** (Backend Web Framework)
- **Flask-SQLAlchemy** (ORM for SQLite)
- **Flask-WTF** (Form Handling)
- **SQLite** (Database)
- **Bootstrap** (Frontend Styling)

## Installation and Setup
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd BudgetTracker
   ```
2. **Set Up Virtual environment**:
    - Create the virtual environment:
    ```bash
    python -m venv venv
    ```
    - Activate the virtual environment
      - **Windows:** ```venv\Scripts\activate````
      - **macOS/Linux:** ```source venv\Scripts\activate````
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ````
4. **Run the Application**:
    - Start the Flask development server:
    ```bash
    python main.py
    ```
    - Open your browser and navigate to ```http://127.0.0.1:5000````

## Usage
- Features:
  - User registration and login.
  - Add, View, and remove transactions.
  - View financial reports.

## Future Improvements
- Deployment to a cloud platform.
- Advanced analytics for transactions.

## License
This project is licensed under the MIT license.