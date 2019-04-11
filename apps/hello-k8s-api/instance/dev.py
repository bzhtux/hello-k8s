import os


#################
### HELLO-K8S-API  # noqa
#################
try:
    HKA_HOST = os.environ['HKA_HOST']
finally:
    HKA_HOST = "0.0.0.0"

try:
    HKA_PORT = os.environ['HKA_PORT']
finally:
    HKA_PORT = 5000

try:
    HKA_DEBUG = os.environ['HKA_DEBUG']
finally:
    HKA_DEBUG = True

MAX_MSG_GET = 10

#########
### REDIS  # noqa
#########
try:
    REDIS_HOST = os.environ['REDIS_HOST']
finally:
    REDIS_HOST = "0.0.0.0"

try:
    REDIS_PORT = int(os.environ['REDIS_PORT'])
finally:
    REDIS_PORT = 6379
