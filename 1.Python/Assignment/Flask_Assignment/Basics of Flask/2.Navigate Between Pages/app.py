# Import Flask, render_template from flask module
from flask import Flask, render_template

# Create an Flask object
app = Flask(__name__)

@app.route('/')     # Decorator for starting page
def load_page():
    return render_template("index.html")        # Load webpage named index.html

@app.route('/newpage')      # Decorator for going next page
def go_next():
    return render_template("newpage.html")      # Load the new webpage named newpage.html

@app.route('/')     # Decorator for going starting page
def go_prev():
    load_page()     # Call load_page function to load the index.html page

# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0")