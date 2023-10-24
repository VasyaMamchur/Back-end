from flask import jsonify
import time
from datetime import datetime

from mymodule import app

is_healthy = True


def get_uptime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@app.route("/healthcheck")
def health_check():
    result = jsonify(isOk=is_healthy, uptime=get_uptime(), timestamp=time.time())
    result.status_code = 200 if is_healthy else 500
    return result