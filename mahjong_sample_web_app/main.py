from flask import jsonify, request
from . import app


@app.route("/", methods=["GET"])
def index():
    body = request.json
    code = 200
    return jsonify({"ans": "AAA"}), code
