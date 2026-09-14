import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters, ConversationHandler
)
from datetime import datetime, timezone

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === YOUR BOT INFORMATION ===
BOT_TOKEN = "8976887607:AAHPLbIKWkSr0Yjbab_Ebhk6V--cRwNi4Eo"
GAME_LINK = "https://tinyurl.com/4n6vkr6h"
TELEBIRR_NUMBER = "0905527481"
ADMIN_USERNAME = "@berhanumekonen6"
BOT_USERNAME = "@DerashBingoPlayBot"

# === SUPABASE CONFIG (same values as your Streamlit app secrets) ===
SUPABASE_URL = "YOUR_SUPABASE_URL_HERE"
SUPABASE_KEY = "YOUR_SUPABASE_SECRET_KEY_HERE"

# === ADMIN TELEGRAM CHAT ID ===
# Get your numeric chat ID by messaging @userinfobot on Telegram
ADMIN_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID_HERE"

# === CONVERSATION STATES ===
(WITHDRAW_AMOUNT, WITHDRAW_USERNAME, WITHDRAW_PHONE,
 DEPOSIT_AMOUNT, DEPOSIT_USERNAME, DEPOSIT_SCREENSHOT) = range(6)


# ===================================================================
# SUPABASE HELPERS
# ===================================================================
def supabase_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def sb_get(table, query=""):
    try:
        url = f"{SUPABASE_URL}/rest/v1/{table}?{query}"
        r = requests.get(url, headers=supabase_headers(), timeout=10)
        return r.json() if r.status_code == 200 else []
    except Exception as e:
        logger.error(f"sb_get error: {e}")
        return []


def sb_post(table, data):
    try:
        url = f"{SUPABASE_URL}/rest/v1/{table}"
        r = requests.post(url, headers=supabase_headers(), json=data, timeout=10)
        return r.status_code in (200, 201)
    except Exception as e:
        logger.error(f"sb_post error: {e}")
        return False


def get_user(username):
    rows = sb_get("users", f"username=eq.{username}&select=*")
    return rows[0] if rows else None


def create_request(req_type, username, amount, phone, telegram_id,
                   telegram_name, screenshot_url=""):
    data = {
        "type": req_type,
        "username": username,
        "amount": float(amount),
        "phone": phone or "",
        "telegram_id": str(telegram_id),
        "telegram_name": telegram_name or "",
        "screenshot_url": screenshot_url or "",
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return sb_post("transactions", data)


# ===================================================================
# MENUS
# ===================================================================
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📝 Register", callback_data="register")],
        [InlineKeyboardButton("💰 Deposit / Pay", callback_data="deposit")],
        [InlineKeyboardButton("💸 Withdraw (ወጪ)", callback_data="withdraw")],
        [InlineKeyboardButton("🎯 Play Game", url=GAME_LINK)],
        [InlineKeyboardButton("❓ How to Play", callback_data="howto")],
        [InlineKeyboardButton("🆘 Support / መረጃ", callback_data="support")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_withdraw_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Start Withdrawal", callback_data="withdraw_start")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_deposit_menu():
    keyboard = [
        [InlineKeyboardButton("✅ I Have Paid — Send Screenshot", callback_data="deposit_start")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ===================================================================
# COMMANDS
# ===================================================================
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


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = f"""
❓ How can I help you?

📋 FAQ:
━━━━━━━━━━━━━━━━━━━
📝 Register → Click "📝 Register"
💰 Deposit  → Click "💰 Deposit / Pay"
💸 Withdraw → Click "💸 Withdraw (ወጪ)"
🎯 Play     → Click "🎯 Play Game"
🆘 Support  → {ADMIN_USERNAME}
━━━━━━━━━━━━━━━━━━━
"""
    await update.message.reply_text(help_text)


# ===================================================================
# CALLBACK BUTTON HANDLERS
# ===================================================================
async def how_to_play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
🎯 HOW TO PLAY DERASH BINGO
━━━━━━━━━━━━━━━━━━━
📝 STEP 1: REGISTER
💰 STEP 2: DEPOSIT → Telebirr: {TELEBIRR_NUMBER}
💸 STEP 3: WITHDRAW
🎯 STEP 4: PLAY
━━━━━━━━━━━━━━━━━━━
📌 RULES:
✅ Max 2 cards per player
✅ Card price: 10 ETB
✅ Prize: 8 ETB per card
✅ Auto-call every 2 seconds
🔗 PLAY NOW: {GAME_LINK}
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_main_menu())


async def register_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
📝 REGISTER TO PLAY

Open the game link below and create your account with a username and password.

🔗 GAME LINK: {GAME_LINK}
📞 Telebirr: {TELEBIRR_NUMBER}

After registering, come back here to deposit funds.
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_main_menu())


async def support_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
🆘 መረጃ እና ድጋፍ (Information & Support)
━━━━━━━━━━━━━━━━━━━
📌 ለመረጃ: {BOT_USERNAME}
📞 ቴሌብር: {TELEBIRR_NUMBER}
🤖 ቻትቦት: {BOT_USERNAME}
👤 አስተዳዳሪ: {ADMIN_USERNAME}
🎯 ጨዋታ: {GAME_LINK}
━━━━━━━━━━━━━━━━━━━
💬 ማንኛውም ጥያቄ ካለዎት እዚህ ይጠይቁ! 😊
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_main_menu())


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "🔙 Main Menu\n\n👇 Select an option:",
        reply_markup=get_main_menu()
    )


# ===================================================================
# DEPOSIT FLOW
# ===================================================================
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
5️⃣ Click "I Have Paid" below and send the screenshot
6️⃣ Wait for admin approval
7️⃣ Balance updates automatically

━━━━━━━━━━━━━━━━━━━
💳 SUGGESTED AMOUNTS:
20 ETB | 50 ETB | 100 ETB | 200 ETB | 500 ETB
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_deposit_menu())


async def deposit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💰 DEPOSIT — STEP 1 OF 3
━━━━━━━━━━━━━━━━━━━
📝 Enter the amount you deposited (ETB):
Example: 100
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text)
    return DEPOSIT_AMOUNT


async def deposit_amount_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("❌ Invalid amount! Enter a number. Example: 100")
        return DEPOSIT_AMOUNT

    if amount < 10:
        await update.message.reply_text("❌ Minimum deposit is 10 ETB.")
        return DEPOSIT_AMOUNT

    context.user_data['deposit_amount'] = amount
    text = f"""
💰 DEPOSIT — STEP 2 OF 3
━━━━━━━━━━━━━━━━━━━
💰 Amount: {amount:.2f} ETB

📝 Enter your registered username:
Example: john
"""
    await update.message.reply_text(text)
    return DEPOSIT_USERNAME


async def deposit_username_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()
    if len(username) < 2:
        await update.message.reply_text("❌ Username too short. Try again:")
        return DEPOSIT_USERNAME

    context.user_data['deposit_username'] = username
    text = f"""
💰 DEPOSIT — STEP 3 OF 3
━━━━━━━━━━━━━━━━━━━
💰 Amount: {context.user_data['deposit_amount']:.2f} ETB
👤 Username: {username}

📸 Now send the payment SCREENSHOT (photo).
"""
    await update.message.reply_text(text)
    return DEPOSIT_SCREENSHOT


async def deposit_screenshot_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("❌ Please send a PHOTO of your payment screenshot.")
        return DEPOSIT_SCREENSHOT

    photo = update.message.photo[-1]
    file_id = photo.file_id

    amount = context.user_data['deposit_amount']
    username = context.user_data['deposit_username']
    user = update.effective_user
    telegram_id = user.id
    telegram_name = user.full_name or user.username or f"User_{telegram_id}"

    ok = create_request(
        "deposit", username, amount,
        phone="", telegram_id=telegram_id,
        telegram_name=telegram_name,
        screenshot_url=file_id,
    )

    admin_msg = (
        f"🔔 NEW DEPOSIT REQUEST!\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Username: {username}\n"
        f"👤 Telegram: {telegram_name}\n"
        f"📱 Telegram ID: {telegram_id}\n"
        f"💰 Amount: {amount:.2f} ETB\n"
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Approve from Admin Panel."
    )
    try:
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=file_id, caption=admin_msg)
    except Exception as e:
        logger.error(f"Admin notify failed: {e}")
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg)
        except Exception as e2:
            logger.error(f"Admin text notify failed: {e2}")

    if ok:
        await update.message.reply_text(
            f"""
✅ DEPOSIT REQUEST SENT!
━━━━━━━━━━━━━━━━━━━
👤 Username: {username}
💰 Amount: {amount:.2f} ETB

⏳ Admin will verify and approve shortly.
💡 Your balance will update automatically.

✅ Thank you!
""",
            reply_markup=get_main_menu()
        )
    else:
        await update.message.reply_text("⚠️ Failed to save request. Try again later.")

    context.user_data.clear()
    return ConversationHandler.END


# ===================================================================
# WITHDRAW FLOW
# ===================================================================
async def withdraw_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💸 WITHDRAW (ወጪ)
━━━━━━━━━━━━━━━━━━━
📝 STEPS:
1️⃣ Click "Start Withdrawal"
2️⃣ Enter amount (min 20 ETB)
3️⃣ Enter your registered username
4️⃣ Enter your registered phone
5️⃣ Wait for admin approval

━━━━━━━━━━━━━━━━━━━
📞 Telebirr: {TELEBIRR_NUMBER}
👤 Support: {ADMIN_USERNAME}
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_withdraw_menu())


async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💸 WITHDRAWAL — STEP 1 OF 3
━━━━━━━━━━━━━━━━━━━
📝 Enter the amount to withdraw:
💰 MINIMUM: 20 ETB
Example: 50
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text)
    return WITHDRAW_AMOUNT


async def withdraw_amount_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("❌ Invalid amount. Example: 50")
        return WITHDRAW_AMOUNT

    if amount < 20:
        await update.message.reply_text("❌ Minimum withdrawal is 20 ETB.")
        return WITHDRAW_AMOUNT

    context.user_data['withdraw_amount'] = amount
    text = f"""
💸 WITHDRAWAL — STEP 2 OF 3
━━━━━━━━━━━━━━━━━━━
💰 Amount: {amount:.2f} ETB

📝 Enter your registered username:
Example: john
"""
    await update.message.reply_text(text)
    return WITHDRAW_USERNAME


async def withdraw_username_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()
    if len(username) < 2:
        await update.message.reply_text("❌ Username too short. Try again:")
        return WITHDRAW_USERNAME

    context.user_data['withdraw_username'] = username
    text = f"""
💸 WITHDRAWAL — STEP 3 OF 3
━━━━━━━━━━━━━━━━━━━
💰 Amount: {context.user_data['withdraw_amount']:.2f} ETB
👤 Username: {username}

📱 Enter your registered phone number:
Example: 0912345678
"""
    await update.message.reply_text(text)
    return WITHDRAW_PHONE


async def withdraw_phone_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    phone_clean = phone.replace(" ", "").replace("-", "")

    if len(phone_clean) < 9 or not phone_clean.isdigit():
        await update.message.reply_text("❌ Invalid phone. Example: 0912345678")
        return WITHDRAW_PHONE

    amount = context.user_data['withdraw_amount']
    username = context.user_data['withdraw_username']
    user = update.effective_user
    telegram_id = user.id
    telegram_name = user.full_name or user.username or f"User_{telegram_id}"

    user_row = get_user(username)
    if not user_row:
        await update.message.reply_text(
            f"❌ Username '{username}' not found. Please register first.",
            reply_markup=get_main_menu()
        )
        context.user_data.clear()
        return ConversationHandler.END

    balance = float(user_row.get("balance", 0))
    if balance < amount:
        await update.message.reply_text(
            f"❌ Insufficient balance!\n\n"
            f"💰 Your balance: {balance:.2f} ETB\n"
            f"💸 Requested: {amount:.2f} ETB",
            reply_markup=get_main_menu()
        )
        context.user_data.clear()
        return ConversationHandler.END

    ok = create_request(
        "withdraw", username, amount,
        phone=phone, telegram_id=telegram_id,
        telegram_name=telegram_name,
    )

    admin_msg = (
        f"🔔 NEW WITHDRAWAL REQUEST!\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Username: {username}\n"
        f"👤 Telegram: {telegram_name}\n"
        f"📱 Telegram ID: {telegram_id}\n"
        f"📞 Phone: {phone}\n"
        f"💰 Amount: {amount:.2f} ETB\n"
        f"💼 Current Balance: {balance:.2f} ETB\n"
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Approve from Admin Panel."
    )
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg)
    except Exception as e:
        logger.error(f"Admin notify failed: {e}")

    if ok:
        await update.message.reply_text(
            f"""
✅ WITHDRAWAL REQUEST SENT!
━━━━━━━━━━━━━━━━━━━
👤 Username: {username}
📱 Phone: {phone}
💰 Amount: {amount:.2f} ETB

⏳ Admin will verify and process shortly.
💡 Check balance after 24 hours.

✅ Thank you!
""",
            reply_markup=get_main_menu()
        )
    else:
        await update.message.reply_text("⚠️ Failed to save request. Try again.")

    context.user_data.clear()
    return ConversationHandler.END


async def cancel_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.", reply_markup=get_main_menu())
    context.user_data.clear()
    return ConversationHandler.END


# ===================================================================
# BUTTON ROUTER
# ===================================================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "register":
        await register_button(update, context)
    elif data == "deposit":
        await deposit_button(update, context)
    elif data == "withdraw":
        await withdraw_button(update, context)
    elif data == "howto":
        await how_to_play(update, context)
    elif data == "support":
        await support_button(update, context)
    elif data == "back_to_menu":
        await back_to_menu(update, context)


# ===================================================================
# MAIN
# ===================================================================
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    deposit_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(deposit_start, pattern="^deposit_start$")],
        states={
            DEPOSIT_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_amount_input)],
            DEPOSIT_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_username_input)],
            DEPOSIT_SCREENSHOT: [MessageHandler(filters.PHOTO, deposit_screenshot_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_flow)],
        name="deposit_conversation",
        persistent=False,
    )

    withdraw_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(withdraw_start, pattern="^withdraw_start$")],
        states={
            WITHDRAW_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_amount_input)],
            WITHDRAW_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_username_input)],
            WITHDRAW_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_phone_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_flow)],
        name="withdraw_conversation",
        persistent=False,
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(deposit_conv)
    application.add_handler(withdraw_conv)
    application.add_handler(CallbackQueryHandler(button_handler))

    print("=" * 50)
    print("✅ BOT IS RUNNING!")
    print("=" * 50)
    print(f"🤖 Bot: {BOT_USERNAME}")
    print(f"🎯 Game: {GAME_LINK}")
    print(f"📞 Telebirr: {TELEBIRR_NUMBER}")
    print("=" * 50)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
