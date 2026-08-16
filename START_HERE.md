# 🚀 HydroBot - SHUHAM BOSHLANG!

Assalomu alaikum! 👋

Siz **HydroBot** loyihasining hamasi bitta papkada mavjud kodlarini oldingiz.
Ushbu fayl sizga boshlash uchun to'liq qo'llanma beradi.

---

## 📖 Qanday Ishlatish

### 1️⃣ Birinchi: Nima Bu Proyekt?

**`PROJECT_SUMMARY.md`** ni o'qing
- Loyiha haqida qisqa ma'lumot
- Nima qiladi, nima qila olmaydi
- Fayl struktura

```
👉 O'qing: PROJECT_SUMMARY.md
```

### 2️⃣ Ikkinchi: Lokal O'rnatish

**`SETUP_UZ.md`** ni to'liq o'qing va amal qiling

Bu faylda:
- ✅ Python o'rnatish
- ✅ Virtual environment
- ✅ Database sozlash
- ✅ Bot ishga tushirish
- ✅ Admin paneli

```bash
# Eng tezkor yo'l:
# Windows uchun:
setup.bat

# Linux/Mac uchun:
chmod +x setup.sh
./setup.sh
```

Yoki **`SETUP_UZ.md`** da qadam-qadamni o'qing.

### 3️⃣ Uchinchi: Lokal Test

Ketayotgan bo'lsa:
1. Bot Telegram da ishlaydi
2. Admin paneli http://localhost:5000/admin da ochiladi
3. Database ulanadi

Muammo bo'lsa **`TROUBLESHOOTING.md`** ni o'qing.

### 4️⃣ Chorinchi: Deploy Qilish

**`DEPLOYMENT.md`** ni o'qing

Deploy qadamlari:
- Telegram Bot Token olish
- GitHub repository
- Neon.tech database
- Render.com deploy
- Uptime Robot

```
👉 O'qing: DEPLOYMENT.md
```

---

## 📁 Loyiha Tuzilishi

Hamasi **bitta papkada** mavjud:

```
🤖 HydroBot/
│
├─ 🔧 CODE (Python fayllar)
│  ├─ bot.py              👈 Asosiy Telegram bot
│  ├─ admin.py            👈 Admin web panel
│  ├─ models.py           👈 Database jadvallar
│  ├─ database.py         👈 Database operatsiyalari
│  └─ config.py           👈 Sozlamalar
│
├─ 🌐 WEB (Admin HTML)
│  └─ templates/
│     ├─ admin_login.html
│     ├─ admin_dashboard.html
│     ├─ admin_channels.html
│     └─ admin_settings.html
│
├─ 📚 DOCUMENTATION (Qo'llanmalar - Siz o'qiyotgan fayllar)
│  ├─ README.md            👈 Asosiy info
│  ├─ PROJECT_SUMMARY.md   👈 Xulasa
│  ├─ SETUP_UZ.md         👈 Setup ko'rsatma
│  ├─ DEPLOYMENT.md       👈 Deploy qilish
│  ├─ TROUBLESHOOTING.md  👈 Muammoni hal
│  └─ START_HERE.md       👈 Bu fayl
│
├─ ⚙️ CONFIG
│  ├─ .env.example        👈 Template (Copy qiling!)
│  ├─ requirements.txt    👈 Python kutubxonalari
│  ├─ Dockerfile          👈 Docker image
│  └─ render.yaml         👈 Render deploy
│
├─ 🚀 SETUP SCRIPTS
│  ├─ setup.bat           👈 Windows setup
│  └─ setup.sh            👈 Linux/Mac setup
│
└─ 📌 GIT
   └─ .gitignore         👈 Maxfiy fayllar
```

---

## ⏱️ Vaqt Taxminiy

| Qadam | Vaqt |
|-------|------|
| Setup qilish | 15-20 daqiqa |
| Lokal test | 10-15 daqiqa |
| Database sozlash | 5-10 daqiqa |
| Deploy (Render) | 20-30 daqiqa |
| **Jami** | **1-2 soat** |

---

## ✅ Checklist - Boshlash Uchun

- [ ] `PROJECT_SUMMARY.md` - O'qildi
- [ ] `SETUP_UZ.md` - O'qildi va amal qilindi
- [ ] Python 3.11+ o'rnatildi
- [ ] Virtual environment yaratildi
- [ ] Kutubxonalar o'rnatildi
- [ ] .env fayli to'ldi (BOT_TOKEN, DATABASE_URL)
- [ ] Database migratsiyasi qilindi
- [ ] Bot lokal `python bot.py` bilan ishlaydi
- [ ] Admin paneli `http://localhost:5000/admin` da ochiladi
- [ ] Telegram bot `/start` da javob beradi

---

## 🎯 Asosiy Fayllar

### Qo'llanmalarni Qaysi Tartibda O'qish

```
1️⃣  START_HERE.md          👈 Siz hozir o'qiyotgan fayl
2️⃣  PROJECT_SUMMARY.md      👈 Loyihani tushunish
3️⃣  SETUP_UZ.md            👈 Lokal sozlash
4️⃣  README.md              👈 Asosiy hujjat
5️⃣  TROUBLESHOOTING.md     👈 Muammoni hal (kerak bo'lganda)
6️⃣  DEPLOYMENT.md          👈 Production deploy
```

### Code Fayllarini Tushunish (Qaytarilgan)

```
bot.py
├─ start() - /start komandasi
├─ earn_callback() - Pul ishlash
├─ withdraw_callback() - Pul chiqarish
├─ profile_callback() - Profil
└─ top_rating_callback() - Top reyting

admin.py
├─ /admin/login - Admin kirish
├─ /admin/channels - Kanallarni sozlash
├─ /admin/withdrawals - To'lovlarni tasdiqlash
├─ /admin/users - Foydalanuvchilar
└─ /admin/settings - Sozlamalar

models.py
├─ User - Foydalanuvchi
├─ Withdrawal - To'lovlar
├─ Channel - Kanallar
└─ CurrencyRate - Valyuta kursi

database.py
├─ add_balance() - Balans qo'shish
├─ create_withdrawal() - To'lov sorovi
├─ add_channel() - Kanal qo'shish
└─ get_top_earners() - Top reyting
```

---

## 💬 Savollar & Javoblar

### Q: Nechta papka kerak?
**A:** Faqat 1ta! Hamasi bitta papkada. `templates/` papkasi admin HTML uchun.

### Q: PostgreSQL kerakmi?
**A:** Ha, yoki cloud (Neon.tech) ishlatish mumkin.

### Q: Bot token qayerdan?
**A:** Telegram da `@BotFather` ga yozing: `/newbot`

### Q: Deploy qayerda?
**A:** Render.com + Neon.tech (cloud, oson, free)

### Q: Admin parolini untuttim?
**A:** .env ni ochib ADMIN_PASSWORD ni o'zgartiring.

### Q: Database backup?
**A:** Neon.tech avtomatik saqlaydi (free)

---

## 🚨 Muhim!

⚠️ **BEFORE DEPLOY:**
- [ ] `.env` fayini `.gitignore` da yozilgan (private bo'lsin)
- [ ] BOT_TOKEN va DATABASE_URL maxfiy saqlang
- [ ] ADMIN_PASSWORD kuchli qiling
- [ ] Faqat Uzbek raqamlarni qabul qiling (+998)

---

## 🎓 Keyingi Qadamlar

Lokal sozlash tugagandan keyin:

### Step 1: Admin Panelni O'rganish
1. http://localhost:5000/admin ga kiring
2. Kanallarni qo'shish
3. To'lov turlarini yaratish
4. Sozlamalarni o'rnatish

### Step 2: Botni Test Qilish
1. Telegram da `/start` bosish
2. Telefon tasdiqlash
3. Pul yechishga berish
4. Top reyting ko'rish

### Step 3: Deploy (Production)
1. `DEPLOYMENT.md` ni o'qish
2. Render.com ga deploy qilish
3. Uptime Robot sozlash

---

## 🔗 Muhim Linklar

| Nima | Link |
|------|------|
| Python | https://python.org |
| PostgreSQL | https://postgresql.org |
| Telegram Bot API | https://core.telegram.org/bots |
| Python Telegram Bot | https://python-telegram-bot.org |
| Render.com | https://render.com |
| Neon.tech | https://neon.tech |
| Flask | https://flask.palletsprojects.com |

---

## 📞 Support

- **GitHub Issues** - Kod muammolari
- **BotFather** - Bot sozlamasi uchun
- **Render Docs** - Deploy uchun
- **Neon Docs** - Database uchun

---

## 🎉 SHUHAM!

Siz hozir **to'liq HydroBot loyihasiga** ega bo'ldingiz!

### Ketayotgan Bosqichlar:

```
1️⃣ PROJECT_SUMMARY.md o'qing (5 min)
   ↓
2️⃣ SETUP_UZ.md amal qiling (30 min)
   ↓
3️⃣ Lokal test qiling (15 min)
   ↓
4️⃣ DEPLOYMENT.md o'qing (20 min)
   ↓
5️⃣ Render.com ga deploy (30 min)
   ↓
6️⃣ Tabriklash! 🎊
```

---

## 🙏 Shukriyalar!

Ushbu loyiha o'zingizning botingizni yasashingizga yordam beradi.

**Muvaffaqqiyatlar!** 💪

---

**Qo'shimcha Ma'lumot:**
- Barcha kod **Uzbek** va **English** izohlar bilan
- Hamma dokumentatsiya **Uzbek tilida**
- Database struktura **to'liq tafsir**
- Admin paneli **oson ta'lim**

**Boshlang! 👉 `PROJECT_SUMMARY.md` **

---

**Made with ❤️ for HydroBot Community**

*Version: 1.0.0*  
*Last Updated: 2024*
