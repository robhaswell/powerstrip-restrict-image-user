import os

import json as _json

from flask import Flask, Response, request
app = Flask(__name__)
app.debug = True

import lib

@app.route("/", methods=["HEAD", "GET", "POST", "DELETE", "PUT"])
def adapter():
    json = request.get_data()
    decoded = _json.loads(json)
    docker_json = _json.loads(decoded['ClientRequest']['Body'])
    image = docker_json['Image']

    user = image.split("/")[0]
    if user != app.config['ALLOWED_USER']:
        return '', 403

    response = lib.pre_hook_response(
        decoded['ClientRequest']['Method'],
        decoded['ClientRequest']['Request'],
        decoded['ClientRequest']['Body'],
    )
    return Response(response, mimetype="application/json")

if __name__ == "__main__":
    app.config['ALLOWED_USER'] = os.environ['USER']
    app.run()
