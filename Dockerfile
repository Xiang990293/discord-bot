# these thing runs on main, not container.
FROM python:3.12
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot
RUN apt-get update && apt-get install -y ffmpeg libavcodec-extra libssl-dev libasound2
# RUN GO111MODULE=on go get -u github.com/DarthSim/overmind/v2
RUN pip install pipenv
RUN pip install -U https://github.com/coletdjnz/yt-dlp-youtube-oauth2/archive/refs/heads/master.zip
ADD Procfile /bot/
COPY start.sh /bot/
RUN chmod +x /bot/start.sh
RUN chmod +x /bot/bot.py
RUN chmod +x /bot/functions/file_server.py
# CMD ["overmind", "start"]
CMD python bot.py
# CMD start.sh