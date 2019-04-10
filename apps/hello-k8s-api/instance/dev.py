import os


#################
### HELLO-K8S-API  # noqa
#################
HKA_HOST = "0.0.0.0"
HKA_PORT = 5000
HKA_DEBUG = True
MAX_MSG_GET = 10
FLASK_DEBUG = True

#########
### REDIS  # noqa
#########
if os.environ['REDIS_HOST'] != "":
    REDIS_HOST = os.environ['REDIS_HOST']
else:
    REDIS_HOST = "0.0.0.0"

if os.environ['REDIS_PORT'] != "":
    REDIS_PORT = int(os.environ['REDIS_PORT'])
else:
    REDIS_PORT = 6379
