# Import all necessary modules
from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google


# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management
app.secret_key = 'ABCxyz1234'

# Create a Google Blueprint for authentication
google_set = make_google_blueprint(client_id='395518691726-4q7eu8i12ntgve59t5giaqnouliepge6.apps.googleusercontent.com',
                                   client_secret='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',
                                   redirect_to='google_login',
                                   redirect_url='/google_login/google/authorized')

# Register the Google Blueprint with the Flask application
app.register_blueprint(google_set, url_prefix='/google_login')


# Define the route for initiating the Google login process
@app.route('/google_login')
def google_login():
    # Check if the user is not authorized and redirect to the Google login page
    if not google.authorized:
        return redirect(url_for('google.login'))

    # Retrieve user information from the Google API
    response = google.get('/plus/v1/people/me')
    assert response.ok, response.text

    # Display the user's display name if successfully logged in
    return 'Logged in as: {}'.format(response.json()['displayName'])


# Define the home page route
@app.route('/')
def load_page():
    # Redirect to the Google login page if user is authorized
    if google.authorized:
        return redirect(url_for('google_login'))

    # Render the home page template if user is not authorized
    return render_template('index.html')


# Define the route for handling Google login authorization
@app.route('/google_login/google/authorized')
def google_login_auth():
    # Redirect to the Google login page after successful authorization
    return redirect(url_for('google_login'))



# Run the Flask application
if __name__ == '__main__':
    app.run()