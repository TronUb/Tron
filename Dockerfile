FROM python:3.10-slim-bullseye

WORKDIR root/bin/

COPY . /workspace/

WORKDIR /workspace/

RUN apt-get update --no-install-recommends --yes

RUN python3 -m pip install --upgrade pip

RUN bash install_nodejs.sh

RUN apt-get update && apt install -y ffmpeg

RUN pip3 install -r requirements.txt  

CMD ["python3", "-u", "-m", "main"]
