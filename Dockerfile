FROM python:3

COPY . /workspace

WORKDIR /workspace

RUN apt-get update --no-install-recommends --yes

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt  

CMD ["python3", "-u", "-m", "main"]
