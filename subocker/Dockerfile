FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt update
RUN apt-get install -y git
RUN pip install --upgrade pip
COPY src src
RUN mkdir temp
RUN pip install --no-cache-dir -r src/requirements.txt
RUN git clone -b parameters https://github.com/Rectle/rectle-library.git src/rectle_lib

CMD ["python", "-u", "src/main.py"]
# CMD ["sleep", "9999999"]
