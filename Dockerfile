FROM python:3.11

WORKDIR /app

# TODO: Add bufferizing
COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]



