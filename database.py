#database logic is file mein hai.

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


# Database Connection
def get_db():
    """
    Database connection kholta hai.
    row_factory = sqlite3.Row — isse hum row['column_name'] likh sakte hain
    """
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn



# USER FUNCTIONS
def create_user(username, password):
    """
    Naya user banata hai. Password ko hash kar ke store karta hai.
    Returns: True agar user bana, False agar username pehle se hai
    """
    conn = get_db()
    cur = conn.cursor()
    password_hash = generate_password_hash(password)

    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError: #unique username check krn k liye
        
        return False #username already exists
    finally:
        conn.close()


def get_user(username):
    """
    Username se user dhoondta hai (login ke liye).
    Returns: row object ya None
    """
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()
    return user


def verify_password(user, password):
    """
    Check karta hai ke password sahi hai ya nahi.
    Returns: True / False
    """
    return check_password_hash(user['password_hash'], password)



# EXPENSE FUNCTIONS
def add_expense(user_id, amount, category, note, date):
    """
    Naya expense add karta hai.
    Returns: naye expense ka ID
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO expenses (user_id, amount, category, note, date) 
        VALUES (?, ?, ?, ?, ?)""",

        (user_id, amount, category, note, date)
    )
    conn.commit()
    expense_id = cur.lastrowid #Jonsi expense ka ID hai, wo return krta hai
    conn.close()
    return expense_id


def get_expenses(user_id):
    """
    User ke saare expenses return karta hai — naye pehle.
    """
    conn = get_db()
    expenses = conn.execute(
        """SELECT * FROM expenses
           WHERE user_id = ?
           ORDER BY date DESC, id DESC""",
        (user_id,) #Is user id k liye saare expenses dhoondta hai.
    ).fetchall()
    conn.close()
    return expenses


def get_expense(expense_id, user_id):
    """
    Ek single expense dhoondta hai (edit page ke liye).
    user_id bhi check — security ke liye.
    """
    conn = get_db()
    expense = conn.execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, user_id)
    ).fetchone()
    conn.close()
    return expense


def update_expense(expense_id, user_id, amount, category, note, date):
    """
    Expense edit karta hai.
    Returns: True agar update hua, False agar expense mila hi nahi
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """UPDATE expenses
           SET amount = ?, category = ?, note = ?, date = ?
           WHERE id = ? AND user_id = ?""",
        (amount, category, note, date, expense_id, user_id)
    )
    conn.commit()
    updated = cur.rowcount > 0
    conn.close()
    return updated


def delete_expense(expense_id, user_id):
    """
    Expense delete karta hai.
    user_id check.
    Returns: True agar delete hua, False agar nahi mila
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, user_id)
    )
    conn.commit()
    deleted = cur.rowcount > 0 #update ya delete hone k baad rowcount check krta hai true ya fasle dene k liye.
    conn.close()
    return deleted


def get_total(user_id):
    """
    User ke saare expenses ka total nikaalta hai.
    Returns: total amount.
    """
    conn = get_db()
    row = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE user_id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    return row['total']