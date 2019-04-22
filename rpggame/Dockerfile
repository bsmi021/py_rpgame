FROM python:3

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY rpgame/main.py ./
COPY run.sh ./
COPY rpgame/. ./rpgame
COPY rpgame/data ./data

RUN chmod +x ./run.sh

ENV PYTHONPATH=.

CMD ["./run.sh"]