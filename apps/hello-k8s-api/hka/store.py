from hka import app
import redis


# How to get config for redis ?
r = redis.Redis(host=app.config['REDIS_HOST'],
                port=app.config['REDIS_PORT'],
                db=0)
# r.flushall()


def redis_get_one(index):
    if not ping():
        return None
    msg = r.get(index)
    print("hka.redis.get_one: %s" % msg)
    msg = msg.decode()
    return msg


def redis_get_all():
    if not ping():
        return None
    all_msg = list()
    list_msg = list(r.scan_iter("[0-9]*", app.config['MAX_MSG_GET']))
    counter = 1
    while counter <= len(list_msg):
        all_msg.append(redis_get_one(counter))
        counter += 1
    print("*** all_msgs: %s" % all_msg)
    return all_msg


def set_new_key():
    if not ping():
        print("SET_NEW_KEY.if.NOT_PING")
        return None
    all_keys = list(r.scan_iter("[0-9]*", app.config['MAX_MSG_GET']))
    len_keys = len(all_keys)
    if len_keys == 0:
        new_key = 1
    else:
        new_key = len_keys + 1
    return new_key


def redis_set_one(value):
    index = set_new_key()
    if index is None:
        return None
    # print("Adding: %i = %s" % (index, value.decode()))
    if r.set(index, value):
        return value
    else:
        return None


def ping():
    try:
        r.ping()
        return True
    except ConnectionError:
        return False
    except redis.exceptions.ConnectionError:
        return False
