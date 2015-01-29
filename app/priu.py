import os, sys

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
    try:
        app.config['ALLOWED_USER'] = os.environ['USER']
    except KeyError:
        sys.stdout.write("""Error: Configuration environment variable USER not provided.

Specify an image username on the Docker command-line by using docker run -e USER=<user>.

Use the user "_" to only allow official Docker images.
""")
        sys.exit(1)
    app.run(port=80)
