from hkf import app
import requests


API_URL = "http://%s:%i" % (app.config['API_HOST'], app.config['API_PORT'])


def send_msg(request):
    if not ping():
        return None
    new_msg = request.form['msg']
    if requests.post("%s/new" % API_URL, new_msg.encode()):
        return True
    else:
        return False


def get_msgs():
    if not ping():
        return None
    r = requests.get(API_URL)
    data = r.json()
    data['messages'].reverse()
    messages = list()
    if len(data['messages']) == 0:
        return messages
    counter = 0
    if len(data['messages']) <= app.config['MAX_MSG_GET']:
        MAX = len(data['messages'])
    else:
        MAX = app.config['MAX_MSG_GET']
    while counter < MAX:
        messages.append(data['messages'][counter])
        counter += 1
    return messages


def ping():
    try:
        response = requests.get('%s/healthz' % API_URL)
    except requests.exceptions.ConnectionError:
        return False
    if (response is not None and response.status_code == 200):
        return True
    else:
        return False
