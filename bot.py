from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TOKEN = '7571605934:AAHKtkmxvD2aNG9Jpwzw_2t46QDvIBMFUjo'
API_KEY = 'Fv2dN2rKpjSPDDyBaX'

product_list = {
    "Kuota 10GB": 15000,
    "Kuota 20GB": 25000
}

def get_list_paket():
    url = 'https://api.hesda-store.com/v2/list_paket'
    params = {'hesdastore': API_KEY, 'jenis': 'nonotp'}
    response = requests.get(url, params=params)
    data = response.json()
    if data['status']:
        return data['data']
    return []

def cek_saldo():
    url = 'https://api.hesda-store.com/v2/saldo'
    params = {'hesdastore': API_KEY}
    res = requests.get(url, params=params)
    data = res.json()
    if data['status']:
        return data['data']['saldo']
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    keyboard = [[p] for p in product_list.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(f"Halo {user}! Silakan pilih produk:", reply_markup=reply_markup)

async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = update.message.text
    if item in product_list:
        price = product_list[item]
        await update.message.reply_text(f"Kamu memilih: {item}\nHarga: Rp{price}\nSilakan transfer ke 08xxxxxxxx dan kirim bukti pembayaran.")
    else:
        await update.message.reply_text("Produk tidak dikenali.")

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    paket_list = get_list_paket()
    if not paket_list:
        await update.message.reply_text("Gagal ambil paket dari API.")
        return

    message = "📦 *Daftar Paket Kuota:*
"
    for p in paket_list[:10]:
        message += f"\n• *{p['package_name_show']}*\nHarga: {p['harga']}\nKode: `{p['package_id']}`\n"

    await update.message.reply_text(message, parse_mode='Markdown')

async def show_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    saldo = cek_saldo()
    if saldo is not None:
        await update.message.reply_text(f"💰 Saldo kamu saat ini: Rp {saldo:,}")
    else:
        await update.message.reply_text("❌ Gagal ambil saldo.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("paket", show_products))
app.add_handler(CommandHandler("saldo", show_saldo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order))

if __name__ == '__main__':
    app.run_polling()
