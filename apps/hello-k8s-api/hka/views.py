from hka import app
from hka.store import redis_set_one, redis_get_all
from flask import jsonify, request


@app.route("/", methods=['GET'])
def get_all():
    all_msg = redis_get_all()
    return jsonify({"status": "success", "messages": all_msg}), 200


@app.route("/new", methods=['POST'])
def add_one():
    new_msg = redis_set_one(request.data)
    if new_msg is not None:
        return jsonify({"status": "success", "message": new_msg.decode()}), 200
    else:
        return jsonify({"status": "error"}), 400
