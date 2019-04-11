import os

######################
### HELLO-K8S-FRONTEND  # noqa
######################
try:
    HKF_DEBUG = os.environ['HKF_DEBUG']
finally:
    HKF_DEBUG = False

try:
    HKF_HOST = os.environ['HKF_HOST']
finally:
    HKF_HOST = "0.0.0.0"

try:
    HKF_PORT = os.environ['HKF_PORT']
finally:
    HKF_PORT = 8080
MAX_MSG_GET = 10


#######
### API  # noqa
#######
try:
    API_HOST = os.environ['API_HOST']
finally:
    API_HOST = "0.0.0.0"

try:
    API_PORT = int(os.environ['API_PORT'])
finally:
    API_PORT = 5000
