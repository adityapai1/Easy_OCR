from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import threading
import eventlet

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

def ocr_process():
    # Simulating a list of statements to be sent
    statements = [
        "Statement 1",
        "Statement 2",
        "Statement 3",
        "Statement 4",
        "Statement 5",
    ]

    for statement in statements:
        # Simulating OCR processing time
        time.sleep(2)

        # Send the statement to the client via WebSocket
        socketio.emit('ocr_update', {'statement': statement}, namespace='/ocr')

if __name__ == '__main__':
    # Start the OCR process in a separate thread
    ocr_thread = threading.Thread(target=ocr_process)
    ocr_thread.start()

    # Run the Flask app using the eventlet event loop
    socketio.run(app)
