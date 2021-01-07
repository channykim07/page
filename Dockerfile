FROM python:3.8

ARG GIT
ARG OAUTH
ARG SERVICE_ACCOUNT
ARG PORT=8080
ARG TEST=false

ENV PORT=${PORT} \
  PYTHONPATH=/page \
  GIT=${GIT} \
  OAUTH=${OAUTH} \
  SERVICE_ACCOUNT=${SERVICE_ACCOUNT}

COPY page/ /page

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
  apt-get -y update && \
  apt-get install -y google-chrome-stable && \
  pip install -r page/requirements.txt

RUN if [ "$TEST" = true ] ; then \
  python -m page.test; \
  else \
  python -m page.api.student && \
  python -m page.api.problem && \
  python -m page.api.doc && \
  python -m page.api.gist; \
  fi

CMD gunicorn --bind :$PORT --workers 1 --threads 8 "page.app:deployment()";
