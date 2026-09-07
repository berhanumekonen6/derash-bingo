import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# === የቻትቦት Token ===
BOT_TOKEN = "8976887607:AAHPLbIKWkSr0Yjbab_Ebhk6V--cRwNi4Eo"

# === ዋና ሜኑ ===
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🎯 Play Game", callback_data="play")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("💳 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("🆘 Support", callback_data="support")],
    ]
    return InlineKeyboardMarkup(keyboard)

# === /start ትዕዛዝ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🎱 እንኳን ወደ ደራሽ ቢንጎ ቻትቦት በደህና መጡ! 🎱

👇 ከታች ካሉት አማራጮች ይምረጡ:
"""
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu())

# === ቁልፍ ጫናዎችን መቀበል ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "play":
        text = """
🎯 ወደ ደራሽ ቢንጎ ጨዋታ ለመግባት እዚህ ይጫኑ 👇

🔗 https://tinyurl.com/u8ctbvr6

📌 ማስታወሻ:
✅ ተመዝግበው መግባት ያስፈልጋል
✅ ባላንስ ካለዎት ብቻ መጫወት ይችላሉ
✅ እስከ 2 ካርድ መምረጥ ይችላሉ

🎉 መልካም ጨዋታ!
"""
        await query.edit_message_text(text, reply_markup=get_main_menu())
    
    elif query.data == "balance":
        text = """
💰 የአሁኑ ባላንስዎ

👤 ተጫዋች: [ስም]
📊 ባላንስ: [ባላንስ] ETB
🏆 ድሎች: [ቁጥር]
🎮 የተጫወቱት: [ቁጥር] ጨዋታዎች

━━━━━━━━━━━━━━━━━━━
💳 ባላንስ ለመጨመር "Deposit" ይጫኑ
💸 ገንዘብ ለማውጣት "Withdraw" ይጫኑ
━━━━━━━━━━━━━━━━━━━
"""
        await query.edit_message_text(text, reply_markup=get_main_menu())
    
    elif query.data == "deposit":
        text = """
💰 ባላንስ ለመጨመር:

📞 ቴሌብር ቁጥር: 0905527481

📝 ደረጃዎች:
1️⃣ በቴሌብር 0905527481 ላይ ገንዘብ ያስተላልፉ
2️⃣ የክፍያ ማረጋገጫ (ስክሪንሾት) ይላኩልኝ
3️⃣ ባላንስዎ በራስ-ሰር ይዘምናል
4️⃣ ከዚያ በኋላ መጫወት ይችላሉ! 🎰

💳 የክፍያ መጠኖች:
20 | 50 | 100 | 200 | 300 | 500 | 1000 ETB

📸 ማረጋገጫውን እዚህ ይላኩ 👇
"""
        await query.edit_message_text(text, reply_markup=get_main_menu())
    
    elif query.data == "support":
        text = """
🆘 እንዴት ልረዳዎት እችላለሁ?

📋 የተለመዱ ጥያቄዎች:
━━━━━━━━━━━━━━━━━━━
❓ እንዴት መመዝገብ እንደሚቻል?
❓ እንዴት መጫወት እንደሚቻል?
❓ እንዴት ባላንስ መጨመር እንደሚቻል?
❓ እንዴት ገንዘብ ማውጣት እንደሚቻል?
━━━━━━━━━━━━━━━━━━━

👤 አስተዳዳሪ: @[የአስተዳዳሪ ስም]
📞 ስልክ: 0905527481

💬 ጥያቄዎን ይጠይቁኝ! 😊
"""
        await query.edit_message_text(text, reply_markup=get_main_menu())

# === ቻትቦት ማስኬድ ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ ቻትቦት ተጀምሯል! በቴሌግራም ላይ /start ይላኩ...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
