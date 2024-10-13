FROM python:3.11

WORKDIR /app

ENV TZ=Asia/Omsk

# Install the tzdata package to configure the timezone
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]



