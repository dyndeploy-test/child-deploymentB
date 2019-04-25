#!/usr/bin/env python3
from flask import Flask, request
import threading
import time
import logging
import requests
import os

app = Flask(__name__)


@app.before_first_request
def activate_job():
    def run_job():
        while True:
            # logging.warning("Run recurring task")
            time.sleep(0.25)

    thread = threading.Thread(target=run_job)
    thread.start()


@app.route('/')
def index():
    logging.warning(request.referrer)
    master_url = os.environ.get('SQUASH_MASTER_DEPLOYMENT')
    if not master_url:
        return '<body><h3 style="text-align: center; margin-top: 20%;">Deployment B is running independently</h3></body>'
    if 'https' not in master_url:
        master_url = f'https:{master_url}'
    try:
        resp = requests.get(master_url)
        if resp.status_code != 200:
            return f'<body><h1 style="text-align: center;">400</h1><h3 style="text-align: center; margin-top: 20%;">Deployment B is running. NO ACCESS to {master_url}</h3></body>'
    except Exception:
        return f'<body><h1 style="text-align: center;">400</h1><h3 style="text-align: center; margin-top: 20%;">Deployment B is running. NO ACCESS to {master_url}</h3></body>'

    return f'<body><h1 style="text-align: center;">200</h1><h4 style="text-align: center; margin-top: 20%;">Deployment B is running and has access to {master_url}</h4></body>'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
