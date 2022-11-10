import sys
import os.path
goal_dir = os.path.join(os.path.dirname(__file__), '../../')
goal_dir = os.path.normpath(goal_dir)
sys.path.insert(0, goal_dir)
from src.adapter import sherlock_adapter
from flask import Flask, request, Response, json, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from queue import Queue

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()
queue_list = {}
result_queue = Queue()


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/search_users', methods=['GET'])
def search_user():
    args = request.args
    data = args.to_dict()
    # string username sepearte by sapce
    username = data['usernames']
    scheduler.add_job(sherlock_adapter.run_sherlock, kwargs={
                      'result_queue': result_queue, 'user_name': username})
    return Response("{'a':'b'}", status=200, mimetype='application/json')
    # return f"submited request for {username}"


@app.route('/get_result', methods=['GET'])
def get_result():
    data = sherlock_adapter.dequeue(result_queue)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run(debug=True)
