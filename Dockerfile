FROM python:3.11
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot
RUN apt-get update && apt-get install -y ffmpeg libavcodec-extra libssl-dev libasound2
RUN pip install pipenv
EXPOSE 443 8080
CMD python bot.py