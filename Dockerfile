FROM python:slim
RUN mkdir /app
RUN apt-get update ; apt-get install -y gcc file make git
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY static /app/static
COPY templates /app/templates
COPY srv.py /app/srv.py
COPY config.json /app/config.json
WORKDIR /app/

EXPOSE 51337

CMD ["python3", "srv.py", "--host", "0.0.0.0", "-p", "51337"]