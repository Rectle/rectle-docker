FROM python:3.8-slim-buster

WORKDIR /app
COPY src/requirements.txt requirements.txt
RUN apt update
RUN pip install --no-cache-dir -r requirements.txt
COPY src src
CMD ["python", "-u", "src/main.py"]