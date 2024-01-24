# Import all necessary modules
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import threading

# Create a Flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ABCxyz1234'
socketio = SocketIO(app)

# Shared data that will be updated in real-time
shared_data = {'value': 0}

def background_thread():
    count = 0
    while True:
        # Simulate a data update every second
        time.sleep(1)
        count += 1
        shared_data['value'] = count
        # Emit an 'update' event to the clients
        socketio.emit('update', {'data': shared_data['value']}, namespace='/test')


# Route to load the initial page
@app.route('/')
def load_page():
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    # Send the initial value of shared data to the connected client
    emit('update', {'data': shared_data['value']})


if __name__ == '__main__':
    # Start a background thread to update the data
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()

    # Run the application with SocketIO support
    socketio.run(app)