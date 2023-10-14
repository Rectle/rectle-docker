FROM python:3.8-slim-buster

WORKDIR /app
COPY src src
RUN apt update
RUN pip install --no-cache-dir -r src/requirements.txt
CMD ["bash", "src/init.sh"]