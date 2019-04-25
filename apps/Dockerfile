FROM alpine:latest

RUN apk update \
    && apk add  dumb-init \
                python3 \
                curl \
                make \
                gcc \
                python3-dev \
                musl-dev

RUN addgroup -S flask \
    && adduser -S flask -G flask \
    && mkdir -p /app \
    && chown -R flask.flask /app
