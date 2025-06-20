#!/bin/bash

echo "🚀 Memulai proses instalasi Bot Telegram + API Hesda Store..."

# Update & install dependencies
sudo apt update && sudo apt install -y python3 python3-pip git

# Clone repo dari GitHub
if [ ! -d "bottele" ]; then
  git clone https://github.com/xyzval/bottele.git
fi

cd bottele || exit

# Install library Python
pip3 install -r requirements.txt

# Sisipkan token bot langsung
sed -i "s|TOKEN = 'YOUR_BOT_TOKEN'|TOKEN = '7571605934:AAHKtkmxvD2aNG9Jpwzw_2t46QDvIBMFUjo'|g" bot.py

# Jalankan bot pakai nohup agar aktif terus
echo "Menjalankan bot dengan nohup..."
nohup python3 bot.py > log.txt 2>&1 &

echo "✅ Bot dijalankan di background. Cek log dengan: tail -f log.txt"
