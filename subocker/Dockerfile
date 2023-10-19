FROM python:3.8-slim-buster

WORKDIR /app

COPY src src
RUN pip install --upgrade pip
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r src/requirements.txt
CMD ["python", "-u", "src/main.py"]