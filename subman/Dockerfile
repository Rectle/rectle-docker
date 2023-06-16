FROM python:3.8-slim-buster

WORKDIR /app
COPY src src
RUN apt update
RUN pip install -r src/requests
# ENTRYPOINT ["python", "src/main.py"]

# # for testing 
ENTRYPOINT ["tail", "-f", "/dev/null"]          