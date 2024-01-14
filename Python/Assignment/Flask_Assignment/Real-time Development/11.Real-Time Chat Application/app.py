# Import all necessary modules
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Create a Flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ABCxyz1234'
socketio = SocketIO(app)

# Route to load the initial page
@app.route('/')
def load_page():
    return render_template('index.html')


@socketio.on('message')
def handle_message(msg):
    # Print the received message to the server console
    print('Received message: ' + msg)

    # Broadcast the received message to all connected clients
    emit('message', msg, broadcast=True)


if __name__ == '__main__':
    # Run the Flask application with SocketIO support
    socketio.run(app, use_reloader=False)