import os


#################
### HELLO-K8S-API  # noqa
#################
if os.environ['HKA_HOST'] != "":
    HKA_HOST = os.environ['HKA_HOST']
else:
    HKA_HOST = "0.0.0.0"
if os.environ['HKA_PORT'] != "":
    HKA_PORT = os.environ['HKA_PORT']
else:
    HKA_PORT = 5000
if os.environ['HKA_DEBUG'] != "":
    HKA_DEBUG = os.environ['HKA_DEBUG']
else:
    HKA_DEBUG = True
MAX_MSG_GET = 10

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
