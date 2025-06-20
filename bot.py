from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TOKEN = '7571605934:AAHKtkmxvD2aNG9Jpwzw_2t46QDvIBMFUjo'
API_KEY = 'Fv2dN2rKpjSPDDyBaX'
ADMIN_IDS = [5942781514]

AUTH = ('r8149762@gmail.com', 'Lugoblok@1')

def get_list_paket():
    try:
        url = 'https://api.hesda-store.com/v2/list_paket'
        params = {'hesdastore': API_KEY, 'jenis': 'nonotp'}
        response = requests.get(url, params=params, auth=AUTH)
        data = response.json()
        if data.get('status'):
            return data['data']
    except Exception as e:
        print("PAKET ERROR:", e)
    return []

def cek_saldo():
    try:
        url = 'https://api.hesda-store.com/v2/saldo'
        params = {'hesdastore': API_KEY}
        response = requests.get(url, params=params, auth=AUTH)
        data = response.json()
        if data.get('status'):
            return data['data']['saldo']
    except Exception as e:
        print("SALDO ERROR:", e)
    return None

def order_kuota(nohp, kode):
    try:
        url = 'https://api.hesda-store.com/v2/order'
        data = {
            'hesdastore': API_KEY,
            'target': nohp,
            'package_id': kode
        }
        res = requests.post(url, data=data, auth=AUTH)
        return res.json()
    except Exception as e:
        print("ORDER ERROR:", e)
        return {"status": False, "msg": "Terjadi kesalahan saat memesan."}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selamat datang! Gunakan /paket untuk lihat paket.")

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    paket_list = get_list_paket()
    if not paket_list:
        await update.message.reply_text("❌ Gagal ambil paket dari API.")
        return

    message = "📦 *Daftar Paket Kuota:*\n"
    for p in paket_list[:10]:
        message += f"\n• *{p['package_name_show']}*\nHarga: {p['harga']}\nKode: `{p['package_id']}`\n"

    await update.message.reply_text(message, parse_mode='Markdown')

async def show_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    saldo = cek_saldo()
    if saldo is not None:
        await update.message.reply_text(f"💰 Saldo kamu saat ini: Rp {saldo:,}")
    else:
        await update.message.reply_text("❌ Gagal ambil saldo.")

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    message = (
        "👮 *Admin Menu:*\n"
        "1. /saldo - Cek saldo\n"
        "2. /paket - Lihat produk\n"
        "3. /order <nohp> <kode> - Kirim pesanan\n"
    )
    await update.message.reply_text(message, parse_mode='Markdown')

async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    try:
        _, nohp, kode = update.message.text.split()
        result = order_kuota(nohp, kode)
        if result["status"]:
            await update.message.reply_text(f"✅ Order berhasil!\nTransaksi ID: {result['data']['trxid']}")
        else:
            await update.message.reply_text(f"❌ Gagal: {result['msg']}")
    except:
        await update.message.reply_text("❌ Format salah. Gunakan: /order 08xxxxxxx KODE")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin_menu))
app.add_handler(CommandHandler("saldo", show_saldo))
app.add_handler(CommandHandler("paket", show_products))
app.add_handler(CommandHandler("order", handle_order))

if __name__ == '__main__':
    app.run_polling()
