"""
database.py

"""

import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# MODELS/Tables
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    expenses = db.relationship('Expense', backref='user', lazy=True)


class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(200))
    date = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


# SETUP
# SETUP
def init_db(app):
    database_url = os.environ.get('DATABASE_URL')

    # SQLAlchemy ko 'postgres://' pasand nahi, usay 'postgresql://' chahiye
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    db.init_app(app)

# USER FUNCTIONS
def create_user(username, password):
    existing = User.query.filter_by(username=username).first()
    if existing:
        return False

    user = User(
        username=username,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    return True


def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return {
            'id': user.id,
            'username': user.username,
            'password_hash': user.password_hash
        }
    return None


def verify_password(user, password):
    return check_password_hash(user['password_hash'], password)


# EXPENSE FUNCTIONS
def add_expense(user_id, amount, category, note, date):
    expense = Expense(
        user_id=user_id,
        amount=amount,
        category=category,
        note=note,
        date=date
    )
    db.session.add(expense)
    db.session.commit()
    return expense.id


def get_expenses(user_id):
    expenses = Expense.query.filter_by(user_id=user_id) \
        .order_by(Expense.date.desc(), Expense.id.desc()).all()

    return [{
        'id': e.id,
        'user_id': e.user_id,
        'amount': e.amount,
        'category': e.category,
        'note': e.note,
        'date': e.date
    } for e in expenses]


def get_expense(expense_id, user_id):
    e = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
    if e:
        return {
            'id': e.id,
            'user_id': e.user_id,
            'amount': e.amount,
            'category': e.category,
            'note': e.note,
            'date': e.date
        }
    return None


def update_expense(expense_id, user_id, amount, category, note, date):
    e = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
    if not e:
        return False

    e.amount = amount
    e.category = category
    e.note = note
    e.date = date
    db.session.commit()
    return True


def delete_expense(expense_id, user_id):
    e = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
    if not e:
        return False

    db.session.delete(e)
    db.session.commit()
    return True


def get_total(user_id):
    result = db.session.query(db.func.sum(Expense.amount)) \
        .filter_by(user_id=user_id).scalar()
    return result or 0