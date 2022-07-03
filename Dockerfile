FROM python:3

COPY . /workspace

WORKDIR /workspace

RUN python3 -m pip install --upgrade pip

RUN apt-get update --no-install-recommends --yes

RUN pip3 install -r requirements.txt  

ENV PYTHONPATH "${PYTHONPATH}:/workspace"

CMD ["python3", "-m", "tronx"]
