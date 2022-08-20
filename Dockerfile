FROM python:3

RUN python3 -m venv root

WORKDIR root/bin/

RUN chmod +x activate

RUN . ./activate

COPY . /workspace

WORKDIR /workspace

RUN apt-get update --no-install-recommends --yes

RUN apt-get install nodejs==15.0.0 --no-install-recommends --yes

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt  

CMD ["python3", "-u", "-m", "main"]
