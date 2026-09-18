#!/bin/bash
echo "[*] Updating Termux and installing dependencies..."
pkg update -y && pkg upgrade -y
pkg install python git ffmpeg -y

echo "[*] Installing Python libraries..."
pip install -r requirements.txt

echo "[*] Setting up 'fbtools' command..."
echo "alias fbtools='python $(pwd)/main.py'" >> ~/.bashrc
source ~/.bashrc

echo "[+] Setup Complete! Type 'fbtools' to launch the app."
