FROM python:slim
RUN mkdir /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY static /app/static
COPY templates /app/templates
COPY srv.py /app/srv.py
COPY config.json /app/config.json

CMD ["/usr/bin/python3", "/app/srv.py", "--host", "127.0.0.1", "-p", "51337"]