# Import all necessary modules
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# Create a Flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ABCxyz1234'
socketio = SocketIO(app)

# Track connected clients using a set
connected_clients = set()


# Route to load the main page
@app.route('/')
def load_page():
    return render_template('index.html')


# Socket event when a client connects
@socketio.on('connect')
def handle_connect():
    # Access request.sid within the socket event function
    connected_clients.add(request.sid)

    # Emit a notification to the connected client
    emit('notification', {'message': 'Connected to the server'}, room=request.sid)


# Socket event when a client disconnects
@socketio.on('disconnect')
def handle_disconnect():
    # Access request.sid within the socket event function
    connected_clients.remove(request.sid)

    # Emit a notification to the disconnected client
    emit('notification', {'message': 'Disconnected from the server'}, room=request.sid)


# Route to simulate sending a notification (not recommended, just for illustration)
@app.route('/send_notification')
def send_notification():
    # In a Flask route, we don't have access to request.sid directly
    # We can't use request.sid here; you can only use it within socket events
    return 'Notification not sent'



# Run the Flask app with SocketIO
if __name__ == '__main__':
    socketio.run(app)