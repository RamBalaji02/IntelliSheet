#!/bin/bash
# Install system dependencies
apt-get update
apt-get install -y portaudio19-dev python3-pyaudio

# Install Python dependencies
pip install -r requirements.txt
