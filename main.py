from flask import Flask, escape, request
from passit_builder import build_passit
import docker

app = Flask(__name__)


@app.route('/container/<name>', methods=['PUT', 'DELETE'])
def container(name):
    if request.method == 'DELETE':
        client = docker.from_env()
        container = client.containers.get(name)
        container.stop()
        container.rm()
        return 'No Content', 204
    elif request.method == 'PUT':
        if request.form['service'] == 'passit':
            build_passit(name)
        return 'Not Acceptable', 406
    return 'Not Acceptable', 406
