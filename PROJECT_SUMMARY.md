# HydroBot - Loyiha Xulasasi 📋

## 📌 Nima Bu?

**HydroBot** - Telegram orqali pul ishlash va yechish tizimini taqdim qiluvchi bot.

Foydalanuvchilar:
- ✅ Do'stlarni taklif qilish orqali pul ishlash
- ✅ Turli usulda pul yechish (Karta, Nomer, Wallet)
- ✅ Kunlik/oylik/umumiy top reyting ko'rish
- ✅ Profil statistikasini o'rnatish

Admin:
- ✅ Barcha sozlamalarni boshqarish
- ✅ Foydalanuvchilarni keltirib chiqarish
- ✅ To'lovlarni tasdiqlash
- ✅ Xabar tarqatish
- ✅ Statistikalarni ko'rish

## 📁 Fayl Strukturasi (Bitta Papkada)

```
root/
├── bot.py                  # Asosiy Telegram bot
├── admin.py                # Admin paneli (Flask)
├── models.py               # Database modelları
├── database.py             # Database operatsiyalari
├── config.py               # Konfiguratsiya
├── requirements.txt        # Python kutubxonalari
├── .env.example           # Environment template
├── .gitignore             # Git ignore
├── Dockerfile             # Docker image
├── render.yaml            # Render deployment
├── setup.bat              # Windows setup
├── setup.sh               # Linux/Mac setup
│
├── README.md              # Asosiy dokumentatsiya
├── SETUP_UZ.md           # Uzbek setup ko'rsatma
├── DEPLOYMENT.md         # Deploy qilish ko'rsatma
├── PROJECT_SUMMARY.md    # Bu fayl
│
└── templates/            # Admin HTML sahifalari
    ├── admin_login.html
    ├── admin_dashboard.html
    ├── admin_channels.html
    ├── admin_settings.html
    └── ... (boshqa sahifalar)
```

## 🚀 Tezkor Boshlash

### Option 1: Avtomatik Setup

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac yoki venv\Scripts\activate (Windows)

# Kutubxonalar
pip install -r requirements.txt

# .env yaratish
cp .env.example .env
# .env ni text editor da ochib, BOT_TOKEN va DATABASE_URL qo'shish

# Database
python models.py

# Botni ishga tushirish (Terminal 1)
python bot.py

# Admin panelini ishga tushirish (Terminal 2)
python admin.py
```

## 🔧 Konfiguratsiya

`.env` faylida quyidagilarni o'rnating:

```env
# Majburiy
BOT_TOKEN=YOUR_BOT_TOKEN
ADMIN_ID=YOUR_TELEGRAM_ID
DATABASE_URL=postgresql://user:pass@localhost/hydrobot

# Admin
ADMIN_PASSWORD=admin123
ADMIN_SECRET_KEY=secret-key

# Kanallari
MANDATORY_CHANNELS=@channel1,@channel2
PAYMENT_CHANNEL_ID=-1001234567890

# Sozlamalar
MIN_WITHDRAWAL=1000
MAX_WITHDRAWAL=1000000
REFERRAL_BONUS=5000
COMMISSION_PERCENT=10
```

## 💾 Database

### Lokal PostgreSQL:
```bash
# O'rnatish va database yaratish
psql -U postgres
CREATE DATABASE hydrobot;
CREATE USER hydro_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE hydrobot TO hydro_user;
```

### Cloud (Neon.tech):
```
DATABASE_URL=postgresql://user:pass@ep-xyz.neon.tech/hydrobot?sslmode=require
```

## 🤖 Telegram Bot Qaytarilgan Funktsiyalar

### Foydalanuvchi Buttons:
- 💰 Pul ishlash - Referal havolasi va narxlar
- 💸 Pul chiqarish - To'lovlarni boshqarish
- 👤 Mening profilim - Statistika
- 🏆 Top reyting - Reyting ko'rish
- 📢 Toʻlovlar kanali - Proof kanali

### Zaruriy Shartlar:
1. **Telefon Tasdiq** - +998 bilan Uzbek raqami
2. **Majburiy Obuna** - Belgilangan kanallarga obuna
3. **Referal Cheklov** - Bir telefonda faqat 1 account
4. **Mutlaq Obuna** - Yangi kanal qo'shilsa barcha tekshir

## 🔐 Admin Paneli

**Login:** `http://localhost:5000/admin`

**Parol:** `.env` da **ADMIN_PASSWORD**

### Menyu:
- 📊 **Dashboard** - Global statistika
- 📢 **Kanallar** - Majburiy va to'lovlar kanali
- 📈 **Statistika** - Top users va grafiklari
- 👥 **Foydalanuvchilar** - Qidirish va boshqarish
- 💳 **To'lovlar** - Pending/reject/approve
- 🏷️ **To'lov Turlari** - Karta, Nomer, Wallet
- 💱 **Valyuta Kursi** - 1 Coin = ? Stars
- 📨 **Xabarlar** - Hammasiga xabar yubor
- ⚙️ **Sozlamalar** - Min/Max, komissiya, bonus

## 📊 Statistika

### User Stats:
- Balans va jami ishlagan
- Referallar soni
- Yechgan miqdori
- Bugun ishlagan referal

### Top Reyting:
- **Kunlik** - Bugun eng koʻp ishlagan
- **Oylik** - Shu oyda eng koʻp
- **Umumiy** - Hammasi moddasi

### Admin Stats:
- Jami foydalanuvchi
- Jami ishlanganlar
- Jami yechilganlar
- Pending to'lovlar

## 💳 To'lov Tizimi

### To'lov Jarayoni:
1. Foydalanuvchi miqdor kiritadi
2. Manzilni kiritadi (+998... yoki ****1234)
3. Admin panelda pending ko'rinadi
4. Admin tasdiqlaydi yoki bekor qiladi
5. To'lovlar kanalida xabar paydo bo'ladi
6. Balans yangilandi

### Supported Turlari:
- 💳 Karta - +998 raqami yoki Visa/Mastercard raqami
- 📞 Nomer - Telefon raqami
- 💰 Wallet - Click, Payme, va boshqalar
- Custom - Admin yaratgan turlari

### Exchange Rates:
Har bir to'lov turi uchun admin o'zining kursi o'rnatadi.

Misol:
- Karta: 1 GidrocoinCoin = 1000 UZS
- Stars: 1 GidrocoinCoin = 1 Star

## 🌐 Deploy Qilish

### Render.com + Neon.tech:

1. **GitHub Repository** - Kodini push qiling
2. **Neon Database** - Connection string oling
3. **Render Web Service** - Admin paneli deploy
4. **Render Background Worker** - Bot deploy
5. **Environment Variables** - .env sozlamalarini qo'shing
6. **Uptime Robot** - Bot tiniq qoldirish uchun

**Batafsilroq:** `DEPLOYMENT.md` ni o'qing

## ⚙️ Technical Stack

- **Language:** Python 3.11+
- **Bot Framework:** python-telegram-bot 20.3
- **Web Framework:** Flask 3.0
- **Database:** PostgreSQL + SQLAlchemy
- **Hosting:** Render.com
- **Database Hosting:** Neon.tech
- **ORM:** SQLAlchemy 2.0

## 📦 Kutubxonalar

```
python-telegram-bot==20.3
flask==3.0.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
gunicorn==21.2.0
requests==2.31.0
```

## 🔐 Security Features

- ✅ Uzbek raqamini tekshirish
- ✅ Multi-account protection (telefon bilan)
- ✅ Admin password
- ✅ Database enkripsiya (Neon.tech)
- ✅ HTTPS (Render.com)
- ✅ Ban sistema
- ✅ Referal cheklov

## 🐛 Debugging

### Logs ko'rish:
```bash
# Bot logs - Terminal da
# Admin logs - /admin/logs (qo'shish kerak)
```

### Database tekshirish:
```bash
psql -U hydro_user -d hydrobot
SELECT * FROM users;
SELECT * FROM withdrawals;
SELECT * FROM channels;
```

## 📚 Documentation

- **README.md** - Asosiy ma'lumot
- **SETUP_UZ.md** - Uzbek setup ko'rsatma
- **DEPLOYMENT.md** - Production deploy
- **PROJECT_SUMMARY.md** - Bu xulasa

## 🆘 Muammoni Hal Qilish

| Muammo | Sabab | Hal |
|--------|-------|-----|
| Bot javob bermaydi | BOT_TOKEN noto'g'ri | .env ni tekshir |
| Admin paneli ochilmaydi | 5000 port band | python admin.py ni o'chir |
| Database xatosi | DATABASE_URL noto'g'ri | .env ni yangilash |
| Withdrawal xatosi | Currency rates yo'q | Admin panelda rates o'rnat |
| Kanal ob subscribe bo'lmadi | Kanal ID noto'g'ri | @username yoki -1001234567890 tekshir |

## ✅ Deploy Checklist

- [ ] Python 3.11+ o'rnatildi
- [ ] PostgreSQL yoki Neon.tech database yaratildi
- [ ] Telegram Bot Token olindi (BotFather)
- [ ] .env fayli to'liq to'ldirildi
- [ ] Virtual environment yaratildi
- [ ] Kutubxonalar o'rnatildi
- [ ] Database migratsiyasi qilindi
- [ ] Bot lokal tekshirildi
- [ ] Admin paneli lokal tekshirildi
- [ ] GitHub repository yaratildi
- [ ] Render.com deploy qilindi
- [ ] Majburiy kanallar yaratildi
- [ ] Admin paneldan sozlamalar o'rnatildi
- [ ] Uptime Robot sozlandi

## 📞 Support

Savollar bo'lsa:
- GitHub Issues da yozing
- Admin paneli -> Xabar yubor

## 📄 License

MIT License - O'z ishingizga ishlating!

## 🎉 Tugallanish

Tabriklaymiz! Endi HydroBot bilan ishlashingiz mumkin.

**Quyidagi qadam: Deploy qilish uchun `DEPLOYMENT.md` ni o'qing.**

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Author:** HydroBot Team
