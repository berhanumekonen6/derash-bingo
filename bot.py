import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from datetime import datetime
import asyncio

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === YOUR BOT INFORMATION ===
BOT_TOKEN = "8976887607:AAHPLbIKWkSr0Yjbab_Ebhk6V--cRwNi4Eo"
GAME_LINK = "https://tinyurl.com/yc4y6ktk"
TELEBIRR_NUMBER = "0905527481"
ADMIN_USERNAME = "@berhanumekonen6"
BOT_USERNAME = "@DerashBingoPlayBot"

# === CONVERSATION STATES ===
WITHDRAW_AMOUNT, WITHDRAW_USERNAME, WITHDRAW_PHONE = range(3)

# === GAME TIMER SETTINGS ===
GAME_DURATION_SECONDS = 120  # 2 minutes countdown
COUNTDOWN_CHAT_ID = None  # Will be set when timer starts

# === MAIN MENU ===
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📝 Register", callback_data="register")],
        [InlineKeyboardButton("💰 Deposit / Pay", callback_data="deposit")],
        [InlineKeyboardButton("💸 Withdraw (ወጪ)", callback_data="withdraw")],
        [InlineKeyboardButton("🎯 Play Game", url=GAME_LINK)],
        [InlineKeyboardButton("❓ How to Play", callback_data="howto")],
        [InlineKeyboardButton("🆘 Support / መረጃ", callback_data="support")],
        [InlineKeyboardButton("⏱️ Game Timer", callback_data="timer_status")],
    ]
    return InlineKeyboardMarkup(keyboard)

# === TIMER MENU ===
def get_timer_menu(seconds_remaining=None):
    if seconds_remaining is None:
        status_text = "⏱️ Timer is not running"
    else:
        minutes = seconds_remaining // 60
        seconds = seconds_remaining % 60
        status_text = f"⏱️ Time Remaining: {minutes:02d}:{seconds:02d}"
    
    keyboard = [
        [InlineKeyboardButton("▶️ Start Game Timer", callback_data="timer_start")],
        [InlineKeyboardButton("⏹️ Stop Timer", callback_data="timer_stop")],
        [InlineKeyboardButton("🔄 Reset Timer", callback_data="timer_reset")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard), status_text

# === WITHDRAW MENU ===
def get_withdraw_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Start Withdrawal", callback_data="withdraw_start")],
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
   → Enter your registered username
   → Enter your registered phone number

🎯 How to play?
   → Click "🎯 Play Game" button
   → Wait for timer to reach 0:00 to join game
   → Card selection stops at 0:00

⏱️ Game Timer?
   → Click "⏱️ Game Timer" to see time remaining
   → Timer counts down every second
   → At 0:00, game starts automatically

🆘 Need more help?
   → Click "Support / መረጃ" or contact {ADMIN_USERNAME}
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
   → Enter your registered username
   → Enter your registered phone number
   → Money will be sent to your Telebirr

━━━━━━━━━━━━━━━━━━━
🎯 STEP 4: PLAY
   → Click "🎯 Play Game" to start playing!
   → Login with your username and password
   → ⏱️ Watch the game timer count down
   → Select 1-2 cards (10 ETB each) before timer hits 0:00
   → At 0:00, card selection stops and game starts
   → Wait for numbers to be called
   → Get BINGO and WIN! 🎉

━━━━━━━━━━━━━━━━━━━
📌 RULES:
✅ Max 2 cards per player
✅ Card price: 10 ETB
✅ Prize: 8 ETB per card
✅ 201 cards available
✅ Auto-call every 2 seconds
✅ Card selection stops at 0:00

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
4️⃣ ⏱️ Watch timer - game starts at 0:00!

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
👉 {BOT_USERNAME}
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text, reply_markup=get_main_menu())

# === WITHDRAW BUTTON ===
async def withdraw_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💸 WITHDRAW (ወጪ)

━━━━━━━━━━━━━━━━━━━
📝 TO WITHDRAW:

1️⃣ Click "💰 Start Withdrawal"
2️⃣ Enter the amount you want to withdraw
3️⃣ Enter your registered username
4️⃣ Enter your registered phone number

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

# === START WITHDRAWAL CONVERSATION ===
async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💸 WITHDRAWAL - STEP 1 OF 3

━━━━━━━━━━━━━━━━━━━
📝 Please enter the amount you want to withdraw:

💰 MINIMUM: 20 ETB
💰 MAXIMUM: Your balance

━━━━━━━━━━━━━━━━━━━
📌 Send the amount as a number:
Example: 50
"""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text)
    return WITHDRAW_AMOUNT

# === HANDLE WITHDRAW AMOUNT ===
async def withdraw_amount_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text.strip())
    except ValueError:
        await update.message.reply_text(
            f"❌ Invalid amount! Please enter a valid number.\n\n"
            f"📌 Example: 50\n\n"
            f"💰 Minimum: 20 ETB"
        )
        return WITHDRAW_AMOUNT
    
    if amount < 20:
        await update.message.reply_text(
            f"❌ Minimum withdrawal is 20 ETB!\n\n"
            f"📌 Please enter a larger amount."
        )
        return WITHDRAW_AMOUNT
    
    # Store the amount in context
    context.user_data['withdraw_amount'] = amount
    
    text = f"""
💸 WITHDRAWAL - STEP 2 OF 3

━━━━━━━━━━━━━━━━━━━
💰 Amount: {amount:.2f} ETB

━━━━━━━━━━━━━━━━━━━
📝 Please enter your registered username:

📌 Example: john
"""
    await update.message.reply_text(text)
    return WITHDRAW_USERNAME

# === HANDLE WITHDRAW USERNAME ===
async def withdraw_username_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()
    
    if len(username) < 2:
        await update.message.reply_text(
            f"❌ Username must be at least 2 characters!\n\n"
            f"📌 Please enter your registered username."
        )
        return WITHDRAW_USERNAME
    
    # Store the username in context
    context.user_data['withdraw_username'] = username
    
    text = f"""
💸 WITHDRAWAL - STEP 3 OF 3

━━━━━━━━━━━━━━━━━━━
💰 Amount: {context.user_data['withdraw_amount']:.2f} ETB
👤 Username: {username}

━━━━━━━━━━━━━━━━━━━
📝 Please enter your registered phone number:

📌 Example: 0912345678
"""
    await update.message.reply_text(text)
    return WITHDRAW_PHONE

# === HANDLE WITHDRAW PHONE ===
async def withdraw_phone_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    
    # Simple phone validation (remove any spaces and check length)
    phone_clean = phone.replace(" ", "").replace("-", "")
    
    if len(phone_clean) < 9 or not phone_clean.isdigit():
        await update.message.reply_text(
            f"❌ Invalid phone number!\n\n"
            f"📌 Please enter a valid phone number.\n"
            f"Example: 0912345678"
        )
        return WITHDRAW_PHONE
    
    # Get all info
    amount = context.user_data['withdraw_amount']
    username = context.user_data['withdraw_username']
    
    # Get user info
    user = update.effective_user
    user_id = user.id
    user_full_name = user.full_name if user.full_name else user.username
    telegram_username = user.username if user.username else f"User_{user_id}"
    
    # Create confirmation message
    confirmation_text = f"""
✅ WITHDRAWAL REQUEST RECEIVED! 🎉

━━━━━━━━━━━━━━━━━━━
📋 WITHDRAWAL DETAILS:
━━━━━━━━━━━━━━━━━━━
👤 Username: {username}
👤 Full Name: {user_full_name}
📱 Phone: {phone}
💸 Amount: {amount:.2f} ETB
📱 Telegram ID: {user_id}
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
    
    # Send notification to admin
    admin_notification = f"""
🔔 NEW WITHDRAWAL REQUEST!

━━━━━━━━━━━━━━━━━━━
📋 DETAILS:
━━━━━━━━━━━━━━━━━━━
👤 Username: {username}
👤 Full Name: {user_full_name}
📱 Phone: {phone}
💸 Amount: {amount:.2f} ETB
📱 Telegram ID: {user_id}
📅 Requested: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━
📞 Process this request:
- Verify user balance: {username}
- Verify phone number: {phone}
- Send money to Telebirr: {TELEBIRR_NUMBER}
- Confirm completion
"""
    
    # Uncomment the lines below to send admin notification
    # try:
    #     await context.bot.send_message(chat_id="YOUR_ADMIN_CHAT_ID", text=admin_notification)
    # except:
    #     pass
    
    logger.info(f"Withdrawal request: {username} - {amount} ETB - Phone: {phone}")
    
    # Clear conversation data
    context.user_data.clear()
    
    # End conversation
    return ConversationHandler.END

# === CANCEL WITHDRAWAL ===
async def cancel_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Withdrawal cancelled.\n\n"
        "🔙 To start again, click '💸 Withdraw (ወጪ)'",
        reply_markup=get_main_menu()
    )
    return ConversationHandler.END

# === BACK TO MENU ===
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "🔙 Back to Main Menu\n\n👇 Select an option below:",
        reply_markup=get_main_menu()
    )

# === SUPPORT BUTTON - UPDATED WITH FULL AMHARIC INFORMATION ===
async def support_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
🆘 መረጃ እና ድጋፍ (Information & Support)

━━━━━━━━━━━━━━━━━━━
📌 ለመረጃ (ለምሳሌ ለመመዝገብ፤ ለመጫዎት፤ ወጭና ገቢ): {BOT_USERNAME}

━━━━━━━━━━━━━━━━━━━
📋 አጭር መመሪያ:

📝 ለመመዝገብ:
   → "📝 Register" ይጫኑ

💰 ገንዘብ ለመጨመር (Deposit):
   → "💰 Deposit / Pay" ይጫኑ
   → በቴሌብር ወደ {TELEBIRR_NUMBER} ይላኩ
   → ማረጋገጫ ስክሪንሾት ይላኩ

💸 ገንዘብ ለማውጣት (Withdraw):
   → "💸 Withdraw (ወጪ)" ይጫኑ
   → መጠኑን ያስገቡ
   → የተመዘገቡበትን ስም ያስገቡ
   → የተመዘገቡበትን ስልክ ቁጥር ያስገቡ

🎯 ለመጫወት:
   → "🎯 Play Game" ይጫኑ
   → በስምዎ እና ይለፍቃድዎ ይግቡ
   → ⏱️ ጨዋታው ከመጀመሩ በፊት ካርድ ይምረጡ
   → በ0:00 ላይ ካርድ መምረጥ ይቆማል
   → ቁጥሮች ሲጠሩ ይጠብቁ
   → ቢንጎ ሲሆን ያሸንፉ! 🎉

━━━━━━━━━━━━━━━━━━━
📌 ህጎች:
✅ በአንድ ተጫዋች እስከ 2 ካርዶች
✅ አንድ ካርድ: 10 ETB
✅ ሽልማት: 8 ETB በአንድ ካርድ
✅ 201 ካርዶች ይገኛሉ
✅ በየ2 ሰከንድ አውቶማቲክ ቁጥር ይጠራል
✅ ካርድ መምረጥ የሚቻለው ከጨዋታ መጀመሩ በፊት ብቻ ነው

━━━━━━━━━━━━━━━━━━━
📞 ቴሌብር: {TELEBIRR_NUMBER}
🤖 ቻትቦት: {BOT_USERNAME}
👤 አስተዳዳሪ: {ADMIN_USERNAME}
🎯 ጨዋታ: {GAME_LINK}

━━━━━━━━━━━━━━━━━━━
💬 ማንኛውም ጥያቄ ካለዎት እዚህ ይጠይቁ! 😊
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
            f"📞 Telebirr: {TELEBIRR_NUMBER}\n\n"
            f"📌 ለመረጃ: {BOT_USERNAME}"
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
4️⃣ ⏱️ Watch timer - game starts at 0:00!

🔗 GAME LINK: {GAME_LINK}
💰 Telebirr: {TELEBIRR_NUMBER}

🎉 Welcome to Derash BINGO! 🎉

📌 ለመረጃ: {BOT_USERNAME}
""",
        reply_markup=get_main_menu()
    )

# === GAME TIMER FUNCTIONS ===

async def update_timer_message(context: ContextTypes.DEFAULT_TYPE):
    """Background task that updates timer every second"""
    job_data = context.job.data
    seconds_remaining = job_data.get('seconds', GAME_DURATION_SECONDS)
    
    if seconds_remaining <= 0:
        # Timer hit 0:00 - Game starts!
        chat_id = job_data.get('chat_id')
        if chat_id:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"""
🎯 GAME STARTED! 🎯

━━━━━━━━━━━━━━━━━━━
⏱️ COUNTDOWN REACHED 0:00!

❌ CARD SELECTION IS NOW CLOSED!
✅ GAME HAS BEGUN!

🎯 Login now and join the game!
🔗 {GAME_LINK}

📌 መረጃ ለማግኘት: {BOT_USERNAME}
"""
            )
        
        # Stop the timer job
        context.job.schedule_removal()
        
        # Reset timer in user_data
        context.user_data['timer_seconds'] = 0
        context.user_data['timer_running'] = False
        
        return
    
    # Update seconds remaining
    seconds_remaining -= 1
    job_data['seconds'] = seconds_remaining
    context.user_data['timer_seconds'] = seconds_remaining
    
    # Send update every 10 seconds to avoid spam, or every second for last 10 seconds
    should_update = (
        seconds_remaining <= 10 or 
        seconds_remaining % 10 == 0 or
        seconds_remaining == 30 or
        seconds_remaining == 60
    )
    
    if should_update and job_data.get('chat_id'):
        minutes = seconds_remaining // 60
        seconds = seconds_remaining % 60
        timer_text = f"""
⏱️ GAME COUNTDOWN

━━━━━━━━━━━━━━━━━━━
⏰ Time Remaining: {minutes:02d}:{seconds:02d}

━━━━━━━━━━━━━━━━━━━
📝 Actions:
• Select your cards before 0:00
• At 0:00, game starts automatically
• Card selection stops at 0:00

━━━━━━━━━━━━━━━━━━━
💰 Each card: 10 ETB
🎯 Prize: 8 ETB per card
✅ Max 2 cards per player

🔗 PLAY NOW: {GAME_LINK}
"""
        
        try:
            await context.bot.send_message(
                chat_id=job_data['chat_id'],
                text=timer_text
            )
        except Exception as e:
            logger.error(f"Failed to send timer update: {e}")

async def timer_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show timer status"""
    await update.callback_query.answer()
    
    seconds = context.user_data.get('timer_seconds', 0)
    is_running = context.user_data.get('timer_running', False)
    
    if is_running and seconds > 0:
        minutes = seconds // 60
        secs = seconds % 60
        status_text = f"⏱️ Timer Running: {minutes:02d}:{secs:02d}"
    elif not is_running and seconds > 0:
        minutes = seconds // 60
        secs = seconds % 60
        status_text = f"⏱️ Timer Paused: {minutes:02d}:{secs:02d}"
    elif seconds == 0:
        status_text = "⏱️ Timer at 0:00 - Game is active!"
    else:
        status_text = "⏱️ Timer not started"
    
    text = f"""
⏱️ GAME TIMER STATUS

━━━━━━━━━━━━━━━━━━━
📊 {status_text}

━━━━━━━━━━━━━━━━━━━
📌 Controls:
▶️ Start - Begin countdown
⏹️ Stop - Pause countdown
🔄 Reset - Reset to {GAME_DURATION_SECONDS//60} minutes

━━━━━━━━━━━━━━━━━━━
💡 When timer reaches 0:00:
• Card selection stops
• Game automatically starts
• Players must join the game

━━━━━━━━━━━━━━━━━━━
📞 Admin: {ADMIN_USERNAME}
"""
    
    timer_menu, _ = get_timer_menu(seconds if is_running else None)
    await update.callback_query.edit_message_text(text, reply_markup=timer_menu)

async def timer_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the game timer"""
    await update.callback_query.answer()
    
    chat_id = update.effective_chat.id
    
    # Check if timer is already running
    if context.user_data.get('timer_running', False):
        await update.callback_query.edit_message_text(
            "⏱️ Timer is already running!\n\n"
            "📌 Use '⏹️ Stop Timer' to pause or '🔄 Reset Timer' to restart.",
            reply_markup=get_timer_menu()[0]
        )
        return
    
    # Get current seconds or reset to default
    seconds = context.user_data.get('timer_seconds', GAME_DURATION_SECONDS)
    if seconds <= 0:
        seconds = GAME_DURATION_SECONDS
    
    context.user_data['timer_running'] = True
    context.user_data['timer_seconds'] = seconds
    
    # Schedule the timer job
    job_data = {
        'seconds': seconds,
        'chat_id': chat_id
    }
    
    # Remove existing job if any
    if context.job_queue:
        current_jobs = context.job_queue.jobs()
        for job in current_jobs:
            if job.name == f"timer_{chat_id}":
                job.schedule_removal()
    
    # Create new job that runs every second
    context.job_queue.run_repeating(
        update_timer_message,
        interval=1,
        first=1,
        data=job_data,
        name=f"timer_{chat_id}"
    )
    
    minutes = seconds // 60
    secs = seconds % 60
    
    await update.callback_query.edit_message_text(
        f"""
▶️ TIMER STARTED! ⏱️

━━━━━━━━━━━━━━━━━━━
⏰ Time: {minutes:02d}:{secs:02d}

━━━━━━━━━━━━━━━━━━━
📌 Timer will count down every second.
⏰ Updates sent every 10 seconds.
🔔 Final 10 seconds update every second.

━━━━━━━━━━━━━━━━━━━
📝 Remember:
• Select cards before 0:00
• At 0:00, game starts!
• Card selection stops at 0:00

🎯 Good luck! 🍀
""",
        reply_markup=get_timer_menu()[0]
    )

async def timer_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop the game timer"""
    await update.callback_query.answer()
    
    chat_id = update.effective_chat.id
    
    if not context.user_data.get('timer_running', False):
        await update.callback_query.edit_message_text(
            "⏱️ Timer is not currently running!\n\n"
            "📌 Use '▶️ Start Game Timer' to begin.",
            reply_markup=get_timer_menu()[0]
        )
        return
    
    # Remove the timer job
    if context.job_queue:
        current_jobs = context.job_queue.jobs()
        for job in current_jobs:
            if job.name == f"timer_{chat_id}":
                job.schedule_removal()
    
    context.user_data['timer_running'] = False
    
    seconds = context.user_data.get('timer_seconds', 0)
    minutes = seconds // 60
    secs = seconds % 60
    
    await update.callback_query.edit_message_text(
        f"""
⏹️ TIMER STOPPED! ⏱️

━━━━━━━━━━━━━━━━━━━
⏰ Time Remaining: {minutes:02d}:{secs:02d}

━━━━━━━━━━━━━━━━━━━
📌 Use '▶️ Start Game Timer' to continue.
🔄 Use '🔄 Reset Timer' to start over.

━━━━━━━━━━━━━━━━━━━
💡 Card selection is still open until 0:00!
""",
        reply_markup=get_timer_menu()[0]
    )

async def timer_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset the game timer"""
    await update.callback_query.answer()
    
    chat_id = update.effective_chat.id
    
    # Remove existing timer job
    if context.job_queue:
        current_jobs = context.job_queue.jobs()
        for job in current_jobs:
            if job.name == f"timer_{chat_id}":
                job.schedule_removal()
    
    context.user_data['timer_running'] = False
    context.user_data['timer_seconds'] = GAME_DURATION_SECONDS
    
    minutes = GAME_DURATION_SECONDS // 60
    
    await update.callback_query.edit_message_text(
        f"""
🔄 TIMER RESET! ⏱️

━━━━━━━━━━━━━━━━━━━
⏰ Reset to: {minutes:02d}:00

━━━━━━━━━━━━━━━━━━━
📌 Use '▶️ Start Game Timer' to begin countdown.
⏰ Timer will count down every second.

━━━━━━━━━━━━━━━━━━━
📝 Remember:
• Select cards before 0:00
• At 0:00, game starts!
• Card selection stops at 0:00
""",
        reply_markup=get_timer_menu()[0]
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
    elif query.data == "withdraw_start":
        await withdraw_start(update, context)
    elif query.data == "howto":
        await how_to_play(update, context)
    elif query.data == "support":
        await support_button(update, context)
    elif query.data == "back_to_menu":
        await back_to_menu(update, context)
    elif query.data == "timer_status":
        await timer_status(update, context)
    elif query.data == "timer_start":
        await timer_start(update, context)
    elif query.data == "timer_stop":
        await timer_stop(update, context)
    elif query.data == "timer_reset":
        await timer_reset(update, context)

# === MAIN FUNCTION ===
def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # === CONVERSATION HANDLER FOR WITHDRAWAL ===
    withdraw_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(withdraw_start, pattern="^withdraw_start$")],
        states={
            WITHDRAW_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_amount_input)],
            WITHDRAW_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_username_input)],
            WITHDRAW_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_phone_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_withdraw)],
        name="withdraw_conversation",
        persistent=False,
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("register", register_command))
    application.add_handler(withdraw_conv)
    application.add_handler(CallbackQueryHandler(button_handler))

    print("=" * 50)
    print("✅ BOT IS RUNNING!")
    print("=" * 50)
    print(f"🤖 Bot: @DerashBingoPlayBot")
    print(f"🔗 Link: https://t.me/DerashBingoPlayBot")
    print(f"🎯 Game: {GAME_LINK}")
    print(f"📞 Telebirr: {TELEBIRR_NUMBER}")
    print(f"💸 Withdraw: Conversation flow (amount, username, phone)")
    print(f"⏱️ Timer: {GAME_DURATION_SECONDS//60} minutes countdown")
    print("=" * 50)
    print("Send /start on Telegram to test!")
    print("Press Ctrl+C to stop the bot.")
    print("=" * 50)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
