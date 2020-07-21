FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y sox libsox-fmt-mp3
RUN pip install sox tqdm

WORKDIR /usr/src/app

COPY giantsteps-key-dataset/annotations/key/ annotations/
COPY *.py ./

CMD ["python", "main.py", "./audio/", "./annotations/", "0", "./generated/", "./generated/annotations/", "5"]
