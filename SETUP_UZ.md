# HydroBot - Lokal Sozlash Ko'rsatmasi 🚀

Ushbu ko'rsatmada HydroBot ni o'z kompyuteringizda sozlash va ishlatishni o'rganasiz.

## 📋 Talablar

- **Python 3.11+** ([python.org](https://www.python.org/downloads/))
- **PostgreSQL** ([postgresql.org](https://www.postgresql.org/download/)) yoki **Neon.tech** (cloud)
- **Git** ([git-scm.com](https://git-scm.com/))
- **Telegram Bot Token** (BotFather dan)
- Kod muharriri (VS Code, PyCharm, va boshqalar)

## 🔧 Setup Qadamlari

### 1. Repository ni Klonlash

```bash
# Repository ni yuklash
git clone https://github.com/YOUR_USERNAME/hydrobot.git
cd hydrobot
```

### 2. Python Virtual Environment Yaratish

```bash
# Windows:
python -m venv venv
venv\Scripts\activate

# Linux / Mac:
python3 -m venv venv
source venv/bin/activate
```

### 3. Kutubxonalarni O'rnatish

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Database Sozlash

#### A. Lokal PostgreSQL:

```bash
# PostgreSQL o'rnatish (Windows uchun installer, Linux uchun: sudo apt install postgresql)

# Database va user yaratish:
psql -U postgres

# SQL da:
CREATE DATABASE hydrobot;
CREATE USER hydro_user WITH PASSWORD 'your_secure_password';
ALTER ROLE hydro_user SET client_encoding TO 'utf8';
ALTER ROLE hydro_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hydro_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE hydrobot TO hydro_user;
\q
```

#### B. Neon.tech (Cloud - Tavsiya Qilinadi):

1. https://neon.tech ga kiring
2. Ro'yxatdan o'ting (Gmail orqali)
3. Yangi project yaratish
4. Connection string ni saqlang:
   ```
   postgresql://user:password@ep-xyz.neon.tech/hydrobot?sslmode=require
   ```

### 5. .env Faylini Yaratish

```bash
# .env.example ni .env ga ko'chirish
cp .env.example .env

# .env ni text editor da ochish va quyidagilarni qo'shish:
```

**.env fayli:**
```env
# Telegram Bot
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ADMIN_ID=YOUR_TELEGRAM_ID

# Database
DATABASE_URL=postgresql://hydro_user:your_secure_password@localhost:5432/hydrobot

# Admin Panel
ADMIN_PASSWORD=admin123
ADMIN_SECRET_KEY=your-secret-key-here

# Channels
MANDATORY_CHANNELS=@channel1,@channel2
PAYMENT_CHANNEL_ID=-1001234567890

# Settings
COMMISSION_PERCENT=10
REFERRAL_BONUS=5000
MIN_WITHDRAWAL=1000
MAX_WITHDRAWAL=1000000

# API
API_URL=http://localhost:5000
API_PORT=5000
```

### 6. Database Migratsiyasi

```bash
python models.py
```

Bu barcha jadvallarni database da yaratadi.

### 7. Botni Ishga Tushirish

```bash
# Terminal 1 - Bot:
python bot.py
```

Agar hech qanday xato bo'lmasa bot ishga tushdi.

### 8. Admin Panelini Ishga Tushirish

```bash
# Terminal 2 (yangi terminal oching):
python admin.py
```

Admin paneli quyidagi manzilda ochiladi:
```
http://localhost:5000/admin
```

## 🔐 Login Qilish

**Admin Panelga kirish:**
1. http://localhost:5000/admin/login ga kiring
2. Parolni kiritish: `admin123` (yoki .env da o'rnatgan parol)

## 🤖 Botni Telegram da Tekshirish

1. Telegram da o'zingizning botni qidiring
2. `/start` yuboring
3. Telefon raqamini tasdiqla (Uzbek raqami: +998...)
4. Majburiy kanallarga obuna bo'l
5. Botdan foydalanishni boshlash

## 📊 Admin Paneli Sozlash

### Ilk Qadamlar:

1. **📢 Kanallarni Sozlash**
   - Majburiy obuna uchun kanallar qo'shish
   - To'lovlar kanali qo'shish

2. **🏷️ To'lov Turlarini Yaratish**
   - "Kartaga" turina
   - "Nomeriga" turina
   - "Wallet" turina

3. **💱 Valyuta Kurslarini O'rnatish**
   - 1 GidrocoinCoin = 1 Star (misol)
   - Har bir tur uchun kurs

4. **⚙️ Sozlamalarni O'rnatish**
   - Min yechish: 1000
   - Max yechish: 1000000
   - Referal bonusi: 5000

## 💰 Test: Balans Qo'shish

```bash
# Python console da:
python
```

```python
from database import *
from models import SessionLocal

db = SessionLocal()
user = get_user_by_telegram_id(db, YOUR_TELEGRAM_ID)
add_balance(db, user.id, 10000)  # 10000 pul qo'shish
print(f"Yangi balans: {user.balance}")
db.close()
```

## 🧪 Test Withdrawal Jarayoni

1. Botda "Pul chiqarish" tugmasini bosing
2. To'lov turini tanlang
3. Miqdorni kiritish (masalan 1000)
4. Manzilni kiritish (masalan: +998901234567)
5. Admin panelga kiring
6. "To'lovlar" bo'limiga kiring
7. Pending to'lovlarni ko'ring
8. Tasdiqlash yoki Bekor qilish qilamiz

## 🐛 Debugging

### Logs ni Ko'rish:

```bash
# Botning logsini ko'rish (Terminal 1)
# Xatolar shu yerda ko'rinadi

# Admin panelining logsini ko'rish (Terminal 2)
# http://localhost:5000 ga so'rovlar ko'rinadi
```

### Database ni Tekshirish:

```bash
psql -U hydro_user -d hydrobot -h localhost

# SQL da:
SELECT * FROM users;
SELECT * FROM withdrawals;
SELECT * FROM channels;
\q
```

## 📝 Foydalanuvchi Tekshirish

Admin panelda:

1. "Foydalanuvchilar" bo'limiga kiring
2. Telegram ID bo'yicha qidiring
3. Quyidagi ma'lumotlarni ko'ring:
   - Balans
   - Jami ishlagan
   - Referallar
   - Ban statusi

## 🎯 Test Scenario

```
1. Botda /start bosish
2. Telefon raqamini tasdiqla
3. Majburiy kanallarga obuna bo'l
4. Pul ishlash bo'limida referal havolasi olish
5. Admin paneldan balans qo'shish
6. Pul yechishga berish
7. Admin tasdiqlashi
8. To'lovlar kanalida xabar ko'rish
9. Top reyting ni ko'rish
```

## ⚡ Keyboard Shortcuts

**Admin Panelida:**
- `CTRL+L` - Login page ga
- `CTRL+K` - Qidirish (ba'zi brauzerlar)

## 🔒 Xavfli Masalalar

- **`.env` faylini GitHub ga yuborma!** (.gitignore da allaqachon yozilgan)
- **DATABASE_URL ni himoya qil**
- **BOT_TOKEN ni maxfiy saqlang**
- **Parolni kuchli qil** (admin123 faqat test uchun)

## 🆘 Muammoni Hal Qilish

### "Database connection xatosi"
```
Sabab: DATABASE_URL noto'g'ri
Hal: .env ni tekshir va DATABASE_URL ni to'g'ri kiriting
```

### "Bot javob bermaydi"
```
Sabab: BOT_TOKEN noto'g'ri yoki bot ishlamaydi
Hal: python bot.py da consoleni tekshir
```

### "Admin paneli ochilmaydi"
```
Sabab: 5000 port band
Hal: python admin.py ni o'chirish yoki boshqa port ishlatish
```

### "Module not found"
```
Sabab: Kutubxonalar o'rnatilmadi
Hal: pip install -r requirements.txt qaytadan ishlatish
```

## 📚 Qo'shimcha Resurslar

- [Python Telegram Bot Docs](https://python-telegram-bot.readthedocs.io)
- [Flask Web Framework](https://flask.palletsprojects.com)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org)
- [PostgreSQL Docs](https://www.postgresql.org/docs)

## 🎓 Keyingi Qadamlar

Lokal test qilingandan so'ng:

1. **Render.com da Deploy** - Bosching DEPLOYMENT.md
2. **Custom Domain** - O'zingizning domenini ulangtirish
3. **SSL Sertifikat** - HTTPS sozlash
4. **Monitoring** - Uptime Robot sozlash

## ✨ Tabriklash

Tabriklaymiz! 🎉

Endi HydroBot ni o'z kompyuteringizda ishlatish mumkin. Deploy qilishga tayyorsiz bo'lsangiz, DEPLOYMENT.md ni o'qing.

**Savollar bo'lsa, GitHub Issues da yozing!**
