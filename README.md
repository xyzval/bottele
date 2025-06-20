# 🤖 Bot Telegram Jualan Kuota - Hesda Store API

Bot ini digunakan untuk jualan kuota (non-OTP) melalui Telegram dengan integrasi **API Hesda Store** dan fitur **Admin Panel langsung dari Telegram**.

---

## 🚀 Fitur Utama

- 🔌 Integrasi penuh dengan [https://api.hesda-store.com](https://api.hesda-store.com)
- 🛒 Tampilkan daftar paket kuota real-time
- 📤 Kirim pesanan otomatis ke API
- 💰 Cek saldo akun Hesda Store
- 🧑‍💼 Admin Panel di dalam bot Telegram
- 🪪 Admin dibatasi hanya oleh ID tertentu

---

## 📜 Perintah Bot

### Umum:
| Perintah   | Fungsi                          |
|------------|---------------------------------|
| `/start`   | Mulai bot & sambutan            |
| `/paket`   | Tampilkan 10 paket kuota        |

### Admin (hanya bisa digunakan oleh ID Telegram `5942781514`):
| Perintah             | Fungsi                             |
|----------------------|------------------------------------|
| `/admin`             | Menu admin                         |
| `/saldo`             | Menampilkan saldo akun Hesda Store|
| `/order <nohp> <kode>` | Kirim pesanan langsung ke API     |

---

## ⚙️ Cara Instalasi di VPS

### 1. Install dependency
```bash
sudo apt update
sudo apt install -y python3 python3-pip git
```

### 2. Clone dari GitHub
```bash
git clone https://github.com/xyzval/bottele.git
cd bottele
```

### 3. Install library Python
```bash
pip3 install -r requirements.txt
```

### 4. Jalankan bot 24 jam dengan `nohup`
```bash
nohup python3 bot.py > log.txt 2>&1 &
```

---

## 📌 Pengaturan

- Token bot dan API key sudah tertanam di `bot.py`
- Ganti admin ID jika perlu:
```python
ADMIN_IDS = [5942781514]
```

---

## 📞 Kontak
Dibuat oleh: **@username_kamu**  
Jika butuh bantuan setup atau fitur tambahan, silakan hubungi developer.
