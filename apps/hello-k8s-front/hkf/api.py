from hkf import app
import requests

API_URL = "http://%s:%i" % (app.config['API_HOST'], app.config['API_PORT'])


def send_msg(request):
    new_msg = request.form['msg']
    requests.post("%s/new" % API_URL, new_msg.encode())


def get_msgs():
    r = requests.get(API_URL)
    data = r.json()
    data['messages'].reverse()
    messages = list()
    if len(data['messages']) == 0:
        return messages
    # print(len(data['messages']))
    counter = 0
    if len(data['messages']) <= app.config['MAX_MSG_GET']:
        MAX = len(data['messages'])
    else:
        MAX = app.config['MAX_MSG_GET']
    while counter < MAX:
        messages.append(data['messages'][counter])
        counter += 1
    return messages
