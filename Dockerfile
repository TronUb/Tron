FROM amd64/python:3.9-buster

WORKDIR root/bin/

COPY . /workspace/

WORKDIR /workspace/

RUN apt-get update --no-install-recommends --yes

RUN python3 -m pip install --upgrade pip

RUN \
  apt-get update --no-install-recommends --yes && apt-get upgrade --no-install-recommends --yes && \
  apt-get install wget curl --no-install-recommends --yes && \
  echo "deb https://deb.nodesource.com/node_17.x buster main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
  wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  apt-get update && apt-get upgrade && \
  apt-get install -yqq nodejs yarn && \
  pip install -U pip && pip install pipenv && \
  npm i -g npm@8.19.1 && \
  curl -sSL https://install.python-poetry.org | python3 - && ln -s /root/.poetry/bin/poetry /usr/local/bin && \
  rm -rf /var/lib/apt/lists/*

RUN bash install_ffmpeg.sh

RUN pip3 install -r requirements.txt  

CMD ["python3", "-u", "-m", "main"]
