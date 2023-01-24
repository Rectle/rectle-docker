FROM python:3.8-slim-buster

WORKDIR /app

COPY src src
COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN sed -i -e 's/\r$//' src/start.sh
ENTRYPOINT ["bash", "src/start.sh"]