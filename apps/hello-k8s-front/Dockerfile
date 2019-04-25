FROM bzhtux/hello-k8s-base:latest

COPY . /app

WORKDIR /app

RUN rm -rf hkf/__pycache__

RUN pip3 install -r requirements.txt

EXPOSE 80 8080

USER flask

ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]

CMD ["python3", "app.py"]
