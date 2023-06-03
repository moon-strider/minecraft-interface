import argparse
import threading
import requests
import time

from flask import Flask, request
from flask import jsonify

from game import execute, prepare_game, interception_data, COMMANDS

REQUEST_WAIT_TIME = 3

app = Flask(__name__)
idata = None

def recieve_commands(server, endpoint, port):
    r = requests.request("POST", f"{server}/{endpoint}")
    cmd = r.json() if 200 <= r.status_code <= 299 else None
    if cmd.replace("_", " ") in COMMANDS:
        execute(idata, cmd)
    time.sleep(REQUEST_WAIT_TIME)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip')
    parser.add_argument('--port')
    parser.add_argument('--server_ip')
    parser.add_argument('--server_port')
    parser.add_argument('--set_cmd_endpoint')
    parser.add_argument('--recieve_endpoint')
    args = parser.parse_args()
    idata = interception_data(*prepare_game())
    threading.Thread(app.run(host=args.ip, port=int(args.port), debug=True, use_reloader=False))
    requests.request("POST", f"{args.server_ip}/{args.set_cmd_endpoint}")
    recieve_commands(args.server_ip, args.recieve_endpoint, args.server_port)