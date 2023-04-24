FROM python:3.10-alpine

RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers libffi-dev openssl-dev

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/
ADD . /var/www/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh
USER www

EXPOSE 5000

CMD ["python", "app.py"]
