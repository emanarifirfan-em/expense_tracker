"""
app.py — Flask application ka main file hai.
saare routes yahan hain.
Yeh file:
1. Browser se requests leti hai
2. database.py ke functions call karti hai
3. HTML templates render karti hai
4. Sessions handle karti hai (login state)
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import *
from functools import wraps



# APP SETUP
app = Flask(__name__)

app.secret_key = '6dc44748992b7af35c9632595fd3d53cd35185fa6d2e667cc00a1e520a0b92ce'  #key to ensure secure login state

# HELPER — Login Required Decorator
def login_required(f):
    """
    Yeh decorator check karta hai ke user logged in hai ya nahi.
    Agar nahi, to login page pe bhej deta hai.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login required', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



# ROUTE 1: HOME
@app.route('/')
def index():
    """
    Home page.
    Login hai to dashboard, warna login page.
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))



# ROUTE 2: SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    GET  → signup form visible
    POST → create new user, move to login page.
    """
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        confirm = request.form['confirm_password'].strip()

        # Validation
        if not username or not password:
            flash('Username andpassword required', 'error')
            return render_template('signup.html')

        if password != confirm:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')

        if len(password) < 6:
            flash('Password length should be at least 6 characters', 'error')
            return render_template('signup.html')

        # User banao
        if create_user(username, password):
            flash('Account Created! Login to your Account', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists', 'error')
            return render_template('signup.html')

    return render_template('signup.html')



# ROUTE 3: LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET  → open login form 
    POST → password verify, mark user as logged in, redirect to dashboard.
    """
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = get_user(username)

        if user and verify_password(user, password):
            #In Session ,user info save 
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')



# ROUTE 4: LOGOUT
@app.route('/logout')
def logout():
    """Session clear and redirect to login page."""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))



# ROUTE 5: DASHBOARD
@app.route('/dashboard')
@login_required
def dashboard():
    """
    Show user expenses + total.
    """
    user_id = session['user_id']
    expenses = get_expenses(user_id)
    total = get_total(user_id)

    return render_template(
        'dashboard.html',
        expenses=expenses,
        total=total,
        username=session['username']
    )



# ROUTE 6: ADD EXPENSE
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    GET  → open add form 
    POST → save new expense, redirect to dashboard.
    """
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
        except ValueError:
            flash('Amount must be a valid number', 'error')
            return render_template('add_expense.html')

        category = request.form['category'].strip()
        note = request.form['note'].strip()
        date = request.form['date']

        if amount <= 0:
            flash('Amount must be a positive number', 'error')
            return render_template('add_expense.html')

        if not category or not date:
            flash('Category and date are required', 'error')
            return render_template('add_expense.html')

        add_expense(session['user_id'], amount, category, note, date)
        flash('Expense added successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_expense.html')



# ROUTE 7: EDIT EXPENSE
@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit(expense_id):
    """
    GET  → open edit form  
    POST → save changes
    """
    user_id = session['user_id']
    expense = get_expense(expense_id, user_id)

    if expense is None:
        flash('Expense not found', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
        except ValueError:
            flash('Amount must be a valid number', 'error')
            return render_template('edit_expense.html', expense=expense)

        category = request.form['category'].strip()
        note = request.form['note'].strip()
        date = request.form['date']

        if amount <= 0:
            flash('Amount must be a positive number', 'error')
            return render_template('edit_expense.html', expense=expense)

        update_expense(expense_id, user_id, amount, category, note, date)
        flash('Expense update ho gaya', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_expense.html', expense=expense)



# ROUTE 8: DELETE EXPENSE
@app.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete(expense_id):
    """
    POST → delete expense.
    """
    user_id = session['user_id']

    if delete_expense(expense_id, user_id):
        flash('Expense deleted successfully', 'success')
    else:
        flash('Expense not found', 'error')

    return redirect(url_for('dashboard'))



# RUN
if __name__ == '__main__':
    app.run(debug=True)