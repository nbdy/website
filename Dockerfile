FROM python:slim
RUN mkdir /app
RUN apt-get update ; apt-get install -y gcc file make
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY static /app/static
COPY templates /app/templates
COPY srv.py /app/srv.py
COPY config.json /app/config.json

EXPOSE 51337

CMD ["python3", "/app/srv.py", "--host", "0.0.0.0", "-p", "51337"]