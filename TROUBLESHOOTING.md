# HydroBot - Muammoni Hal Qilish Qo'llanmasi 🔧

Ushbu qo'llanmada eng ko'p uchraydigan muammolar va ularni hal qilish yo'llari keltirilgan.

## 🔴 Bot Xatalari

### 1. "ModuleNotFoundError: No module named 'telegram'"

**Sabab:** Kutubxonalar o'rnatilmadi

**Hal:**
```bash
pip install -r requirements.txt
```

### 2. "AttributeError: 'NoneType' object has no attribute..."

**Sabab:** Database connection yo'q yoki user topilmadi

**Hal:**
```bash
# DATABASE_URL to'g'ri ekanligini tekshir
python -c "from models import SessionLocal; db = SessionLocal(); print('OK')"
```

### 3. "TelegramError: Bot token was not provided!"

**Sabab:** BOT_TOKEN .env da yo'q yoki noto'g'ri

**Hal:**
1. .env faylini ochish
2. BOT_TOKEN ni tekshir (BotFather dan saqlasangiz)
3. Bot ni restart qilish

```bash
python bot.py
```

### 4. Bot /start qilganda "Unauthorized" xatosi

**Sabab:** Bot BotFather da noto'g'ri sozlanmoqchi yoki timeout

**Hal:**
```bash
# Botni qayta ochish
# python bot.py ni stop qiling (CTRL+C)
# Keyin qayta:
python bot.py
```

### 5. "Invalid phone number" xatosi

**Sabab:** Faqat Uzbek raqamlari (+998) qabul qilinadi

**Hal:**
- Telefon raqamini +998 dan boshlash kerak
- Masalan: +998901234567
- Yoki: 998901234567

---

## 🔴 Admin Paneli Xatalari

### 1. "Address already in use" xatosi

**Sabab:** 5000 port band (boshqa dastur ishlayapti)

**Hal:**

**Option 1:** Boshqa dasturni o'chirish
```bash
# Linux/Mac: 
lsof -i :5000  # Port dan kim foydalanayotganini ko'rish
kill -9 <PID>

# Windows (Administrator):
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Option 2:** Boshqa port ishlatish
```bash
# .env da:
API_PORT=5001

# python admin.py
```

### 2. "Cannot GET /admin"

**Sabab:** Flask app ishlamayapti

**Hal:**
```bash
# Admin panel logun tekshir
python -c "from admin import app; print('OK')"

# Keyin qayta boshlash
python admin.py
```

### 3. Admin parolini unutdim

**Sabab:** ADMIN_PASSWORD .env da yo'q yoki noto'g'ri

**Hal:**
```bash
# .env ni ochish va yangilash
ADMIN_PASSWORD=new_password_here

# Admin reLogin qilish
```

### 4. "Template not found" xatosi

**Sabab:** HTML fayllar `templates/` papkasida yo'q

**Hal:**
```bash
# Templates papkasi mavjud ekanligini tekshir
ls templates/

# Agar yo'q bo'lsa, README dan fayllarni yukla
```

---

## 🔴 Database Xatalari

### 1. "psycopg2.OperationalError: could not connect to server"

**Sabab:** PostgreSQL server ishlamayapti yoki DATABASE_URL noto'g'ri

**Hal:**

**Lokal PostgreSQL:**
```bash
# Linux/Mac:
brew services start postgresql  # Mac
sudo service postgresql start   # Linux

# Windows:
# Services.msc ni ochib PostgreSQL ni topish va start qilish
```

**Neon.tech:**
```bash
# .env da DATABASE_URL tekshir
# postgresql://user:password@ep-xxx.neon.tech/dbname?sslmode=require

# Masala bo'lsa: https://neon.tech/dashboard ga kiring
```

### 2. "FATAL: password authentication failed"

**Sabab:** Database password noto'g'ri

**Hal:**
```bash
# .env da DATABASE_URL tekshir
# Format: postgresql://USERNAME:PASSWORD@HOST:PORT/DBNAME

# Password da maxsus belgisi bo'lsa, % bilan escape qil
# Masalan: pas@word -> pas%40word
```

### 3. "relation "users" does not exist"

**Sabab:** Database migratsiyasi qilmadingiz

**Hal:**
```bash
python models.py
```

### 4. "permission denied for schema public"

**Sabab:** Database user da ruxsat yo'q

**Hal:**
```bash
# psql da:
GRANT ALL PRIVILEGES ON SCHEMA public TO hydro_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hydro_user;
```

---

## 🔴 Telegram Bot Muammolari

### 1. Bot majburiy kanallarga obuna qilishni talab qilmaydi

**Sabab:** MANDATORY_CHANNELS .env da to'g'ri yozilmagan

**Hal:**
```env
# .env da:
MANDATORY_CHANNELS=@channel1,@channel2
# bo'sh joy bo'lmasin!
```

Yoki admin paneldan:
1. Kanallarni qo'shish
2. Turi: "mandatory"

### 2. "User is not a member of the channel"

**Sabab:** Bot kanalda admin emas yoki kanal topilmadi

**Hal:**
1. Kanalni tekshir (@channel_name yoki ID)
2. Botni kanal adminiga qo'shish
3. .env da MANDATORY_CHANNELS yangilash

### 3. Withdrawal xabari to'lovlar kanalida paydo bo'lmaydi

**Sabab:** PAYMENT_CHANNEL_ID noto'g'ri yoki bot admin emas

**Hal:**
1. To'lovlar kanaligni tekshir
2. Botni kanal adminiga qo'shish
3. ID ni .env dan tekshir (- yoki -100 bilan boshlashi kerak)

### 4. Referal link ishlamayapti

**Sabab:** Bot username noto'g'ri yoki referrer blok qilingan

**Hal:**
```bash
# Bot username ni tekshir:
# Bot profilda @username mavjud bo'lishi kerak

# Admin panelda referrer blok qilinganligini tekshir
```

### 5. "/start qilganda menu ko'rinmaydi"

**Sabab:** Majburiy obuna bosqichi qo'sh qilinmayapti

**Hal:**
- Mandatory kanallar mavjud ekanligini tekshir
- Bot logun tekshir
- Botni qayta boshlash

---

## 🔴 To'lov Tizimi Muammolari

### 1. "Insufficient balance" xatosi

**Sabab:** Foydalanuvchining balansi yetarli emas

**Hal:**
- Admin paneldan balans qo'shish
- Yoki referal orqali pul taklif qilish

### 2. Withdrawal type ko'rinmaydi

**Sabab:** To'lov turlari yaratilmadi

**Hal:**
Admin panelda:
1. "🏷️ To'lov Turlari" => "Qo'shish"
2. Nomi: "Kartaga"
3. Tavsif: "Bank kartasiga"
4. Save

### 3. "Invalid withdrawal address"

**Sabab:** Manzil formati noto'g'ri

**Hal:**
- Karta raqami: ****1234 (oxirgi 4 raqam)
- Telefon: +998901234567
- Wallet ID: 1234567890

### 4. Admin withdraw tasdiqlamaydi

**Sabab:** Admin paneli ishlamayapti yoki admin status yo'q

**Hal:**
1. Admin panelga kirish
2. "To'lovlar" bo'limida pending ko'rish
3. "Tasdiqlash" bosish

---

## 🟡 Performance Muammolari

### 1. "Application is slow"

**Sabab:** Database connection ko'p yoki memory o'tgan

**Hal:**
```bash
# Database ulanishni tekshir
# SQLAlchemy pool size ni qisqartir

# config.py da:
pool_size = 5
max_overflow = 10
```

### 2. "High CPU usage"

**Sabab:** Juda ko'p bot update yoki loop

**Hal:**
```bash
# bot.py ni tekshir
# Zarur bo'lmagan handler o'chirish
# Sleep() qo'shish
```

### 3. "Memory leak"

**Sabab:** Sessiya o'chirmayapti

**Hal:**
```python
# database.py da:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # MUHIM!
```

---

## 🔧 Debugging Tricks

### 1. Logging ni yoqish

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debugging info")
logger.info("Information")
logger.error("Error occurred")
```

### 2. Database sorgovini tekshirish

```bash
# Terminal da:
psql -U hydro_user -d hydrobot

# SQL:
SELECT * FROM users WHERE telegram_id = 123456;
SELECT * FROM withdrawals ORDER BY id DESC LIMIT 5;
```

### 3. Bot tokenini tekshirish

```python
import requests
token = "YOUR_BOT_TOKEN"
url = f"https://api.telegram.org/bot{token}/getMe"
response = requests.get(url)
print(response.json())
```

### 4. .env faylini tekshirish

```python
import os
from dotenv import load_dotenv

load_dotenv()
print(f"BOT_TOKEN: {os.getenv('BOT_TOKEN')}")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
```

---

## 🚀 Deploy Muammolari (Render)

### 1. "Build failed"

**Sabab:** requirements.txt o'yinda yoki Python version

**Hal:**
1. `python-version: 3.11` o'rnatilganligini tekshir
2. requirements.txt ni tekshir
3. Render logs ni ko'rish

### 2. "Bot not responding on Render"

**Sabab:** Background worker ishlamayapti

**Hal:**
1. Render dashboard da background worker topish
2. Logs tekshir
3. BOT_TOKEN va DATABASE_URL ko'rsatilganligini tekshir

### 3. Database error on Render

**Sabab:** Neon.tech connection string noto'g'ri

**Hal:**
1. Neon dashboard da connection string tekshir
2. Render environment variable yangilash
3. Service restart qilish

---

## 📞 Oxirgi Chora

Agar hech narsa ishlad qo'lsan:

### 1. Logs Okin Ko'rish
```bash
# Bot logs:
tail -f bot_output.log

# Admin logs:
tail -f admin_output.log
```

### 2. Fresh Start
```bash
# Hammasini o'chirish va yangi boshlash
rm -rf venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python models.py
python bot.py
```

### 3. GitHub Issues
- Issues ochib, muammoni batafsil yozing
- Logs ni attach qiling
- .env da sensitive ma'lumotni yozma!

### 4. Stack Overflow
- "HydroBot telegram" yoki "Python telegram bot" qidiring
- Python Telegram Bot docs ni o'qish

---

## ✅ Tekshirilgan Checklist

Muammoni hal qilingandan keyin:

- [ ] Bot javob beradi
- [ ] Admin paneli ochiladi
- [ ] Database ulanadi
- [ ] Withdrawal ishlaydi
- [ ] Kanallarga obuna tekshiriladi
- [ ] Logs xato ko'rsatmaydi

---

**Tabriklaymiz!** 🎉 Muammoni hal qildingiz!

Keyingi marta ushbu qo'llanmani onadi ko'riring.

**Happy Coding!** 💻
