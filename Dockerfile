FROM amd64/python:3.9-buster

WORKDIR /workspace/

COPY . /workspace/

RUN apt-get update --no-install-recommends --yes && \
    apt-get install -y ffmpeg --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "-u", "-m", "main"]
