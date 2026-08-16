import os
from dotenv import load_dotenv

load_dotenv()

# Bot Settings
BOT_TOKEN = os.getenv('8681119799:AAEpyFcI8tigZJQVG8VcW9aaqSJ7NydeC60')
ADMIN_ID = int(os.getenv('ADMIN_ID', '8926978756'))
OWNER_ID = int(os.getenv('OWNER_ID', '8926978756'))

# Database
DATABASE_URL = os.getenv('postgresql://neondb_owner:npg_8mtaPf6uoRZT@ep-icy-pond-b2x3o6l5-pooler.c-6.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

# Channels
MANDATORY_CHANNELS = os.getenv('MANDATORY_CHANNELS', '').split(',')
PAYMENT_CHANNEL_ID = int(os.getenv('PAYMENT_CHANNEL_ID', '0'))

# Rates
COMMISSION_PERCENT = float(os.getenv('COMMISSION_PERCENT', '10'))
REFERRAL_BONUS = float(os.getenv('REFERRAL_BONUS', '100'))

# Withdrawal Settings
MIN_WITHDRAWAL = float(os.getenv('MIN_WITHDRAWAL', '1000'))
MAX_WITHDRAWAL = float(os.getenv('MAX_WITHDRAWAL', '1000000'))

# API
API_URL = os.getenv('API_URL', 'http://localhost:5000')
API_PORT = int(os.getenv('API_PORT', '5000'))

# Uzbek Phone Numbers only
PHONE_REGEX = r'^\+?998\d{9}$'

# Multi-account Protection
DEVICE_FINGERPRINT = True
MAX_ACCOUNTS_PER_PHONE = 1
