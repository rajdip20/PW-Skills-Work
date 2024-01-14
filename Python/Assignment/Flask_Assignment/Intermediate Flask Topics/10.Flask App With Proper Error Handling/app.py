# Import all necessary modules
from flask import Flask, render_template, request

# Create a Flask object
app = Flask(__name__)

# Function to perform the calculation based on the operator and numbers
def perform_calculation(operator, num1, num2):
    try:
        if num1 is None or num2 is None:
            raise ValueError("Please provide values for both numbers")

        num1 = float(num1)
        num2 = float(num2)

        if operator == 'add':
            result = num1 + num2
        elif operator == 'subtract':
            result = num1 - num2
        elif operator == 'multiply':
            result = num1 * num2
        elif operator == 'divide':
            if num2 == 0:
                raise ValueError("Cannot divide by zero")
            result = num1 / num2
        else:
            raise ValueError("Invalid operator")

        return result

    except ValueError as v:
        # If There is an error, raise a ValueError with an appropriate message
        raise ValueError(f"Error in calculation: {str(v)}")


# Route to load the initial page
@app.route('/')
def load_page():
    return render_template('index.html')


# Route to handle the calculation form submission
@app.route('/', methods=['POST'])
def calculate():
    try:
        # Get operator and numbers from the form submission
        operator = request.form['operator']
        num1 = request.form['num1']
        num2 = request.form['num2']

        # Perform the calculation and render the result on the page
        result = perform_calculation(operator, num1, num2)
        return render_template('index.html', result=result, operator=operator, num1=num1, num2=num2)

    except ValueError as v:
        # If there is an error, render the error message on the page
        return render_template('index.html', error=str(v))


# Custom 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


# Custom 500 error handler
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Run the Flask application
    app.run()