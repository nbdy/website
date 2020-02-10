FROM ubuntu:18.04
RUN apt-get install -y python3 python3-pip
RUN mkdir /app
COPY ../requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["/app/"]