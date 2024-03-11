#!/bin/bash

# Start your Discord bot in the background
python bot.py

# Start your file server (adjust the port as needed)
python file_server.py

# Keep the container running
tail -f /dev/null