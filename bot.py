from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests, json, os

TOKEN = "7571605934:AAHKtkmxvD2aNG9Jpwzw_2t46QDvIBMFUjo"
API_KEY = "Fv2dN2rKpjSPDDyBaX"
AUTH = ("r8149762@gmail.com", "Lugoblok@1")
SALDO_FILE = "saldos.json"

if not os.path.exists(SALDO_FILE):
    with open(SALDO_FILE, "w") as f:
        json.dump({}, f)

def load_saldo():
    with open(SALDO_FILE) as f:
        return json.load(f)

def save_saldo(data):
    with open(SALDO_FILE, "w") as f:
        json.dump(data, f)

def potong_saldo(user_id, jumlah):
    user_id = str(user_id)
    data = load_saldo()
    if data.get(user_id, 0) >= jumlah:
        data[user_id] -= jumlah
        save_saldo(data)
        return True
    return False

def ambil_paket_xl():
    url = "https://api.hesda-store.com/v2/list_paket"
    params = {'hesdastore': API_KEY, 'jenis': 'nonotp'}
    try:
        res = requests.get(url, params=params, auth=AUTH)
        data = res.json()
        if data.get("status"):
            return [p for p in data["data"] if "xl" in p['package_name_show'].lower()]
    except:
        pass
    return []

async def paket_xl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produk = ambil_paket_xl()
    if not produk:
        await update.message.reply_text("❌ Gagal ambil paket XL.")
        return

    for p in produk[:15]:
        nama = p["package_name_show"]
        harga = int(p["harga"])
        kode = p["package_id"]
        btn = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"Beli - Rp {harga:,}", callback_data=f"beli|{kode}|{harga}")]
        ])
        await update.message.reply_text(
            f"*{nama}*
Harga: Rp {harga:,}
Kode: `{kode}`",
            reply_markup=btn,
            parse_mode="Markdown"
        )

async def handle_beli(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    _, kode, harga = query.data.split("|")
    harga = int(harga)

    if not potong_saldo(user_id, harga):
        await query.edit_message_text("❌ Saldo kamu tidak cukup.")
        return

    url = "https://api.hesda-store.com/v2/order"
    data = {
        "hesdastore": API_KEY,
        "target": "08xxxxxxxx",
        "package_id": kode
    }
    res = requests.post(url, data=data, auth=AUTH).json()
    if res.get("status"):
        await query.edit_message_text(f"✅ Order berhasil!
ID Transaksi: {res['data']['trxid']}")
    else:
        await query.edit_message_text(f"❌ Gagal order: {res.get('msg')}")

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    saldo = load_saldo().get(user_id, 0)
    await update.message.reply_text(f"💰 Saldo kamu: Rp {saldo:,}")



async def addsaldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        uid = context.args[0]
        jumlah = int(context.args[1])

        if jumlah < 15000:
            await update.message.reply_text("❌ Minimal top-up adalah Rp 15.000")
            return

        data = load_saldo()
        data[uid] = data.get(uid, 0) + jumlah
        save_saldo(data)
        await update.message.reply_text(f"✅ Tambah saldo Rp {jumlah:,} ke ID {uid}")

        try:
            await context.bot.send_message(
                chat_id=int(uid),
                text=f"💰 Saldo kamu telah ditambahkan: Rp {jumlah:,}"
            )
        except:
            pass

    except:
        await update.message.reply_text("❌ Format: /addsaldo <user_id> <jumlah>")
