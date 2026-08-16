from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import (
    User, Referral, Withdrawal, Channel, ChannelSubscription,
    WithdrawalType, CurrencyRate, Settings, SessionLocal
)

# USER FUNCTIONS
def get_or_create_user(db: Session, telegram_id: int, username: str = None, first_name: str = None):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=username, first_name=first_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

def ban_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_banned = True
        db.commit()
    return user

def unban_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_banned = False
        db.commit()
    return user

def add_balance(db: Session, user_id: int, amount: float):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.balance += amount
        user.total_earned += amount
        user.last_activity = datetime.utcnow()
        db.commit()
    return user

def subtract_balance(db: Session, user_id: int, amount: float):
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.balance >= amount:
        user.balance -= amount
        db.commit()
    return user

def disable_referral(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.can_refer = False
        db.commit()
    return user

# REFERRAL FUNCTIONS
def add_referral(db: Session, referrer_id: int, referred_user_id: int):
    existing = db.query(Referral).filter(
        Referral.referrer_id == referrer_id,
        Referral.referred_user_id == referred_user_id
    ).first()
    
    if not existing:
        referral = Referral(referrer_id=referrer_id, referred_user_id=referred_user_id)
        db.add(referral)
        
        referrer = db.query(User).filter(User.id == referrer_id).first()
        if referrer:
            referrer.referral_count += 1
            referrer.active_referrals += 1
        
        db.commit()
        return referral
    return existing

def get_referrer(db: Session, user_id: int):
    referral = db.query(Referral).filter(Referral.referred_user_id == user_id).first()
    if referral:
        return db.query(User).filter(User.id == referral.referrer_id).first()
    return None

def get_user_referrals(db: Session, user_id: int):
    return db.query(Referral).filter(Referral.referrer_id == user_id).all()

def get_active_referrals_count(db: Session, user_id: int):
    return db.query(Referral).filter(
        Referral.referrer_id == user_id,
        Referral.status == "active"
    ).count()

# WITHDRAWAL FUNCTIONS
def get_next_withdrawal_order_number(db: Session):
    last = db.query(Withdrawal).order_by(Withdrawal.order_number.desc()).first()
    return (last.order_number + 1) if last else 1

def create_withdrawal(db: Session, user_id: int, amount: float, currency: str, withdrawal_type: str, address: str):
    order_number = get_next_withdrawal_order_number(db)
    withdrawal = Withdrawal(
        order_number=order_number,
        user_id=user_id,
        amount=amount,
        currency=currency,
        withdrawal_type=withdrawal_type,
        withdrawal_address=address
    )
    db.add(withdrawal)
    db.commit()
    db.refresh(withdrawal)
    return withdrawal

def get_pending_withdrawals(db: Session):
    return db.query(Withdrawal).filter(Withdrawal.status == "pending").all()

def get_rejected_withdrawals(db: Session):
    return db.query(Withdrawal).filter(Withdrawal.status == "rejected").all()

def approve_withdrawal(db: Session, withdrawal_id: int):
    withdrawal = db.query(Withdrawal).filter(Withdrawal.id == withdrawal_id).first()
    if withdrawal:
        withdrawal.status = "approved"
        withdrawal.processed_at = datetime.utcnow()
        db.commit()
    return withdrawal

def reject_withdrawal(db: Session, withdrawal_id: int):
    withdrawal = db.query(Withdrawal).filter(Withdrawal.id == withdrawal_id).first()
    if withdrawal:
        withdrawal.status = "rejected"
        withdrawal.processed_at = datetime.utcnow()
        # Return money to user
        user = db.query(User).filter(User.id == withdrawal.user_id).first()
        if user:
            user.balance += withdrawal.amount
        db.commit()
    return withdrawal

# CHANNEL FUNCTIONS
def add_channel(db: Session, channel_id: int, channel_name: str, channel_type: str, is_public: bool = True):
    channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    if not channel:
        channel = Channel(
            channel_id=channel_id,
            channel_name=channel_name,
            channel_type=channel_type,
            is_public=is_public
        )
        db.add(channel)
        db.commit()
        db.refresh(channel)
    return channel

def get_channels_by_type(db: Session, channel_type: str):
    return db.query(Channel).filter(Channel.channel_type == channel_type).all()

def get_all_channels(db: Session):
    return db.query(Channel).all()

def delete_channel(db: Session, channel_id: int):
    channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    if channel:
        db.delete(channel)
        db.commit()
    return True

def user_subscribed_to_channel(db: Session, user_id: int, channel_id: int):
    return db.query(ChannelSubscription).filter(
        ChannelSubscription.user_id == user_id,
        ChannelSubscription.channel_id == channel_id
    ).first() is not None

def add_subscription(db: Session, user_id: int, channel_id: int):
    existing = db.query(ChannelSubscription).filter(
        ChannelSubscription.user_id == user_id,
        ChannelSubscription.channel_id == channel_id
    ).first()
    if not existing:
        sub = ChannelSubscription(user_id=user_id, channel_id=channel_id)
        db.add(sub)
        db.commit()

# WITHDRAWAL TYPE FUNCTIONS
def get_withdrawal_types(db: Session):
    return db.query(WithdrawalType).filter(WithdrawalType.is_active == True).all()

def add_withdrawal_type(db: Session, name: str, description: str = None):
    wtype = WithdrawalType(name=name, description=description)
    db.add(wtype)
    db.commit()
    db.refresh(wtype)
    return wtype

def delete_withdrawal_type(db: Session, wtype_id: int):
    wtype = db.query(WithdrawalType).filter(WithdrawalType.id == wtype_id).first()
    if wtype:
        wtype.is_active = False
        db.commit()

# CURRENCY RATE FUNCTIONS
def set_currency_rate(db: Session, from_curr: str, to_curr: str, rate: float, wtype_id: int = None):
    existing = db.query(CurrencyRate).filter(
        CurrencyRate.from_currency == from_curr,
        CurrencyRate.to_currency == to_curr,
        CurrencyRate.withdrawal_type_id == wtype_id
    ).first()
    
    if existing:
        existing.rate = rate
        existing.updated_at = datetime.utcnow()
    else:
        existing = CurrencyRate(
            from_currency=from_curr,
            to_currency=to_curr,
            rate=rate,
            withdrawal_type_id=wtype_id
        )
        db.add(existing)
    
    db.commit()
    db.refresh(existing)
    return existing

def get_currency_rate(db: Session, from_curr: str, to_curr: str, wtype_id: int = None):
    return db.query(CurrencyRate).filter(
        CurrencyRate.from_currency == from_curr,
        CurrencyRate.to_currency == to_curr,
        CurrencyRate.withdrawal_type_id == wtype_id
    ).first()

# STATISTICS FUNCTIONS
def get_user_stats(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    referral_count = get_active_referrals_count(db, user_id)
    today_referrals = db.query(Referral).filter(
        Referral.referrer_id == user_id,
        Referral.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    ).count()
    
    return {
        'user_id': user.id,
        'telegram_id': user.telegram_id,
        'username': user.username,
        'balance': user.balance,
        'total_earned': user.total_earned,
        'total_withdrawn': user.total_withdrawn,
        'referral_count': referral_count,
        'active_referrals': user.active_referrals,
        'today_referrals': today_referrals
    }

def get_top_earners(db: Session, period: str = 'all', limit: int = 10):
    """Get top earners - period: 'today', 'month', 'all'"""
    if period == 'today':
        start_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'month':
        start_date = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_date = None
    
    query = db.query(User).order_by(User.total_earned.desc())
    if start_date:
        query = query.filter(User.last_activity >= start_date)
    
    return query.limit(limit).all()

def get_top_withdrawers(db: Session, period: str = 'all', limit: int = 10):
    """Get top withdrawers - period: 'today', 'month', 'all'"""
    if period == 'today':
        start_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'month':
        start_date = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_date = None
    
    query = db.query(User).order_by(User.total_withdrawn.desc())
    if start_date:
        query = query.filter(User.last_activity >= start_date)
    
    return query.limit(limit).all()

def get_global_stats(db: Session):
    total_users = db.query(User).count()
    total_earned = db.query(User).with_entities(db.func.sum(User.total_earned)).scalar() or 0
    total_withdrawn = db.query(Withdrawal).filter(Withdrawal.status == "approved").with_entities(
        db.func.sum(Withdrawal.amount)
    ).scalar() or 0
    pending_withdrawals = db.query(Withdrawal).filter(Withdrawal.status == "pending").count()
    
    return {
        'total_users': total_users,
        'total_earned': total_earned,
        'total_withdrawn': total_withdrawn,
        'pending_withdrawals': pending_withdrawals
    }
