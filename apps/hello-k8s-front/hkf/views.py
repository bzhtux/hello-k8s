from hkf import app
from hkf.api import send_msg, get_msgs
from flask import render_template, request, jsonify, flash


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        send_msg(request)
    all_msg = get_msgs()
    print("*** all_msg just after calling it: %s" % all_msg)
    if not all_msg:
        flash('Sorry API is not responding ... try again later ;-(')
    elif (all_msg is not None and len(all_msg) == 0):
        all_msg = ["No messages yet :("]
    return render_template("index.html", messages=all_msg)


@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "success"}), 200
