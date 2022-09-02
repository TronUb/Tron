echo "deb https://deb.nodesource.com/node_17.x buster main" > /etc/apt/sources.list.d/nodesource.list && \
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key --no-install-recommends --yes | apt-key add - && \
  apt update --no-install-recommends --yes && apt upgrade --no-install-recommends --yes && \
  apt install wget curl --no-install-recommends --yes && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
  wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  apt-get update --no-install-recommends --yes && \
  apt-get install -yqq nodejs yarn --no-install-recommends --yes && \
  pip install -U pip && pip install pipenv && \
  npm i -g npm@^8 && \
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && ln -s /root/.poetry/bin/poetry /usr/local/bin && \
  rm -rf /var/lib/apt/lists/*
