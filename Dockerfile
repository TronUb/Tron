FROM python:3.10-slim-bullseye

COPY . /workspace

WORKDIR /workspace

RUN python3 -m pip install --upgrade pip

RUN apt-get update && apt-get install libpq-dev

RUN pip3 install -r requirements.txt  

ENV PYTHONPATH "${PYTHONPATH}:/workspace"

CMD ["python3", "-m", "tronx"]
