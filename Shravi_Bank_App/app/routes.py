from app import app
from app import db
from app.models import User

from flask import request

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return f"Username '{username}' already exists. Please choose a different username."

        # Add the new user to the database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return f"User '{username}' added successfully!"
    else:
        # Render a form for adding users
        return '''
        <form method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br>
            <button type="submit">Add User</button>
        </form>
        '''
@app.route('/view_users')
def view_users():
    users = User.query.all()
    user_list = ""
    for user in users:
        user_list += f"<p>Username: {user.username}</p>"
    if not user_list:
        user_list = "<p>No users found.</p>"
    return user_list

from flask import redirect, url_for

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username exists in the database
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return f"Welcome, {username}! You have successfully logged in."
        elif user:
            return "Invalid password. Please try again."
        else:
            return "Username not found. Please sign up first."

    # Render a login form
    return '''
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
    '''
