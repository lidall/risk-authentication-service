FROM python:3.8-alpine

RUN apk add --update \
    py-pip \
    curl

COPY . /tmp/risk-authentication-service
WORKDIR /tmp/risk-authentication-service

RUN pip install -r requirements.txt
RUN pip install .

EXPOSE 8080

CMD ["python3", "-u", "./main.py"]