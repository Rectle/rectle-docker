FROM python:3.8-slim-buster

WORKDIR /app

COPY src src
COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# ENTRYPOINT ["python", "src/main.py"]

# # for testing
ENTRYPOINT ["tail", "-f", "/dev/null"]