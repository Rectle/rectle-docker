FROM alpine:3

RUN apk update && \
    apk add --no-cache bash git openssh

WORKDIR /app

CMD ["./storage.sh"]