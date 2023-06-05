FROM python:3.8-slim-buster

WORKDIR /app
COPY src src
ENTRYPOINT ["python", "src/main.py"]

# for testing
# ENTRYPOINT ["tail", "-f", "/dev/null"]          