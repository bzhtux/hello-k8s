FROM alpine:latest

RUN apk update \
    && apk add dumb-init python3

RUN addgroup -S flask \
    && adduser -S flask -G flask \
    && mkdir -p /app \
    && chown -R flask.flask /app

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 80 8080

ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]

CMD ["python3", "app.py"]