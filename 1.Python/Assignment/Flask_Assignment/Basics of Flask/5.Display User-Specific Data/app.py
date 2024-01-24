# Import Flask, render_template, request, session, redirect, url_for from flask module
from flask import Flask, render_template, request, session, redirect, url_for

# Create a Flask object
app = Flask(__name__)
app.secret_key = '84mjn4'       # Create a secret_key for a session



@app.route('/')     # Decorator for starting page
def load_page():
    return render_template('index.html')        # Load webpage named index.html



@app.route('/login', methods=['POST'])      # Decorator for redirect another function
def login():
    if request.method == 'POST':
        username = request.form['username']     # Get username from index.html
        session['username'] = username          # Store the username in session variable with username key
        return redirect(url_for('user_profile'))        # Redirect or call user_profile function

@app.route('/profile')      # Decorator for user profile page
def user_profile():
    if 'username' in session:
        username = session['username']          # Store the username from session variable to username variable
        
        # Create some example data for user for demonstration purposes
        user_data = {
            'name': username,
            'age': 25,
            'gender': 'Male',
            'country': 'Country X'
        }
        return render_template('profile.html', user_data=user_data)     # Load the new webpage named profile.html with user data
    return redirect(url_for('load_page'))       # If there is no username in session then redirect to load_page function

@app.route('/logout')       # Decorator for logout page
def logout():
    session.pop('username', None)       # Remove the username from the session
    return redirect(url_for('load_page'))       # Redirect to load_page function when user logged out


# Start the flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0')