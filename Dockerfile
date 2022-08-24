FROM amd64/python:3.9-buster

WORKDIR root/bin/

COPY . /workspace

WORKDIR /workspace

RUN \
    apt-get update --no-install-recommends --yes && \
    echo "deb https://deb.nodesource.com/node_17.x buster main" > /etc/apt/sources.list.d/nodesource.list && \
    wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    apt-get install -yqq nodejs && apt-get install -y ffmpeg

RUN pip3 install -r requirements.txt  

CMD ["python3", "-u", "-m", "main"]
