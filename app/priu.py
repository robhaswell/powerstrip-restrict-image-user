import os

from flask import Flask
app = Flask(__name__)

@app.route("/", methods=["HEAD", "GET", "POST", "DELETE", "PUT"])
def adapter():
    return "Some data"

if __name__ == "__main__":
    app.config['ALLOWED_USER'] = os.environ['USER']
    app.run()
