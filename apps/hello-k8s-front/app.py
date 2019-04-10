from hkf import app

if __name__ == "__main__":
    app.run(host=app.config['HKF_HOST'],
            port=app.config['HKF_PORT'],
            debug=app.config['HKF_DEBUG'])
