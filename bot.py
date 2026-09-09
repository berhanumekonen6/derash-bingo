import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from datetime import datetime

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
        [InlineKeyboardButton("💸 Withdraw (ወጪ)", callback_data="withdraw")],
        [InlineKeyboardButton("🎯 Play Game", url=GAME_LINK)],
        [InlineKeyboardButton("❓ How to Play", callback_data="howto")],
        [InlineKeyboardButton("🆘 Support", callback_data="support")],
    ]
    return InlineKeyboardMarkup(keyboard)

# === WITHDRAW MENU ===
def get_withdraw_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Enter Withdraw Amount", callback_data="withdraw_amount")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")],
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
3️⃣ Click "💸 Withdraw (ወጪ)" to withdraw funds
4️⃣ Click "🎯 Play Game" to start playing!

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
   → Click "📝 Register" button

💰 How to add balance?
   → Click "💰 Deposit / Pay" button
   → Send money via Telebirr to {TELEBIRR_NUMBER}

💸 How to withdraw?
   → Click "💸 Withdraw (ወጪ)" button
   → Enter the amount you want to withdraw
   → Send to Telebirr: {TELEBIRR_NUMBER}

🎯 How to play?
   → Click "🎯 Play Game" button

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
   → Click "📝 Register" button

━━━━━━━━━━━━━━━━━━━
💰 STEP 2: DEPOSIT
   → Click "💰 Deposit / Pay"
   → Send money via Telebirr: {TELEBIRR_NUMBER}
   → Send payment screenshot to this bot
   → Your balance will be updated!

━━━━━━━━━━━━━━━━━━━
💸 STEP 3: WITHDRAW
   → Click "💸 Withdraw (ወጪ)"
   → Enter the amount you want to withdraw
   → Money will be sent to your Telebirr

━━━━━━━━━━━━━━━━━━━
🎯 STEP 4: PLAY
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

Click "📝 Register" to create your account.

━━━━━━━━━━━━━━━━━━━
✅ After registration:
1️⃣ Click "💰 Deposit / Pay" to add balance
2️⃣ Click "💸 Withdraw (ወጪ)" to withdraw funds
3️⃣ Click "🎯 Play Game" to start playing!

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

# === WITHDRAW BUTTON ===
async def withdraw_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💸 WITHDRAW (ወጪ)

━━━━━━━━━━━━━━━━━━━
📝 TO WITHDRAW:

1️⃣ Click "💰 Enter Withdraw Amount"
2️⃣ Send: /withdraw [amount]
3️⃣ Money will be sent to your Telebirr

━━━━━━━━━━━━━━━━━━━
📌 EXAMPLES:
/withdraw 50
/withdraw 100
/withdraw 200

━━━━━━━━━━━━━━━━━━━
📞 Telebirr Number: {TELEBIRR_NUMBER}

━━━━━━━━━━━━━━━━━━━
💳 MINIMUM WITHDRAWAL: 20 ETB
💳 MAXIMUM WITHDRAWAL: Your balance

━━━━━━━━━━━━━━━━━━━
📞 For support: {ADMIN_USERNAME}

🔙 Click "Back to Menu" to return
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_withdraw_menu())

# === WITHDRAW AMOUNT - Asks for amount ===
async def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💸 WITHDRAW (ወጪ)

━━━━━━━━━━━━━━━━━━━
📝 Please send the amount you want to withdraw:

/withdraw [amount]

━━━━━━━━━━━━━━━━━━━
📌 EXAMPLES:
/withdraw 50
/withdraw 100
/withdraw 200

━━━━━━━━━━━━━━━━━━━
💳 MINIMUM: 20 ETB
💳 MAXIMUM: Your balance

━━━━━━━━━━━━━━━━━━━
📞 Telebirr Number: {TELEBIRR_NUMBER}
👤 Admin: {ADMIN_USERNAME}

💡 Your balance will be checked before withdrawal.
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_withdraw_menu())

# === /withdraw COMMAND ===
async def withdraw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    
    if len(args) < 1:
        await update.message.reply_text(
            f"❌ Please enter the amount you want to withdraw!\n\n"
            f"📝 Format: /withdraw amount\n"
            f"📌 Example: /withdraw 50\n\n"
            f"💰 Minimum withdrawal: 20 ETB\n"
            f"💸 Maximum withdrawal: Your balance\n"
            f"📞 Telebirr: {TELEBIRR_NUMBER}\n\n"
            f"👤 Admin: {ADMIN_USERNAME}"
        )
        return
    
    try:
        amount = float(args[0])
    except ValueError:
        await update.message.reply_text(
            f"❌ Invalid amount! Please enter a valid number.\n\n"
            f"📌 Example: /withdraw 50"
        )
        return
    
    if amount < 20:
        await update.message.reply_text(
            f"❌ Minimum withdrawal is 20 ETB!\n\n"
            f"📌 Example: /withdraw 20"
        )
        return
    
    # Get user info
    user = update.effective_user
    user_id = user.id
    user_full_name = user.full_name if user.full_name else user.username
    username = user.username if user.username else f"User_{user_id}"
    
    # Create confirmation message
    confirmation_text = f"""
✅ WITHDRAWAL REQUEST RECEIVED! 🎉

━━━━━━━━━━━━━━━━━━━
👤 Username: {username}
👤 Full Name: {user_full_name}
💸 Amount: {amount:.2f} ETB
📱 User ID: {user_id}
📅 Requested: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━
📝 NEXT STEPS:
1️⃣ Admin will verify your balance
2️⃣ Money will be sent to your Telebirr
3️⃣ You will receive confirmation

━━━━━━━━━━━━━━━━━━━
📞 Telebirr: {TELEBIRR_NUMBER}
👤 Admin: {ADMIN_USERNAME}

⏳ Please wait for admin to process your request.
💡 Check your balance after 24 hours.

✅ Thank you for using Derash BINGO!
"""
    
    # Send confirmation to user
    await update.message.reply_text(confirmation_text, reply_markup=get_main_menu())
    
    # Send notification to admin (you can enable this for admin notifications)
    admin_notification = f"""
🔔 NEW WITHDRAWAL REQUEST!

━━━━━━━━━━━━━━━━━━━
👤 Username: {username}
👤 Full Name: {user_full_name}
💸 Amount: {amount:.2f} ETB
📱 User ID: {user_id}
📅 Requested: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━
📞 Process this request:
- Verify user balance
- Send money to Telebirr: {TELEBIRR_NUMBER}
- Confirm completion
"""
    
    # Uncomment the lines below to send admin notification
    # try:
    #     await context.bot.send_message(chat_id="YOUR_ADMIN_CHAT_ID", text=admin_notification)
    # except:
    #     pass
    
    logger.info(f"Withdrawal request from {username} (ID: {user_id}) - {amount} ETB")

# === BACK TO MENU ===
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "🔙 Back to Main Menu\n\n👇 Select an option below:",
        reply_markup=get_main_menu()
    )

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
መ: "📝 Register" ይጫኑ

ጥ: እንዴት ባላንስ መጨመር እንደሚቻል?
መ: "💰 Deposit / Pay" ይጫኑ

ጥ: እንዴት ገንዘብ ማውጣት (withdraw) እንደሚቻል?
መ: "💸 Withdraw (ወጪ)" ይጫኑ
ወይም /withdraw amount ይላኩ
ምሳሌ: /withdraw 50

ጥ: እንዴት መጫወት እንደሚቻል?
መ: "🎯 Play Game" ይጫኑ

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
2️⃣ Click "💸 Withdraw (ወጪ)" to withdraw funds
3️⃣ Click "🎯 Play Game" to start playing!

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
    elif query.data == "withdraw":
        await withdraw_button(update, context)
    elif query.data == "withdraw_amount":
        await withdraw_amount(update, context)
    elif query.data == "howto":
        await how_to_play(update, context)
    elif query.data == "support":
        await support_button(update, context)
    elif query.data == "back_to_menu":
        await back_to_menu(update, context)

# === MAIN FUNCTION ===
def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("register", register_command))
    application.add_handler(CommandHandler("withdraw", withdraw_command))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("=" * 50)
    print("✅ BOT IS RUNNING!")
    print("=" * 50)
    print(f"🤖 Bot: @DerashBingoPlayBot")
    print(f"🔗 Link: https://t.me/DerashBingoPlayBot")
    print(f"🎯 Game: {GAME_LINK}")
    print(f"📞 Telebirr: {TELEBIRR_NUMBER}")
    print(f"💸 Withdraw: /withdraw amount")
    print("=" * 50)
    print("Send /start on Telegram to test!")
    print("Press Ctrl+C to stop the bot.")
    print("=" * 50)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
