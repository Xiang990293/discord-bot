#!/bin/bash

# Setting the yt-dlp first
yt-dlp --config-location /bot/yt-dlp.txt

# Start your Discord bot in the background
python bot.py

# Start your file server (adjust the port as needed)
# python temp_file/file_server.py

# Keep the container running
tail -f /dev/null