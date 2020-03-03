from flask import Flask, escape, request
from passit_builder import build_passit, destroy_passit

app = Flask(__name__)


@app.route('/container/<name>', methods=['PUT', 'DELETE'])
def container(name):
    if request.method == 'DELETE':
        if name:
            destroy_passit(name)
            return 'No Content', 204
    elif request.method == 'PUT':
        if request.form['service'] == 'passit':
            build_passit(name)
            return 'Created', 201
        return 'Not Acceptable', 406
    return 'Not Acceptable', 406
