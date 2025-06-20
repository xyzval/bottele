# Telegram Bot Jualan

Bot Telegram untuk jualan kuota.

## Cara Jalankan

1. Edit file `bot.py`, ganti `YOUR_BOT_TOKEN` dengan token dari @BotFather.
2. Install dependency:
```
pip install -r requirements.txt
```
3. Jalankan bot:
```
python bot.py
```

## Install di VPS

Jalankan perintah berikut di VPS:

```
sudo apt update
sudo apt install -y python3 python3-pip git
git clone https://github.com/xyzval/bottele.git
cd bottele
pip3 install -r requirements.txt
nohup python3 bot.py &
```
