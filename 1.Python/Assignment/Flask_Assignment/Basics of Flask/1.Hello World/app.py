# Import Flask and render_template from flask module
from flask import Flask, render_template

# Create an Flask object
app = Flask(__name__)

@app.route('/')     # Decorator for starting page
def loadpage():
    return render_template("index.html")        # Load webpage named index.html

# Start the Flask app
if __name__ == "__main__":
    app.run()