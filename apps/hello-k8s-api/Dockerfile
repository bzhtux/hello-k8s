FROM bzhtux/hello-k8s-base:latest

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

USER flask

ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]

CMD ["python3", "app.py"]
