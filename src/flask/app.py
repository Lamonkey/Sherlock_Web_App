# from gevent import monkey
# monkey.patch_all()
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request
from src.adapter.sherlock_adapter import SherlockAdapter



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
adapter_for_sessions = {}
adapter_to_delete = {}


@app.route("/")
def home():
    return render_template('index.html')


@socketio.on('continous_result')
def send_query_result():
    current_socket_Id = request.sid
    adapter = adapter_for_sessions[current_socket_Id]
    # adapter.start_sherlock(user_name)
    query_result, is_complete = adapter.get_result()
    # print(f"sending result to {current_socket_Id}")
    emit('query_result', {'data': query_result})
    # tell frontend it is completed, empty data for now
    if is_complete:
        emit('query_complete', {})


@socketio.on('query')
def handle_query(data):
    current_socket_Id = request.sid
    print(f"process on {data['username']}")
    adapter_for_sessions[current_socket_Id] = SherlockAdapter()
    adapter_for_sessions[current_socket_Id].start_adapter(data['username'])
    emit('query_result', {'data': [('running', '#')]})


@socketio.on('connect')
def handle_connection(data):
    current_socket_Id = request.sid
    print(f"{current_socket_Id} connected!")
    adapter_for_sessions[current_socket_Id] = None
    print(f"created worker for {current_socket_Id}")


@socketio.on('disconnect')
def handle_disconnect():
    '''
    delete sherlock_adapter, and close adapter if finished
    '''
    current_socket_Id = request.sid
    print(f"{current_socket_Id} closed connection!")

    adapter_to_delete[current_socket_Id] = adapter_for_sessions[current_socket_Id]
    del adapter_for_sessions[current_socket_Id]

    keys = list(adapter_to_delete.keys())
    for key in keys:
        if adapter_to_delete[key] is None:
            del adapter_to_delete[key]
            continue
        if adapter_to_delete[key].get_status():
            del adapter_to_delete[key]
            print(f"remove worker for {key}")


if __name__ == '__main__':
    socketio.run(app)
