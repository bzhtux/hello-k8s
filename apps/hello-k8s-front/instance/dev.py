import os

######################
### HELLO-K8S-FRONTEND  # noqa
######################
HKF_DEBUG = True
HKF_HOST = "0.0.0.0"
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
