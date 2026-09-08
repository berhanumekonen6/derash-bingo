import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === YOUR BOT INFORMATION ===
BOT_TOKEN = "8976887607:AAHPLbIKWkSr0Yjbab_Ebhk6V--cRwNi4Eo"
GAME_LINK = "https://tinyurl.com/u8ctbvr6"
TELEBIRR_NUMBER = "0905527481"
ADMIN_USERNAME = "@berhanumekonen6"

# === MAIN MENU ===
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📝 Register", callback_data="register")],
        [InlineKeyboardButton("💰 Deposit / Pay", callback_data="deposit")],
        [InlineKeyboardButton("🎯 Play Game", url=GAME_LINK)],  # Opens directly!
        [InlineKeyboardButton("❓ How to Play", callback_data="howto")],
        [InlineKeyboardButton("🆘 Support", callback_data="support")],
    ]
    return InlineKeyboardMarkup(keyboard)

# === /start COMMAND ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"""
🎱 Welcome to Derash BINGO {user.first_name}! 🎱

⭐ To Play Derash BINGO:
━━━━━━━━━━━━━━━━━━━
1️⃣ Click "📝 Register" to create account
2️⃣ Click "💰 Deposit / Pay" to add balance
3️⃣ Click "🎯 Play Game" to start playing!

💰 Prize: 8 ETB per card
📞 Telebirr: {TELEBIRR_NUMBER}

👇 Select an option below:
"""
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu())

# === /help COMMAND ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = f"""
❓ How can I help you?

📋 FAQ:
━━━━━━━━━━━━━━━━━━━
📝 How to register?
   → Send: /register username FullName Phone Password
   Example: /register john "John Doe" 0912345678 mypass

💰 How to add balance?
   → Send money via Telebirr to {TELEBIRR_NUMBER}
   → Send payment screenshot to this bot

🎯 How to play?
   → After registering and depositing, click "Play Game"

🆘 Need more help?
   → Click "Support" or contact {ADMIN_USERNAME}
━━━━━━━━━━━━━━━━━━━
"""
    await update.message.reply_text(help_text)

# === HOW TO PLAY ===
async def how_to_play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
🎯 HOW TO PLAY DERASH BINGO

━━━━━━━━━━━━━━━━━━━
📝 STEP 1: REGISTER
   → Click "Register" or send:
   /register username FullName Phone Password

━━━━━━━━━━━━━━━━━━━
💰 STEP 2: DEPOSIT
   → Click "Deposit / Pay"
   → Send money via Telebirr: {TELEBIRR_NUMBER}
   → Send payment screenshot to this bot
   → Your balance will be updated!

━━━━━━━━━━━━━━━━━━━
🎯 STEP 3: PLAY
   → Click "🎯 Play Game" to start playing!
   → Login with your username and password
   → Select 1-2 cards (10 ETB each)
   → Wait for numbers to be called
   → Get BINGO and WIN! 🎉

━━━━━━━━━━━━━━━━━━━
📌 RULES:
✅ Max 2 cards per player
✅ Card price: 10 ETB
✅ Prize: 8 ETB per card
✅ 201 cards available
✅ Auto-call every 2 seconds

🔗 PLAY NOW: {GAME_LINK}
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_main_menu())

# === REGISTER BUTTON ===
async def register_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
📝 REGISTER TO PLAY

To register, send this command:

/register username FullName Phone Password

━━━━━━━━━━━━━━━━━━━
📌 EXAMPLE:
/register john "John Doe" 0912345678 mypassword

━━━━━━━━━━━━━━━━━━━
✅ After registration:
1️⃣ Click "💰 Deposit / Pay" to add balance
2️⃣ Click "🎯 Play Game" to start playing!

🔗 GAME LINK: {GAME_LINK}
📞 Telebirr: {TELEBIRR_NUMBER}
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_main_menu())

# === DEPOSIT BUTTON ===
async def deposit_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💰 HOW TO DEPOSIT / PAY

━━━━━━━━━━━━━━━━━━━
📞 Telebirr Number: {TELEBIRR_NUMBER}

📝 STEPS:
1️⃣ Open Telebirr on your phone
2️⃣ Send money to {TELEBIRR_NUMBER}
3️⃣ Write your username in the memo
4️⃣ Take a screenshot of the payment
5️⃣ Send the screenshot to this bot
6️⃣ Your balance will be updated!

━━━━━━━━━━━━━━━━━━━
💳 PAYMENT AMOUNTS:
20 ETB  |  50 ETB  |  100 ETB
200 ETB |  300 ETB |  500 ETB
1000 ETB

━━━━━━━━━━━━━━━━━━━
📸 After payment, send screenshot here:
👉 @DerashBingoPlayBot
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_main_menu())

# === SUPPORT BUTTON - AMHARIC ===
async def support_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
🆘 ምን እናግዘዎ!?

━━━━━━━━━━━━━━━━━━━
📞 ቴሌብር: {TELEBIRR_NUMBER}
🤖 ቻትቦት: @DerashBingoPlayBot
🎯 ጨዋታ: {GAME_LINK}

━━━━━━━━━━━━━━━━━━━
❓ ተዘውትረው የሚጠየቁ ጥያቄዎች:

ጥ: እንዴት መመዝገብ እንደሚቻል?
መ: /register username FullName Phone Password ይላኩ

ጥ: እንዴት ባላንስ መጨመር እንደሚቻል?
መ: በቴሌብር ወደ {TELEBIRR_NUMBER} ገንዘብ ያስተላልፉ

ጥ: እንዴት መጫወት እንደሚቻል?
መ: ከተመዘገቡ እና ባላንስ ከጨመሩ በኋላ "Play Game" ይጫኑ

ጥ: መግባት አልቻልኩም?
መ: መጀመሪያ መመዝገብዎን ያረጋግጡ!

ጥ: ባላንሴ አልታየም?
መ: የክፍያ ማረጋገጫዎን ለዚህ ቻትቦት ይላኩ

━━━━━━━━━━━━━━━━━━━
👤 አስተዳዳሪ: {ADMIN_USERNAME}
📞 ስልክ: {TELEBIRR_NUMBER}

💬 ጥያቄዎን እዚህ ይጠይቁ! 😊
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_main_menu())

# === /register COMMAND ===
async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 4:
        await update.message.reply_text(
            f"❌ Please provide all required information!\n\n"
            f"📝 Format: /register username FullName Phone Password\n"
            f"📌 Example: /register john 'John Doe' 0912345678 mypassword\n\n"
            f"💰 After registration, deposit to get balance!\n"
            f"📞 Telebirr: {TELEBIRR_NUMBER}"
        )
        return
    
    if len(args) >= 5:
        username = args[0]
        full_name = " ".join(args[1:-2])
        phone = args[-2]
        password = args[-1]
    else:
        username = args[0]
        full_name = args[1]
        phone = args[2]
        password = args[3]
    
    await update.message.reply_text(
        f"""
✅ REGISTRATION SUCCESSFUL! 🎉

━━━━━━━━━━━━━━━━━━━
👤 Username: {username}
👤 Full Name: {full_name}
📱 Phone: {phone}

━━━━━━━━━━━━━━━━━━━
🎯 NEXT STEPS:
1️⃣ Click "💰 Deposit / Pay" to add balance
2️⃣ Click "🎯 Play Game" to start playing!

🔗 GAME LINK: {GAME_LINK}
💰 Telebirr: {TELEBIRR_NUMBER}

🎉 Welcome to Derash BINGO! 🎉
""",
        reply_markup=get_main_menu()
    )

# === BUTTON HANDLER ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "register":
        await register_button(update, context)
    elif query.data == "deposit":
        await deposit_button(update, context)
    elif query.data == "howto":
        await how_to_play(update, context)
    elif query.data == "support":
        await support_button(update, context)

# === MAIN FUNCTION ===
def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("register", register_command))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("=" * 50)
    print("✅ BOT IS RUNNING!")
    print("=" * 50)
    print(f"🤖 Bot: @DerashBingoPlayBot")
    print(f"🔗 Link: https://t.me/DerashBingoPlayBot")
    print(f"🎯 Game: {GAME_LINK}")
    print(f"📞 Telebirr: {TELEBIRR_NUMBER}")
    print("=" * 50)
    print("Send /start on Telegram to test!")
    print("Press Ctrl+C to stop the bot.")
    print("=" * 50)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
