from hkf import app
from hkf.api import send_msg, get_msgs
from flask import render_template, request


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        send_msg(request)
    all_msg = get_msgs()
    if len(all_msg) == 0:
        all_msg = ["No messages yet :("]
    return render_template("index.html", messages=all_msg)