FROM python:3.11
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot
RUN apt add ffmpeg
CMD python bot.py