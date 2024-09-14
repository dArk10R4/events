# app/routes/user_routes.py

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import User, db
from app.services.user_service import get_all_users, create_user

user_routes = Blueprint('user_routes', __name__)

# Login Page
@user_routes.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        print(user)
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('user_routes.create_user_page'))
            else:
                return redirect(url_for('user_routes.user_dashboard'))
        else:
            flash('Login failed. Check email and password.', 'danger')
    
    return render_template('login.html', title='Login')


# Logout Route
@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('user_routes.login_page'))


# Admin Create User Page (GET) - Requires login
@user_routes.route('/admin/create_user_page', methods=['GET'])
@login_required
def create_user_page():
    if current_user.role != 'admin':
        return redirect(url_for('user_routes.user_dashboard'))
    
    return render_template('admin.html', title='Create User')


# User Dashboard (GET) - Simple User Page after Login
@user_routes.route('/user/dashboard', methods=['GET'])
@login_required
def user_dashboard():
    return render_template('user_dashboard.html', title='User Dashboard')


# View all users (admin-only)
@user_routes.route('/admin/users_page', methods=['GET'])
@login_required
def users_page():
    if current_user.role != 'admin':
        return redirect(url_for('user_routes.user_dashboard'))
    
    users = get_all_users()
    return render_template('users.html', title='All Users', users=users)
