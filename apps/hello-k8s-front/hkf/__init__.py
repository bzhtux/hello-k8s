from flask import Flask
import sys
import os

sys.path.append(os.path.abspath(os.curdir))

app = Flask(__name__, instance_relative_config=True)

# Try to get env from SHELL ENV
# Set to 'prod' by default
try:
    env = os.environ['FLASK_ENV']
except Exception as e:
    print(" * [hello-k8s-front] Setting env to default: production")
    print(" * {}".format(e))
    env = "prod"

# print(" * FLASK_ENV: {}".format(env))

# Load the config file regarding env above
if env == "dev":
    app.config.from_pyfile('dev.py')
elif env == "test":
    app.config.from_pyfile('test.py')
elif env == "prod":
    app.config.from_pyfile('prod.py')
elif env == "docker":
    app.config.from_pyfile('docker.py')
else:
    print(" * [hello-k8s-front] Unrecognized FLASK_ENV value, exiting ...")
    print(" * Available envs: dev/test/prod")
    sys.exit(1)

try:
    import hkf.views     # noqa
except Exception as e:
    print("import hkf.views.except:", e)
    sys.exit(1)

from hkf.utils import use_env_vars  # noqa

use_env_vars()