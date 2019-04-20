FROM python:3

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY run.sh ./
COPY rpgame/. ./rpgame
COPY data/. ./data

RUN chmod +x ./run.sh

ENV PYTHON_PATH=.

CMD ["./run.sh"]