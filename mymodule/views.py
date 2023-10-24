from flask import jsonify
import time
from datetime import datetime

from mymodule import app

is_healthy = True


def get_uptime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route("/hello")
def hello():
    return "Hello!"

@app.route("/healthcheck")
def health_check():
    result = jsonify(IsOk=is_healthy, current_date=get_uptime(), epoch_time=time.time())
    result.status_code = 200 if is_healthy else 500
    return result