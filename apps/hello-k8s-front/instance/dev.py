import os

######################
### HELLO-K8S-FRONTEND  # noqa
######################
try:
    HKF_DEBUG = os.environ['HKF_DEBUG']
except KeyError:
    HKF_DEBUG = True

try:
    HKF_HOST = os.environ['HKF_HOST']
except KeyError:
    HKF_HOST = "0.0.0.0"

try:
    HKF_PORT = os.environ['HKF_PORT']
except KeyError:
    HKF_PORT = 8080
MAX_MSG_GET = 10
SECRET_KEY = "G1sPYEOyG,@a#E.0(%ZrY60pXD46c6Ti,x7od5W17UNJds;k@;sObDfj6?BvlND="
DOCKER_VERSION = "0.0.16"

#######
### API  # noqa
#######
try:
    API_HOST = os.environ['API_HOST']
except KeyError:
    API_HOST = "0.0.0.0"

try:
    API_PORT = int(os.environ['API_PORT'])
except KeyError:
    API_PORT = 5000
