FROM nikolaik/python-nodejs:python3.10-nodejs18

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app

RUN pc init

CMD ["pc", "run"]