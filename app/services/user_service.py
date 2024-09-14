# app/services/user_service.py

from app.models.user import User, db

def create_user(username, email, password, role='user'):
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        raise ValueError('Email already exists')

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

def get_all_users():
    return User.query.all()
