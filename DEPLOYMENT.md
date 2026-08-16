# HydroBot Deploy Ko'rsatmasi

Ushbu ko'rsatmada HydroBot ni **Render.com** va **Neon.tech** da deploy qilishni o'rganasiz.

## 1. Telegram Bot Yaratish

### BotFather orqali Bot Token olish:
1. Telegram da `@BotFather` ni qidiring
2. `/newbot` komandasini yuboring
3. Bot nomini kiritish (masalan: "HydroBot")
4. Username kiritish (masalan: "hydrobot_test_bot")
5. **TOKEN** ni saqlang (bu kerak bo'ladi)

## 2. GitHub Repository Yaratish

### Git Repo Sozlash:
```bash
# GitHub da yangi repository yaratish (public bo'lsin)
# Keyin lokal mashinada:

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hydrobot.git
git push -u origin main
```

## 3. Neon.tech da Database Yaratish

### PostgreSQL Database:
1. https://neon.tech ga kiring va ro'yxatdan o'ting
2. Yangi project yaratish
3. Databaseni yaratish
4. **Connection String** ni saqlang (kuylarak ayniyatli bo'lsin!)

Misol:
```
postgresql://user:password@ep-xyz.neon.tech/dbname?sslmode=require
```

## 4. Render.com da Deploy

### A. Web Service (Admin Paneli)

1. https://render.com ga kiring
2. "New Web Service" bosing
3. GitHub repositoriyni ulangtiring
4. Quyidagi sozlamalarni kiritish:

**Service Settings:**
- Name: `hydrobot-api`
- Environment: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT admin:app`
- Plan: **Free** (test uchun) yoki **Paid** (production uchun)

**Environment Variables:**
```
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ADMIN_ID=YOUR_TELEGRAM_ID
DATABASE_URL=YOUR_NEON_CONNECTION_STRING
ADMIN_PASSWORD=strong_password_here
ADMIN_SECRET_KEY=some_random_secret_key
MANDATORY_CHANNELS=@channel1,@channel2
PAYMENT_CHANNEL_ID=-1001234567890
COMMISSION_PERCENT=10
REFERRAL_BONUS=5000
MIN_WITHDRAWAL=1000
MAX_WITHDRAWAL=1000000
```

Deploy qilamiz va **Deploy URL** ni saqlang.

### B. Background Worker (Bot Service)

1. "New Background Worker" bosing
2. GitHub repositoriyni ulangtiring
3. Quyidagi sozlamalarni kiritish:

**Service Settings:**
- Name: `hydrobot-bot`
- Environment: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python bot.py`
- Plan: **Free**

**Environment Variables:** (yuqoridagi bilan bir xil)

## 5. Render URL ni o'rnatish

Admin paneli URL sini olganingizdan so'ng:

**Misol:** `https://hydrobot-api.onrender.com`

`.env` faylni yangilash (agar kerak bo'lsa):
```
API_URL=https://hydrobot-api.onrender.com
```

## 6. Uptime Robot sozlash

Botni tiniq qoldirish uchun:

1. https://uptimerobot.com ga kiring
2. "Add New Monitor" bosing
3. Monitor Type: **HTTP(s)**
4. URL: `https://YOUR_ADMIN_URL.onrender.com/admin`
5. Checking Interval: **5 minutes**
6. Save

Bu har 5 minutda siteya so'rov yuboradi va Render uyg'una qo'ydiradi.

## 7. Telegram Kanallarni Sozlash

Admin panelida quyidagilarni yaratish:

### Majburiy Kanallar:
1. Telegram da kanallar yaratish (private yoki public)
2. Botni admin qilib qo'shish
3. Admin panelga kanal ID va nomini kiritish

### To'lovlar Kanali:
1. Private kanal yaratish (proof uchun)
2. Botni admin qilib qo'shish
3. Admin panelga kanal ID ni kiritish

## 8. Admin Panelni Sozlash

### Ilk Marta Kirish:
1. `https://YOUR_ADMIN_URL.onrender.com/admin/login` ga kiring
2. Parolni kiritish (**ADMIN_PASSWORD** dan)
3. Dashboard ga kirildi

### Dastlabki Sozlash:
1. **Kanallarni Sozlash** - Majburiy kanallar va to'lovlar kanali
2. **To'lov Turlari** - Karta, Nomer, Wallet va boshqalar
3. **Valyuta Kursi** - 1 GidrocoinCoin = ? Stars (misol: 1 = 1)
4. **Sozlamalar** - Min/Max yechish, komissiya, bonus

## 9. Bot Yakuniy Sozlash

### Botni /start qilish:
1. Telegram da o'zingizning botni qidiring
2. `/start` yuboring
3. Telefon raqamini tasdiqla
4. Majburiy kanallarga obuna bo'l
5. Botdan foydalanishni boshlash

### Test Withdrawal:
1. Balans yechishga berish (admin paneldan)
2. Botda pul yechishga urinish
3. Admin panelda tasdiqlash
4. To'lovlar kanalida xabar paydo bo'lishi kerak

## 10. Maxsus Sozlamalar

### Multi-Account Protection:
- Telefon raqami faqat bir accountga
- Bir IP dan ko'p accountni blokla (optional)

### Uzbek Raqami Tekshirish:
Faqat `+998` bilan boshlanadigan raqamlar qabul qilinadi

### Referal Sistema:
- Bot orqali link yuborish
- Referer hisoblanishi uchun zaruriy shartlar
- Baqasi avtomat hisoblanadi

## 11. Monitoring va Logs

### Render Logs:
1. Render dashboard da service tanlang
2. "Logs" ni bosing
3. Real-time logs ko'rish

### Database Logs:
Neon.tech dashboarddan SQL queries ni tekshirish

## 12. Xavfli Masalalar

⚠️ **MUHIM:**
- `.env` faylni GitHub ga yuborma!
- Parolni hech kimga aytma!
- Database URL ni maxfiy saqlang!
- Regular backupni olish (Neon.tech backups avtomatik)

## 13. Problem Solving

### Bot javob bermaydi:
- Render logs ni tekshir
- BOT_TOKEN to'g'ri ekanligini tekshir
- Database connection ni tekshir

### Admin paneli ochilmaydi:
- Parolni tekshir
- ADMIN_SECRET_KEY o'rnatilganligini tekshir
- Render status ni tekshir

### Withdrawal xatoligi:
- Currency rates o'rnatilganligini tekshir
- Admin panelni refresh qil
- Database connection ni tekshir

## 14. Foydali Linklar

- [Render Docs](https://render.com/docs)
- [Neon Docs](https://neon.tech/docs)
- [Python Telegram Bot](https://python-telegram-bot.readthedocs.io)
- [Flask Docs](https://flask.palletsprojects.com)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)

## 15. O'zlashtirilgan Domenimiz bo'lsa

Agar o'zingizning domeningiz bo'lsa:

1. Render da custom domain o'rnatish
2. DNS sozlamalari
3. SSL sertifikat (Render avtomatik)

---

**Tugallandi!** 🎉

Endi botingiz to'liq ishlaydi. Admin paneldan boshqaring!
