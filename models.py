from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    phone_verified = Column(Boolean, default=False)
    balance = Column(Float, default=0)
    total_earned = Column(Float, default=0)
    total_withdrawn = Column(Float, default=0)
    referral_count = Column(Integer, default=0)
    active_referrals = Column(Integer, default=0)
    is_banned = Column(Boolean, default=False)
    can_refer = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    referrals = relationship("Referral", back_populates="referrer", foreign_keys="Referral.referrer_id")
    withdrawals = relationship("Withdrawal", back_populates="user")
    subscriptions = relationship("ChannelSubscription", back_populates="user")

class Referral(Base):
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="active")  # active, inactive, blocked
    created_at = Column(DateTime, default=datetime.utcnow)
    
    referrer = relationship("User", foreign_keys=[referrer_id], back_populates="referrals")

class Withdrawal(Base):
    __tablename__ = "withdrawals"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(Integer, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    currency = Column(String)  # GidrocoinCoin, Stars, etc.
    withdrawal_type = Column(String)  # Card, Number, etc.
    withdrawal_address = Column(String)  # ****1234
    status = Column(String, default="pending")  # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="withdrawals")

class WithdrawalType(Base):
    __tablename__ = "withdrawal_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CurrencyRate(Base):
    __tablename__ = "currency_rates"
    
    id = Column(Integer, primary_key=True, index=True)
    from_currency = Column(String)  # GidrocoinCoin
    to_currency = Column(String)  # Stars, UZS, etc.
    rate = Column(Float)  # 1 GidrocoinCoin = X Stars
    withdrawal_type_id = Column(Integer, ForeignKey("withdrawal_types.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, unique=True, index=True)
    channel_name = Column(String)
    channel_type = Column(String)  # mandatory, payment
    is_public = Column(Boolean, default=True)
    total_members = Column(Integer, default=0)
    added_date = Column(DateTime, default=datetime.utcnow)
    today_members = Column(Integer, default=0)

class ChannelSubscription(Base):
    __tablename__ = "channel_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    channel_id = Column(Integer, ForeignKey("channels.id"))
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="subscriptions")

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
