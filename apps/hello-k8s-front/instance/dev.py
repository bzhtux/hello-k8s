import os

######################
### HELLO-K8S-FRONTEND  # noqa
######################
if os.environ['HKF_DEBUG'] != "":
    HKF_DEBUG = os.environ['HKF_DEBUG']
else:
    HKF_DEBUG = False
if os.environ['HKF_HOST'] != "":
    HKF_HOST = os.environ['HKF_HOST']
else:
    HKF_HOST = "0.0.0.0"
if os.environ['HKF_PORT'] != "":
    HKF_PORT = os.environ['HKF_PORT']
else:
    HKF_PORT = 8080
MAX_MSG_GET = 10


#######
### API  # noqa
#######
if os.environ['API_HOST'] != "":
    API_HOST = os.environ['API_HOST']
else:
    API_HOST = "0.0.0.0"

if os.environ['API_PORT'] != "":
    API_PORT = int(os.environ['API_PORT'])
else:
    API_PORT = 5000
