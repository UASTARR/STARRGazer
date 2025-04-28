#!/bin/sh

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Update the package list and install Nginx with RTMP module and FFmpeg
apt update

# Check if update was successful
if [ $? -ne 0 ]; then
    echo "Failed to update package list. Please check your network connection."
    exit 1
fi

# Install Nginx with RTMP module and FFmpeg
apt install \
    nginx \
    libnginx-mod-rtmp \
    ffmpeg
