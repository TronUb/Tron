FROM python:3

COPY . /app

WORKDIR /app

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt  

CMD ["python3", "-m", "tronx"]
