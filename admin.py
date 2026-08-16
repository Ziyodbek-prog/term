from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import logging
from datetime import datetime
from config import *
from database import *
from models import SessionLocal, User, Withdrawal, Channel, WithdrawalType, CurrencyRate, Settings
from telegram import Bot
from telegram.error import TelegramError
import asyncio

app = Flask(__name__)
app.secret_key = os.getenv('ADMIN_SECRET_KEY', 'change-this-secret-key')

logger = logging.getLogger(__name__)
bot = Bot(token=BOT_TOKEN)

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# LOGIN
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.getenv('ADMIN_PASSWORD', 'admin123'):
            session['admin_id'] = ADMIN_ID
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Parol noto\'g\'ri'), 401
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('admin_login'))

# DASHBOARD
@app.route('/admin')
@admin_required
def admin_dashboard():
    db = SessionLocal()
    stats = get_global_stats(db)
    db.close()
    
    return render_template('admin_dashboard.html', stats=stats)

# CHANNELS MANAGEMENT
@app.route('/admin/channels', methods=['GET', 'POST'])
@admin_required
def manage_channels():
    db = SessionLocal()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            channel_id = int(request.form.get('channel_id'))
            channel_name = request.form.get('channel_name')
            channel_type = request.form.get('channel_type')
            is_public = request.form.get('is_public') == 'on'
            
            add_channel(db, channel_id, channel_name, channel_type, is_public)
            return jsonify({'success': True, 'message': 'Kanal qo\'shildi'})
        
        elif action == 'delete':
            channel_id = int(request.form.get('channel_id'))
            delete_channel(db, channel_id)
            return jsonify({'success': True, 'message': 'Kanal o\'chirildi'})
    
    channels = get_all_channels(db)
    db.close()
    
    return render_template('admin_channels.html', channels=channels)

# STATISTICS
@app.route('/admin/statistics')
@admin_required
def admin_statistics():
    db = SessionLocal()
    stats = get_global_stats(db)
    
    # Top earners
    top_earners = get_top_earners(db, 'month', 20)
    
    # Top withdrawers
    top_withdrawers = get_top_withdrawers(db, 'month', 20)
    
    # Pending withdrawals count
    pending = db.query(Withdrawal).filter(Withdrawal.status == 'pending').count()
    
    db.close()
    
    return render_template('admin_statistics.html', 
                         stats=stats,
                         top_earners=top_earners,
                         top_withdrawers=top_withdrawers,
                         pending_withdrawals=pending)

# USERS MANAGEMENT
@app.route('/admin/users', methods=['GET', 'POST'])
@admin_required
def manage_users():
    db = SessionLocal()
    
    search_type = request.args.get('search_type', 'user_id')
    search_query = request.args.get('search_query', '')
    user = None
    
    if search_query:
        if search_type == 'user_id':
            user = get_user_by_id(db, int(search_query))
        elif search_type == 'telegram_id':
            user = get_user_by_telegram_id(db, int(search_query))
    
    if request.method == 'POST':
        action = request.form.get('action')
        user_id = int(request.form.get('user_id'))
        
        if action == 'ban':
            ban_user(db, user_id)
            return jsonify({'success': True, 'message': 'Foydalanuvchi bloklanadi'})
        elif action == 'unban':
            unban_user(db, user_id)
            return jsonify({'success': True, 'message': 'Foydalanuvchi blokdan chiqariladi'})
        elif action == 'add_balance':
            amount = float(request.form.get('amount'))
            add_balance(db, user_id, amount)
            return jsonify({'success': True, 'message': 'Balans qo\'shildi'})
        elif action == 'subtract_balance':
            amount = float(request.form.get('amount'))
            subtract_balance(db, user_id, amount)
            return jsonify({'success': True, 'message': 'Balans ayirildi'})
        elif action == 'disable_referral':
            disable_referral(db, user_id)
            return jsonify({'success': True, 'message': 'Referal bloklanadi'})
        elif action == 'send_message':
            message = request.form.get('message')
            try:
                asyncio.run(bot.send_message(user.telegram_id, message))
                return jsonify({'success': True, 'message': 'Xabar yuborildi'})
            except TelegramError as e:
                return jsonify({'success': False, 'message': str(e)})
    
    db.close()
    
    return render_template('admin_users.html', user=user)

# WITHDRAWAL MANAGEMENT
@app.route('/admin/withdrawals')
@admin_required
def manage_withdrawals():
    db = SessionLocal()
    
    status = request.args.get('status', 'pending')
    
    if status == 'pending':
        withdrawals = get_pending_withdrawals(db)
    elif status == 'rejected':
        withdrawals = get_rejected_withdrawals(db)
    else:
        withdrawals = db.query(Withdrawal).all()
    
    db.close()
    
    return render_template('admin_withdrawals.html', 
                         withdrawals=withdrawals,
                         current_status=status)

@app.route('/admin/withdrawals/<int:withdrawal_id>', methods=['POST'])
@admin_required
def process_withdrawal(withdrawal_id):
    db = SessionLocal()
    action = request.form.get('action')
    
    withdrawal = db.query(Withdrawal).filter(Withdrawal.id == withdrawal_id).first()
    
    if action == 'approve':
        approve_withdrawal(db, withdrawal_id)
        status = 'approved'
    elif action == 'reject':
        reject_withdrawal(db, withdrawal_id)
        status = 'rejected'
    else:
        return jsonify({'success': False}), 400
    
    # Notify user
    user = db.query(User).filter(User.id == withdrawal.user_id).first()
    message = (
        f"💳 To'lov so'rovi #{withdrawal.order_number} "
        f"{'✅ TASDIQLANDI' if action == 'approve' else '❌ BEKOR QILINDI'}\n\n"
        f"Miqdor: {withdrawal.amount:.0f} {withdrawal.currency}\n"
        f"Tur: {withdrawal.withdrawal_type}"
    )
    
    try:
        asyncio.run(bot.send_message(user.telegram_id, message))
    except:
        pass
    
    db.close()
    
    return jsonify({'success': True, 'message': f'To\'lov {status}'})

# WITHDRAWAL TYPES MANAGEMENT
@app.route('/admin/withdrawal-types', methods=['GET', 'POST'])
@admin_required
def manage_withdrawal_types():
    db = SessionLocal()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            name = request.form.get('name')
            description = request.form.get('description')
            add_withdrawal_type(db, name, description)
            return jsonify({'success': True, 'message': 'Tur qo\'shildi'})
        
        elif action == 'delete':
            wtype_id = int(request.form.get('wtype_id'))
            delete_withdrawal_type(db, wtype_id)
            return jsonify({'success': True, 'message': 'Tur o\'chirildi'})
    
    wtypes = get_withdrawal_types(db)
    db.close()
    
    return render_template('admin_withdrawal_types.html', wtypes=wtypes)

# CURRENCY RATES
@app.route('/admin/currency-rates', methods=['GET', 'POST'])
@admin_required
def manage_currency_rates():
    db = SessionLocal()
    
    if request.method == 'POST':
        from_curr = request.form.get('from_currency')
        to_curr = request.form.get('to_currency')
        rate = float(request.form.get('rate'))
        wtype_id = request.form.get('wtype_id')
        wtype_id = int(wtype_id) if wtype_id else None
        
        set_currency_rate(db, from_curr, to_curr, rate, wtype_id)
        return jsonify({'success': True, 'message': 'Kurs yangilandi'})
    
    rates = db.query(CurrencyRate).all()
    wtypes = get_withdrawal_types(db)
    
    db.close()
    
    return render_template('admin_currency_rates.html', rates=rates, wtypes=wtypes)

# MESSAGE DISTRIBUTION
@app.route('/admin/messages', methods=['GET', 'POST'])
@admin_required
def send_messages():
    if request.method == 'POST':
        message_type = request.form.get('message_type')
        message = request.form.get('message')
        
        db = SessionLocal()
        users = db.query(User).all()
        
        sent = 0
        failed = 0
        
        for user in users:
            try:
                asyncio.run(bot.send_message(user.telegram_id, message))
                sent += 1
            except:
                failed += 1
        
        db.close()
        
        return jsonify({
            'success': True,
            'message': f'Yuborildi: {sent}, Muvaffaq bo\'lmadi: {failed}'
        })
    
    return render_template('admin_messages.html')

# SETTINGS
@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    db = SessionLocal()
    
    if request.method == 'POST':
        min_withdrawal = float(request.form.get('min_withdrawal'))
        max_withdrawal = float(request.form.get('max_withdrawal'))
        commission = float(request.form.get('commission'))
        referral_bonus = float(request.form.get('referral_bonus'))
        
        # Update in database
        settings_map = {
            'min_withdrawal': min_withdrawal,
            'max_withdrawal': max_withdrawal,
            'commission_percent': commission,
            'referral_bonus': referral_bonus
        }
        
        for key, value in settings_map.items():
            setting = db.query(Settings).filter(Settings.key == key).first()
            if setting:
                setting.value = str(value)
            else:
                setting = Settings(key=key, value=str(value))
                db.add(setting)
        
        db.commit()
        
        return jsonify({'success': True, 'message': 'Sozlamalar yangilandi'})
    
    db.close()
    
    return render_template('admin_settings.html', 
                         min_withdrawal=MIN_WITHDRAWAL,
                         max_withdrawal=MAX_WITHDRAWAL,
                         commission=COMMISSION_PERCENT,
                         referral_bonus=REFERRAL_BONUS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=API_PORT, debug=False)
