FROM amd64/python:3.9-buster

WORKDIR root/bin/

COPY . /workspace/

WORKDIR /workspace/

RUN apt-get update --no-install-recommends --yes

RUN apt-get install ffmpeg --no-install-recommends --yes

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt  

CMD ["python3", "-u", "-m", "main"]
