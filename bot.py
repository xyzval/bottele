from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '7571605934:AAHKtkmxvD2aNG9Jpwzw_2t46QDvIBMFUjo'

product_list = {
    "Kuota 10GB": 15000,
    "Kuota 20GB": 25000
}

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

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order))

if __name__ == '__main__':
    app.run_polling()
