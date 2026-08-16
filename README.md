# HydroBot - Pul Ishlash Telegram Boti

🤖 Telegram boti orqali foydalanuvchilarga pul ishlash va yechish imkoniyatini beradigan bot.

## Xususiyatlar

✅ **Referal Tizimi** - Do'stlarni taklif qilish orqali pul ishlash  
✅ **Pul Yechish** - Turli turda (Karta, Nomer, va boshqalar)  
✅ **Admin Paneli** - To'liq boshqarish paneli  
✅ **Top Reyting** - Kunlik, oylik va umumiy reyting  
✅ **Telefon Tasdiqlash** - Faqat O'zbekiston raqamlari  
✅ **Majburiy Kanallar** - Obuna shartlari  
✅ **Multi-Account Zashtita** - Telefonni ikkita marta ishlata olmaslik  

## Talablar

- Python 3.11+
- PostgreSQL (Neon.tech)
- Telegram Bot Token
- Render.com akkaunt (Deploy uchun)

## Setup

### 1. Lokal O'rnatish

```bash
# Git repositorini klonlash
git clone <your-repo>
cd hydrobot

# Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows

# Kutubxonalarni o'rnatish
pip install -r requirements.txt

# .env.example ni .env ga ko'chirish va o'zingizning ma'lumotlarni qo'shish
cp .env.example .env

# Database migratsiyasini jarayoni
python models.py

# Botni ishga tushirish
python bot.py

# Admin panelini ishga tushirish (boshqa terminalda)
python admin.py
```

### 2. Render.com da Deploy

1. GitHub repositoriyani Render ga ulangtiring
2. `render.yaml` orqali deploy qiling
3. Environment variables ni o'rnating
4. Database URL ni Neon.tech dan oling

### 3. Uptime Robot Sozlash

1. https://uptimerobot.com ga kiring
2. API orqali statusni tekshiring

## Loyiha Strukturasi

```
hydrobot/
├── bot.py              # Asosiy telegram bot
├── admin.py            # Admin paneli (Flask)
├── models.py           # Database modelları
├── database.py         # DB helper funksiyalari
├── config.py           # Konfiguratsiya
├── requirements.txt    # Python kutubxonalari
├── .env.example        # Environment template
├── Dockerfile          # Docker image uchun
├── render.yaml         # Render.com deployment
└── README.md          # Bu fayl
```

## Admin Paneli

Admin paneli http://localhost:5000/admin da mavjud

### Admin Panelida:

- **Kanallarni sozlash** - Majburiy kanallar, to'lovlar kanali
- **Statistika** - Jami ma'lumot va grafiklar
- **Foydalanuvchilar** - Qidirish, balans o'zgartirish, ban
- **To'lovlar** - Pending, tasdiqlash, bekor qilish
- **Xabar tarqatish** - Barcha foydalanuvchilarga xabar yuborish
- **Sozlamalar** - Min/Max yechish, komissiya, bonus

## Bot Komandalar

- `/start` - Botni boshlash
- Admin uchun `/admin` - Admin panelga o'tish

## Environment Variables

```env
BOT_TOKEN              # Telegram Bot Token
ADMIN_ID               # Admin Telegram ID
DATABASE_URL           # PostgreSQL connection string
ADMIN_PASSWORD         # Admin paneli uchun parol
MANDATORY_CHANNELS     # Majburiy obuna kanallari (@channel1,@channel2)
PAYMENT_CHANNEL_ID     # To'lovlar kanali ID
COMMISSION_PERCENT     # Komissiya foizi
REFERRAL_BONUS         # Referal bonusi
MIN_WITHDRAWAL         # Minimal yechish
MAX_WITHDRAWAL         # Maksimal yechish
```

## Database

Neon.tech (https://neon.tech) dan free PostgreSQL:

1. Account yaratish
2. Database yaratish
3. Connection string olib .env ga qo'shish

## Deployment Checklist

- [ ] GitHub repositoriy yaratish
- [ ] .env file sozlash
- [ ] Database yaratish (Neon.tech)
- [ ] Bot Token olish (BotFather)
- [ ] Render.com da deploy qilish
- [ ] Uptime Robot sozlash
- [ ] Majburiy kanallarni yaratish
- [ ] Admin paneldan sozlamalarni o'rnating
- [ ] Test withdrawal qilish

## Support

Savollar bo'lsa, admin bilan bog'lanib o'tishingiz mumkin.

## License

MIT License
