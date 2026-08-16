import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime
from config import *
from database import *
from models import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# INLINE KEYBOARDS
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Pul ishlash", callback_data="earn")],
        [InlineKeyboardButton("💸 Pul chiqarish", callback_data="withdraw")],
        [InlineKeyboardButton("👤 Mening profilim", callback_data="profile")],
        [InlineKeyboardButton("🏆 Top reyting", callback_data="top_rating")],
        [InlineKeyboardButton("📢 Toʻlovlar kanali", callback_data="payment_channel")]
    ])

def earn_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Referal havolasi", callback_data="referral_link")],
        [InlineKeyboardButton("📊 Tasnif va narxlar", callback_data="commission_info")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
    ])

def withdraw_menu_keyboard(db_session):
    types = get_withdrawal_types(db_session)
    buttons = []
    for wtype in types:
        buttons.append([InlineKeyboardButton(f"{wtype.name}", callback_data=f"wtype_{wtype.id}")])
    buttons.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(buttons)

def top_rating_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Eng koʻp ishlagani", callback_data="top_earned_today")],
        [InlineKeyboardButton("💸 Eng koʻp yechishga bergani", callback_data="top_withdrawn_today")],
        [InlineKeyboardButton("📅 Oylik", callback_data="top_earned_month")],
        [InlineKeyboardButton("📅 Umumiy", callback_data="top_earned_all")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
    ])

def yes_no_keyboard(callback_yes, callback_no):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Ha", callback_data=callback_yes),
            InlineKeyboardButton("❌ Yo'q", callback_data=callback_no)
        ]
    ])

# USER HANDLERS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = SessionLocal()
    
    # Get or create user
    db_user = get_or_create_user(db, user.id, user.username, user.first_name)
    
    # Check if user is banned
    if db_user.is_banned:
        await update.message.reply_text("❌ Siz bloklanib tushingiz. Admin bilan bog'lanib o'tuvchi mavjud emas.")
        db.close()
        return
    
    # Check phone verification
    if not db_user.phone_verified:
        await update.message.reply_text(
            "📱 Telefon raqamini tasdiqlab o'tish kerak.\n\n"
            "Pastdagi tugma orqali kontaktingizni ulashing:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📱 Kontaktni ulashing", callback_data="verify_phone")
            ]])
        )
        db.close()
        return
    
    # Check mandatory channels
    channels = get_channels_by_type(db, "mandatory")
    not_subscribed = []
    
    for channel in channels:
        try:
            member = await context.bot.get_chat_member(channel.channel_id, user.id)
            if member.status not in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                not_subscribed.append(channel)
        except:
            not_subscribed.append(channel)
    
    if not_subscribed:
        buttons = []
        for channel in not_subscribed:
            channel_link = f"https://t.me/{channel.channel_name.replace('@', '')}"
            buttons.append([InlineKeyboardButton(f"📌 {channel.channel_name}", url=channel_link)])
        buttons.append([InlineKeyboardButton("✅ Obuna qildim", callback_data="check_subscription")])
        
        await update.message.reply_text(
            "⚠️ Majburiy kanallarga obuna bo'lishi kerak!\n\n"
            "Quyidagi kanallarga obuna bo'ling:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        db.close()
        return
    
    # Check if referral
    referrer_id = context.user_data.get('referrer_id')
    if referrer_id and not get_referrer(db, db_user.id):
        add_referral(db, referrer_id, db_user.id)
        referrer = get_user_by_id(db, referrer_id)
        if referrer and referrer.can_refer:
            add_balance(db, referrer_id, REFERRAL_BONUS)
    
    # Main menu
    await update.message.reply_text(
        f"👋 Salom, {user.first_name}!\n\n"
        f"💰 Balansiz: {db_user.balance:.0f}\n"
        f"💸 Jami yechishga berilgan: {db_user.total_withdrawn:.0f}",
        reply_markup=main_menu_keyboard()
    )
    
    db.close()

async def verify_phone_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "📱 Kontaktingizni ulashing:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("📞 Kontakt", request_contact=True)
        ]])
    )

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    user = update.effective_user
    contact = update.message.contact
    
    # Verify Uzbek phone
    phone = contact.phone_number
    if not re.match(PHONE_REGEX, phone):
        await update.message.reply_text("❌ Faqat O'zbekiston raqamlari qabul qilinadi! (+998...)")
        db.close()
        return
    
    # Check if phone already used
    existing = get_user_by_phone(db, phone)
    if existing and existing.telegram_id != user.id:
        await update.message.reply_text("❌ Bu raqam boshqa foydalanuvchi tomonidan ishlatilyapti!")
        db.close()
        return
    
    # Save phone
    db_user = get_or_create_user(db, user.id, user.username, user.first_name)
    db_user.phone = phone
    db_user.phone_verified = True
    db.commit()
    
    await update.message.reply_text(
        "✅ Telefon raqam tasdiqlandi!\n\n"
        "Endi botdan foydalanishni boshlash mumkin.",
        reply_markup=main_menu_keyboard()
    )
    
    db.close()

async def earn_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "💰 Pul ishlash\n\n"
        "Do'stingizni taklif qilib pul ishlay olasiz.",
        reply_markup=earn_menu_keyboard()
    )

async def referral_link_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    db = SessionLocal()
    
    db_user = get_user_by_telegram_id(db, user_id)
    referral_link = f"https://t.me/{context.bot.username}?start={user_id}"
    
    await query.answer()
    await query.edit_message_text(
        f"🔗 Sizning referal havolangiz:\n\n"
        f"`{referral_link}`\n\n"
        f"👥 Jami referallar: {db_user.referral_count}\n"
        f"✅ Faol referallar: {get_active_referrals_count(db, user_id)}\n\n"
        f"Har bir do'stning ichiga 5000 pul ishlashga beriladi!",
        reply_markup=earn_menu_keyboard(),
        parse_mode="Markdown"
    )
    
    db.close()

async def profile_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    db = SessionLocal()
    
    stats = get_user_stats(db, get_user_by_telegram_id(db, user_id).id)
    referrer = get_referrer(db, get_user_by_telegram_id(db, user_id).id)
    
    text = f"""👤 Mening profilim

💰 Balans: {stats['balance']:.0f}
💸 Jami ishlagan: {stats['total_earned']:.0f}
📤 Jami yechgan: {stats['total_withdrawn']:.0f}

👥 Jami referallar: {stats['referral_count']}
✅ Faol referallar: {stats['active_referrals']}
📊 Bugun ishlagan referal: {stats['today_referrals']}

{'👨 Referal: ' + str(referrer.first_name) if referrer else ''}
"""
    
    await query.answer()
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
    ]))
    
    db.close()

async def withdraw_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    db = SessionLocal()
    
    db_user = get_user_by_telegram_id(db, user_id)
    
    if db_user.balance < MIN_WITHDRAWAL:
        await query.answer(f"❌ Minimal yechish: {MIN_WITHDRAWAL:.0f}")
        return
    
    await query.answer()
    await query.edit_message_text(
        "💸 Pul chiqarish\n\n"
        "Yechish turini tanlang:",
        reply_markup=withdraw_menu_keyboard(db)
    )
    
    db.close()

async def withdrawal_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    # Extract withdrawal type ID
    wtype_id = int(query.data.split('_')[1])
    
    db = SessionLocal()
    wtype = db.query(WithdrawalType).filter(WithdrawalType.id == wtype_id).first()
    
    context.user_data['withdrawal_type_id'] = wtype_id
    context.user_data['withdrawal_type_name'] = wtype.name
    
    await query.answer()
    await query.edit_message_text(
        f"💵 {wtype.name} orqali yechish\n\n"
        f"Miqdorni kiriting ({MIN_WITHDRAWAL:.0f} - {MAX_WITHDRAWAL:.0f}):"
    )
    
    context.user_data['awaiting_withdrawal_amount'] = True
    db.close()

async def withdrawal_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('awaiting_withdrawal_amount'):
        return
    
    user_id = update.effective_user.id
    db = SessionLocal()
    
    try:
        amount = float(update.message.text)
        
        if amount < MIN_WITHDRAWAL or amount > MAX_WITHDRAWAL:
            await update.message.reply_text(
                f"❌ Miqdor {MIN_WITHDRAWAL:.0f} - {MAX_WITHDRAWAL:.0f} oraligida bo'lishi kerak!"
            )
            db.close()
            return
        
        db_user = get_user_by_telegram_id(db, user_id)
        
        if db_user.balance < amount:
            await update.message.reply_text(f"❌ Balansingizda yetarli pul yo'q!")
            db.close()
            return
        
        # Ask for payment address
        context.user_data['withdrawal_amount'] = amount
        context.user_data['awaiting_payment_address'] = True
        context.user_data['awaiting_withdrawal_amount'] = False
        
        await update.message.reply_text(
            f"📮 To'lov manzilingizni kiriting:\n\n"
            f"(Karta raqami bo'lsa: ****1234 korinishida, nomer bo'lsa: +998...)"
        )
        
    except ValueError:
        await update.message.reply_text("❌ Raqam kiriting!")
    
    db.close()

async def payment_address_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('awaiting_payment_address'):
        return
    
    user_id = update.effective_user.id
    db = SessionLocal()
    
    address = update.message.text
    amount = context.user_data['withdrawal_amount']
    wtype_id = context.user_data['withdrawal_type_id']
    wtype_name = context.user_data['withdrawal_type_name']
    
    db_user = get_user_by_telegram_id(db, user_id)
    
    # Create withdrawal request
    withdrawal = create_withdrawal(
        db, db_user.id, amount, "GidrocoinCoin", wtype_name, address
    )
    
    # Subtract from balance
    subtract_balance(db, db_user.id, amount)
    
    context.user_data['awaiting_payment_address'] = False
    context.user_data['withdrawal_type_id'] = None
    context.user_data['withdrawal_amount'] = None
    
    await update.message.reply_text(
        f"✅ To'lov so'rovi qabul qilindi!\n\n"
        f"Buyurtma #️⃣: {withdrawal.order_number}\n"
        f"Miqdor: {amount:.0f} GidrocoinCoin\n"
        f"Tur: {wtype_name}\n"
        f"Manzil: {address}\n\n"
        f"Admin tasdiqlashini kutiyapiz...",
        reply_markup=main_menu_keyboard()
    )
    
    # Notify admin
    admin_msg = (
        f"🔔 Yangi to'lov so'rovi!\n\n"
        f"Buyurtma #️⃣: {withdrawal.order_number}\n"
        f"Foydalanuvchi: {db_user.first_name} ({db_user.telegram_id})\n"
        f"Miqdor: {amount:.0f} GidrocoinCoin\n"
        f"Tur: {wtype_name}\n"
        f"Manzil: {address}\n"
        f"Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )
    
    try:
        await context.bot.send_message(
            ADMIN_ID,
            admin_msg,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_withdraw_{withdrawal.id}"),
                    InlineKeyboardButton("❌ Bekor qilish", callback_data=f"reject_withdraw_{withdrawal.id}")
                ]
            ])
        )
    except:
        pass
    
    db.close()

async def top_rating_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🏆 Top reyting\n\n"
        "Reyting turini tanlang:",
        reply_markup=top_rating_keyboard()
    )

async def show_top_earners(update: Update, context: ContextTypes.DEFAULT_TYPE, period: str):
    query = update.callback_query
    db = SessionLocal()
    
    if 'earned' in query.data:
        users = get_top_earners(db, period, 10)
        title = "👥 Eng koʻp pul ishlagani"
        metric = "total_earned"
    else:
        users = get_top_withdrawers(db, period, 10)
        title = "💸 Eng koʻp yechishga bergani"
        metric = "total_withdrawn"
    
    text = f"{title} ({period.upper()}):\n\n"
    
    for idx, user in enumerate(users, 1):
        amount = getattr(user, metric)
        text += f"{idx}. {user.first_name or 'Foydalanuvchi'}: {amount:.0f}\n"
    
    buttons = []
    if period != 'today':
        buttons.append([InlineKeyboardButton("📅 Bugun", callback_data=f"top_earned_today")])
    if period != 'month':
        buttons.append([InlineKeyboardButton("📅 Oylik", callback_data=f"top_earned_month")])
    if period != 'all':
        buttons.append([InlineKeyboardButton("📅 Umumiy", callback_data=f"top_earned_all")])
    
    buttons.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="top_rating")])
    
    await query.answer()
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    
    db.close()

async def back_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    
    await query.answer()
    await query.edit_message_text(
        f"👋 Salom, {user.first_name}!",
        reply_markup=main_menu_keyboard()
    )

async def commission_info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    db = SessionLocal()
    
    types = get_withdrawal_types(db)
    
    text = "📊 Tasnif va narxlar:\n\n"
    text += f"🎁 Referal bonus: {REFERRAL_BONUS:.0f} GidrocoinCoin\n"
    text += f"📈 Komissiya: {COMMISSION_PERCENT}%\n\n"
    text += "💱 Valyuta kurslar:\n\n"
    
    for wtype in types:
        text += f"🏦 {wtype.name}:\n"
        # Add rates for this type
        text += "  1 GidrocoinCoin = ? (Admin sozlaydi)\n\n"
    
    await query.answer()
    await query.edit_message_text(text, reply_markup=earn_menu_keyboard())
    
    db.close()

async def payment_channel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    db = SessionLocal()
    
    channel = db.query(Channel).filter(Channel.channel_type == "payment").first()
    
    if channel:
        channel_link = f"https://t.me/{channel.channel_name.replace('@', '')}"
        text = f"📢 Toʻlovlar kanali\n\n{channel.channel_name}"
        
        await query.answer()
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📌 Kanalga o'tish", url=channel_link)],
                [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
            ])
        )
    else:
        await query.answer("⚠️ To'lovlar kanali hali sozlanmagan!")
    
    db.close()

# Admin handlers will be in admin.py
# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')

# Main function
async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, withdrawal_amount_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, payment_address_handler))
    
    # Callback handlers
    app.add_handler(CallbackQueryHandler(verify_phone_callback, pattern="^verify_phone$"))
    app.add_handler(CallbackQueryHandler(earn_callback, pattern="^earn$"))
    app.add_handler(CallbackQueryHandler(referral_link_callback, pattern="^referral_link$"))
    app.add_handler(CallbackQueryHandler(profile_callback, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(withdraw_callback, pattern="^withdraw$"))
    app.add_handler(CallbackQueryHandler(withdrawal_type_callback, pattern="^wtype_"))
    app.add_handler(CallbackQueryHandler(top_rating_callback, pattern="^top_rating$"))
    app.add_handler(CallbackQueryHandler(lambda u, c: show_top_earners(u, c, 'today'), pattern="^top_earned_today$"))
    app.add_handler(CallbackQueryHandler(lambda u, c: show_top_earners(u, c, 'month'), pattern="^top_earned_month$"))
    app.add_handler(CallbackQueryHandler(lambda u, c: show_top_earners(u, c, 'all'), pattern="^top_earned_all$"))
    app.add_handler(CallbackQueryHandler(lambda u, c: show_top_earners(u, c, 'today'), pattern="^top_withdrawn_today$"))
    app.add_handler(CallbackQueryHandler(back_main_callback, pattern="^back_main$"))
    app.add_handler(CallbackQueryHandler(commission_info_callback, pattern="^commission_info$"))
    app.add_handler(CallbackQueryHandler(payment_channel_callback, pattern="^payment_channel$"))
    
    app.add_error_handler(error_handler)
    
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
