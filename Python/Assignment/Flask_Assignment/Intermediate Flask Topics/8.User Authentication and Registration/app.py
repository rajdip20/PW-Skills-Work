# Import necessary modules
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3


# Create a Flask object
app = Flask(__name__)
# Specify a secret key for a session
app.config['SECRET_KEY'] = 'your_secret_key'

# Specify the path to the SQLite database file
app.config['DATABASE'] = 'Python/Assignment/Flask_Assignment/Intermediate Flask Topics/8.User Authentication and Registration/users.db'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Create an user
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


# User data loader in the website
@login_manager.user_loader
def load_user(user_id):
    # Load user data from the database based on user_id
    user_data = query_db('SELECT * FROM users WHERE id = ?', [user_id], one=True)
    if user_data:
        # Create and return a User object
        return User(user_data[0], user_data[1], user_data[2])
    return None


# Function to establish a connection to the SQLite database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)


# Function to execute a database query and fetch results
def query_db(query, args=(), one=False):
    cur = connect_db().cursor()
    cur.execute(query, args)
    results = cur.fetchall()
    cur.close()
    # Return a single result (if 'one' is True) or a list of results
    return (results[0] if results else None) if one else results


# Function to execute a database query that modifies data (insert, update, delete)
def execute_db(query, args=()):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()


@app.route('/')
def load_page():
    # Home route to render the index.html template
    return render_template('index.html')


# Login route for handling user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = query_db('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)
        if user_data:
            # If user credentials are valid, log the user in
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)

            # Uncomment the line below if you want to use flash messages for successful login
            # flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # If login fails, flash an error message
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():            # Dashboard route accessible only to logged-in users
    return f'Hello, {current_user.username}! This is the dashboard. <a href="/logout">Logout</a>'


@app.route('/logout')
@login_required
def logout():           # Logout route to log the user out and redirect to the home page
    logout_user()
    # Flash a success message
    flash('You have been logged out.', 'success')
    return redirect(url_for('load_page'))


# Registration route for handling user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        
        if existing_user:
            # If username already exists, flash an error message
            flash('Username already exists. Please choose a different username.', 'danger')
        else:
            # If registration is successful, insert the new user into the database
            execute_db('INSERT INTO users (username, password) VALUES (?, ?)', [username, password])
            # Flash a success message
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')



if __name__ == '__main__':
    with app.app_context():
        # Create the 'users' table in the database if it doesn't exist
        execute_db('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

    # Run the Flask application
    app.run()