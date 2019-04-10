from hka import app


if __name__ == "__main__":
    app.run(host=app.config['HKA_HOST'],
            port=app.config['HKA_PORT'],
            debug=app.config['HKA_DEBUG'])