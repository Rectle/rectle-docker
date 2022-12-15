FROM alpine:3

LABEL maintainer="Rectle"

# Copy source files
COPY . .

# Install python
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Install docker
RUN apk add docker docker-compose docker-cli-compose

# Install dependencies
RUN pip3 install --no-cache-dir -r subocker/requirements.txt

# Run
CMD ["python","-u", "subocker/main.py"]