from flask import Flask, render_template, Response
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_sse.html')

def generate_data():
    for i in range(1, 11):
        start_time = time.time()
        result = i * 10
        elapsed_time = time.time() - start_time

        yield f"data: Iteration: {i}, Result: {result}, Elapsed Time: {elapsed_time:.2f} seconds\n\n"
        time.sleep(15)  # Simulate each iteration taking 15 seconds

@app.route('/stream')
def stream():
    return Response(generate_data(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)