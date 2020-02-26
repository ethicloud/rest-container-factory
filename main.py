from flask import Flask, escape, request
import docker

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'World'


@app.route('/container', methods=['PUT'])
def containers():
    if request.method == 'PUT':
        if request.form['name']:
            client = docker.from_env()
            client.containers.run("nginx", detach=True, ports={
                                  "80/tcp": 80}, name=request.form['name'])
            return 'No Content', 204
        return 'Not Acceptable', 406


@app.route('/container/<name>', methods=['DELETE'])
def container(name):
    if request.method == 'DELETE':
        client = docker.from_env()
        client.containers.get(name).stop()
        return 'No Content', 204
