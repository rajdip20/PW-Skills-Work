# Import Flask, render_template, request from flask module
from flask import Flask, render_template, request

# Create an Flask object
app = Flask(__name__)

@app.route('/')     # Decorator for starting page
def load_page():
    return render_template('index.html')        # Load webpage named index.html

@app.route('/display', methods=['GET', 'POST'])     # Decorator for navigate to display page
def display():
    # Fetch all user input from index.html page
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    country = request.form.get('country')

    # Load the new webpage named display.html with all the user information
    return render_template('display.html', name=name, age=age, gender=gender, country=country)


# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0')