from src.adapter.sherlock_adapter import SherlockAdapter
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# import time
# from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/")
def home():
    return render_template('index.html')


@socketio.on('query')
def handle_query(data):
    print(f"process on {data['username']}")
    adapter = SherlockAdapter()
    adapter.start_sherlock(data['username'])

    while True:
        query_result, is_complete = adapter.get_result()
        if is_complete:
            # tell frontend it is completed, empty data for now
            emit('query_complete', {})
            break
        if len(query_result) != 0:
            emit('query_result', {'data': query_result})
    adapter = None


@socketio.on('connect')
def handle_connection(data):
    print("connected!")


@socketio.on('disconnect')
def handle_disconnect():
    print("connection closed!")


if __name__ == '__main__':
    socketio.run(app)
