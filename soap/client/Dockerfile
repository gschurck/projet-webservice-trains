FROM nikolaik/python-nodejs:python3.10-nodejs18

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app

WORKDIR /test
RUN pc init
WORKDIR /
RUN rm -rf /test

WORKDIR /app

CMD ["pc", "run"]