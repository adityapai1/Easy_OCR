from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/multiples')
def run_multiples():
    for i in range(1, 11):
        start_time = time.time()
        result = i * 10
        elapsed_time = time.time() - start_time

        # Send the update to the client via WebSocket
        emit('multiples_update', {'result': result, 'seconds': elapsed_time}, namespace='/multiples')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
