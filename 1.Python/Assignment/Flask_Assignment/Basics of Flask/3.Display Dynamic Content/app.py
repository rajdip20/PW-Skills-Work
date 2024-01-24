# Import Flask, render_template, request, redirect, url_for from flask module
from flask import Flask, render_template, request, redirect, url_for

# Create an Flask object
app = Flask(__name__)

@app.route('/')     # Decorator for starting page
def load_page():
    return render_template("index.html")        # Load webpage named index.html

@app.route('/user', methods=['POST'])       # Decorator for redirect another function
def display_profile():
    username = request.form.get('username')     # Get username from index.html
    return redirect(url_for('get_profile', username=username))      # Redirect or call get_profile function by pass username data

@app.route('/<username>')       # Decorator for user page with username in the url (dynamic link)
def get_profile(username):

    # Load the new webpage named profile.html with username
    # The page displays dynamic content for different users
    return render_template("profile.html", username=username)


# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0")