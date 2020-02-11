FROM debian:wheezy
RUN apt-get install -y python3 python3-pip
RUN mkdir /app
RUN mkdir /app/cert
COPY ../requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY ../static/ /app/static
COPY ../templates /app/templates
COPY ../srv.py /app/srv.py

ENTRYPOINT ["/usr/bin/python3", "/app/srv.py", "--host", "0.0.0.0", "-p", "8080"]
CMD ["-sc", "", "-sk", ""]