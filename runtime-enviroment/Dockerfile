FROM python:3.8-slim-buster

WORKDIR /app

COPY src src
COPY requirements.txt requirements.txt
RUN apt-get update -y && apt-get install -y \
    xvfb
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["src/start.sh"]
