# Import necessary modules
from flask import Flask, render_template, request
import requests
import random

# Create a Flask object
app = Flask(__name__)


# Function to get data from a public API
def get_publicAPIs_data():
    url = 'https://api.publicapis.org/entries'
    response = requests.get(url)
    data = response.json()
    return data


# Define the route for the main page
@app.route('/')
def load_page():
    # Render the 'index.html' template for the main page
    return render_template('index.html')


# Define the route for the results page, handling both GET and POST requests
@app.route('/results', methods=['POST', 'GET'])
def results():
    # Check if the request method is POST
    if request.method == 'POST':
        # Retrieve the number of APIs specified by the user from the form
        number = int(request.form['number'])

        # Get data from the public API
        data = get_publicAPIs_data()

        # Select a random subset of APIs based on the user-specified number
        select_random = random.sample(data['entries'], number)

        # Render the 'results.html' template with the selected data
        return render_template('results.html', data={'count': len(data['entries']), 'entries': select_random, 'entries_count': len(select_random)})
    else:
        # If the request method is GET, render the 'index.html' template
        return render_template('index.html')



# Run the Flask application
if __name__ == '__main__':
    app.run()