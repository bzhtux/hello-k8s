from hkf import app
import re
import os


def get_keys_from_config(config_file):
    ''' Get all configuration keys from configuration file in `instance/` directory.

        :param config_file:     relative path to configuration file
        :type config_file:      string()
        :return:                A list of keys
        :rtype:                 list()

        :Example:

        >>> from api.utils import get_keys_from_config
        >>> from api import app
        >>> config_file = "instance/%s.py" % app.config['ENV']
        >>> config_keys = get_keys_from_config(config_file)
        >>> config_keys
        ['APP_NAME', 'APP_VERSION', 'APP_DESC', 'APP_FQDN', 'ASSETS_SRV', 'RECIPES_SRV',
        'TOKEN_SRV', 'USERS_SRV', 'HKF_API_ENDPOINT', 'HKF_API_PORT', 'HKF_SECRET_KEY',
        'HKF_TOP_LEVEL_DIR', 'HKF_EMAIL_VERIFY', 'HKF_DEBUG', 'HKF_ADMIN_PASS',
        'HKF_TOKEN_VALID_DURATION', 'HKF_DB_CONNECTOR', 'HKF_DB_NAME', 'SQLALCHEMY_DATABASE_URI',
        'SQLALCHEMY_TRACK_MODIFICATIONS', 'JWT_ALGO', 'JWT_SECRET', 'JWT_EXPIRATION']
    '''
    with open(config_file, "r") as conf_fd:
        data = conf_fd.read()
    data = data.split("\n")
    keys = list()
    for item in data:
        # print("*** analysing %s" % item)
        if item != "" \
                and re.search("import", item) is None \
                and re.search("from", item) is None \
                and re.search("# ", item) is None:
            if item.split(" =")[0] != "None":
                # print("%s---" % item.split(" =")[0])
                keys.append(item.split(" =")[0])
    return keys


def set_config_keys(config_dict):
    ''' Set new configuration app.config[$KEYS].

        :param config_dict:     new configuration keys and values
        :type config_dict:      dict()
        :type config_dict:      dict()
        :return:                True if new config is sync, False if not
        :rtype:                 bool()

        :Example:

        >>> from api.utils import set_config_keys
        >>> os.environ['APP_VERSION'] = "0.0.2"
        >>> env_keys = dict()
        >>> env_keys['APP_VERSION'] = os.environ['APP_VERSION']
        >>> set_config_keys(env_keys)
        * old value: APP_VERSION = 0.0.1
        * new value: APP_VERSION = 0.0.2
        >>> app.fonfig['APP_VERSION']
        '0.0.2'
    '''
    try:
        for key in config_dict:
            # print("* old value: %s = %s" % (key, app.config[key]))
            app.config[key] = config_dict[key]
            # print("* new value: %s = %s" % (key, app.config[key]))
            return True
    except Exception as e:
        if app.config['HKF_DEBUG']:
            print("set_config_keys.except: %s" % e)
        return False


def build_new_envars(config_keys):
    '''
    '''
    conf = dict()
    for key in config_keys:
        try:
            if os.environ[key] != "":
                conf[key] = os.environ[key]
                if app.config['HKF_DEBUG']:
                    print(" * override %s : True" % key)
                    print("   > new value: %s" % os.environ[key])
        except Exception as e:
            if app.config['HKF_DEBUG']:
                print(" * override %s : False" % e)
    return conf


def use_env_vars():
    ''' Use variable environnment as settings. Useful to run app within docker.
    '''
    try:
        config_file = "instance/%s.py" % os.environ['FLASK_ENV']
    except Exception as e:
        config_file = "instance/prod.py"
    config_keys = get_keys_from_config(config_file)
    conf = build_new_envars(config_keys)
    if len(conf) > 0:
        if set_config_keys(conf) and app.config['HKF_DEBUG']:
            print(" * New conf applied: %s" % conf)
    return True
