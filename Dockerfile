FROM python:3

RUN python3 -m venv .venv

RUN ./.venv/bin/activate

COPY . /workspace

WORKDIR /workspace

RUN apt-get update --no-install-recommends --yes

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt  

CMD ["python3", "-m", "tronx"]
