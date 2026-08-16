# -*- coding: utf-8 -*-
import os, re
import random
import string
import asyncio
from telethon import TelegramClient, functions
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import events
from datetime import datetime, timedelta
from telethon.tl.functions.account import GetPasswordRequest, UpdatePasswordSettingsRequest
from telethon.tl.functions.channels import EditPhotoRequest, EditTitleRequest, UpdateUsernameRequest
from telethon.tl.functions.messages import EditChatAboutRequest

# ==================== SOZLAMALAR ====================
API_ID = 26440858           # o'zingizning api_id
API_HASH = "95ce18a4bef887bd954afa18a73850fe" # o'zingizning api_hash
SESSION_DIR = "./sessions"
COUNTER_FILE = "counter.txt"
CHANNEL_FILE = "channel.txt"

async def edit_channel_settings_one_acc():
    accs = list_accounts()
    if not accs:
        print("⚠️ Avval akk qo‘shing!")
        return

    print("Qaysi akkni ishlatamiz?")
    for i, a in enumerate(accs, start=1):
        print(f"{i}. {a.replace('.session','')}")
    idx = int(input("Raqam kiriting: ")) - 1

    phone = accs[idx].replace(".session", "")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("⚠️ Akk avtorizatsiya qilinmagan!")
        await client.disconnect()
        return

    channel_link = input("🆔 Kanal username/link kiriting: ")
    try:
        entity = await client.get_entity(channel_link)
    except Exception as e:
        print(f"❌ Kanal topilmadi: {e}")
        await client.disconnect()
        return

    while True:
        print("\n=== Kanal tahriri ===")
        print("1 - Kanal nomini o‘zgartirish")
        print("2 - Tavsifni o‘zgartirish")
        print("3 - Ommaviy/Maxfiy qilish (username)")
        print("0 - Orqaga")
        tanlov = input("Tanlang: ")

        if tanlov == "1":
            new_title = input("📝 Yangi kanal nomi: ")
            try:
                await client(EditTitleRequest(entity, new_title))
                print("✅ Kanal nomi o‘zgartirildi!")
            except Exception as e:
                print(f"❌ O‘zgartirib bo‘lmadi: {e}")

        elif tanlov == "2":
            new_about = input("ℹ️ Yangi tavsif: ")
            try:
                await client(EditAboutRequest(entity, new_about))
                print("✅ Kanal tavsifi o‘zgartirildi!")
            except Exception as e:
                print(f"❌ O‘zgartirib bo‘lmadi: {e}")

        elif tanlov == "3":
            while True:
                new_username = input("📛 Username kiriting (yoki bo‘sh qoldiring maxfiy qilish uchun): ")
                if new_username == "":
                    confirm = input("Username olib tashlansinmi? (1-yo‘q, 2-ha, 3-ortga): ")
                    if confirm == "2":
                        try:
                            await client(UpdateUsernameRequest(entity, ""))
                            print("🔒 Kanal maxfiy qilindi!")
                            break
                        except Exception as e:
                            print(f"❌ O‘zgartirib bo‘lmadi: {e}")
                    elif confirm == "3":
                        break
                    else:
                        print("Bekor qilindi.")
                        break
                else:
                    try:
                        await client(UpdateUsernameRequest(entity, new_username))
                        print(f"✅ Kanal ommaviy qilindi: @{new_username}")
                        break
                    except UsernameOccupiedError:
                        print("❌ Bu username band, boshqa username kiriting!")
                    except Exception as e:
                        print(f"❌ Username o‘rnatib bo‘lmadi: {e}")
                        break

        elif tanlov == "0":
            print("⬅️ Orqaga qaytildi.")
            break
        else:
            print("❌ Noto‘g‘ri tanlov!")

    await client.disconnect()
    
async def terminate_other_sessions_one_acc():
    accs = list_accounts()
    if not accs:
        print("⚠️ Avval akk qo‘shing!")
        return

    print("Qaysi akkni ishlatamiz?")
    for i, a in enumerate(accs, start=1):
        print(f"{i}. {a.replace('.session','')}")
    idx = int(input("Raqam kiriting: ")) - 1

    phone = accs[idx].replace(".session", "")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("⚠️ Akk avtorizatsiya qilinmagan!")
        await client.disconnect()
        return

    try:
        print("🔄 Boshqa barcha qurilmalar sessiyalarini chiqarib yuborilmoqda...")
        await client(functions.auth.ResetAuthorizationsRequest())
        print("✅ Barcha boshqa sessiyalar chiqarildi! Faqat shu session qoldi.")
    except Exception as e:
        print(f"❌ Xatolik: {e}")

    await client.disconnect()
    
# ==================== COUNTER FUNKSIYALARI ====================
def get_next_counter():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("50")
        return 50
    with open(COUNTER_FILE, "r") as f:
        return int(f.read())

def increment_counter():
    c = get_next_counter() + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(c))
      
# ==================== KANAL FUNKSIYALARI ====================

async def create_channel_one_acc():
    from telethon.tl.functions.channels import CreateChannelRequest

    accs = list_accounts()
    if not accs:
        print("⚠️ Avval akk qo‘shing!")
        return

    print("Qaysi akkni ishlatamiz?")
    for i, a in enumerate(accs, start=1):
        print(f"{i}. {a.replace('.session','')}")
    idx = int(input("Raqam kiriting: ")) - 1

    phone = accs[idx].replace(".session", "")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        print("⚠️ Akk avtorizatsiya qilinmagan!")
        await client.disconnect()
        return

    title = input("📢 Kanal nomini kiriting: ")
    about = input("ℹ️ Kanal tavsifi: ")

    try:
        result = await client(CreateChannelRequest(
            title=title,
            about=about,
            broadcast=True  # Ommaviy kanal
        ))
        new_channel = result.chats[0]
        print(f"✅ Kanal yaratildi: {new_channel.title} (id: {new_channel.id})")
    except Exception as e:
        print(f"❌ Kanal yaratib bo‘lmadi: {e}")

    await client.disconnect()


async def delete_channel_one_acc():
    from telethon.tl.functions.channels import DeleteChannelRequest

    accs = list_accounts()
    if not accs:
        print("⚠️ Avval akk qo‘shing!")
        return

    print("Qaysi akkni ishlatamiz?")
    for i, a in enumerate(accs, start=1):
        print(f"{i}. {a.replace('.session','')}")
    idx = int(input("Raqam kiriting: ")) - 1

    phone = accs[idx].replace(".session", "")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("⚠️ Akk avtorizatsiya qilinmagan!")
        await client.disconnect()
        return

    channel_link = input("🆔 Kanal username/link kiriting: ")
    try:
        entity = await client.get_entity(channel_link)
        await client(DeleteChannelRequest(entity))
        print("✅ Kanal o‘chirildi!")
    except Exception as e:
        print(f"❌ Kanalni o‘chirib bo‘lmadi: {e}")

    await client.disconnect()


async def send_message_to_channel_one_acc():
    accs = list_accounts()
    if not accs:
        print("⚠️ Avval akk qo‘shing!")
        return

    print("Qaysi akkni ishlatamiz?")
    for i, a in enumerate(accs, start=1):
        print(f"{i}. {a.replace('.session','')}")
    idx = int(input("Raqam kiriting: ")) - 1

    phone = accs[idx].replace(".session", "")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("⚠️ Akk avtorizatsiya qilinmagan!")
        await client.disconnect()
        return

    chat = input("Kanal yoki guruh username/link kiriting: ")
    msg = input("📨 Yuboriladigan xabar matni: ")
    try:
        await client.send_message(chat, msg)
        print("✅ Xabar yuborildi!")
    except Exception as e:
        print(f"❌ Xabar yuborib bo‘lmadi: {e}")

    await client.disconnect()


async def join_or_leave_channel_one_acc():
    from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest

    accs = list_accounts()
    if not accs:
        print("⚠️ Avval akk qo‘shing!")
        return

    print("Qaysi akkni ishlatamiz?")
    for i, a in enumerate(accs, start=1):
        print(f"{i}. {a.replace('.session','')}")
    idx = int(input("Raqam kiriting: ")) - 1

    phone = accs[idx].replace(".session", "")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("⚠️ Akk avtorizatsiya qilinmagan!")
        await client.disconnect()
        return

    chat = input("Kanal/guruh username/link kiriting: ")
    action = input("Qo‘shilaymi yoki chiqaymi? (join/leave): ").lower()

    try:
        entity = await client.get_entity(chat)
        if action == "join":
            await client(JoinChannelRequest(entity))
            print("✅ Muvaffaqiyatli qo‘shildi!")
        elif action == "leave":
            await client(LeaveChannelRequest(entity))
            print("🚪 Guruhdan/kanaldan chiqildi.")
        else:
            print("❌ Noto‘g‘ri buyruq!")
    except Exception as e:
        print(f"❌ Amalni bajarib bo‘lmadi: {e}")

    await client.disconnect()
  
# ==================== OTP FUNKSIYASI====================

async def otp_monitor_one_acc():
    accs = [f for f in os.listdir(SESSION_DIR) if f.endswith(".session")]
    if not accs:
        print("⚠️ Akklar mavjud emas!")
        return

    print("📱 Akklar:")
    for i, a in enumerate(accs, start=1):
        print(f"{i}. {a.replace('.session','')}")
    idx = int(input("Qaysi akkni tanlaymiz? Raqam: ")) - 1
    phone = accs[idx].replace(".session","")

    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print(f"⚠️ {phone} avtorizatsiya qilinmagan! Avval login qiling.")
        return

    print(f"✅ {phone} endi OTP monitor holatida ishlaydi.")

    @client.on(events.NewMessage)
    async def handler(event):
        text = event.message.message
        print(f"📩 {phone} -> {text}")

        match = re.search(r"\b\d{4,6}\b", text)
        if match:
            print(f"✅ OTP topildi: {match.group()}")

    await client.run_until_disconnected()



async def main():
    await change_2fa_password()
    if not accs:
        print("⚠️ Akklar yo‘q!")
        return

    print("📱 Akklar ro‘yxati:")
    for i, a in enumerate(accs, start=1):
        print(f"{i}. {a.replace('.session','')}")

    idx = int(input("Raqam kiriting: ")) - 1
    if idx < 0 or idx >= len(accs):
        print("❌ Noto‘g‘ri tanlov!")
        return

    phone = accs[idx].replace(".session","")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.start(phone)

    pwd = await client(GetPasswordRequest())
    eski_parol = input("🔑 Eski 2FA parol (agar yo'q bo'lsa Enter): ")
    yangi_parol = input("🔑 Yangi 2FA parol kiriting: ")

    eski_hash = await client._client._compute_password_hash(pwd, eski_parol) if eski_parol else None
    yangi_hash = await client._client._compute_password_hash(pwd, yangi_parol)

    try:
        await client(UpdatePasswordSettingsRequest(
            password=eski_hash,
            new_settings=dict(  # <--- Endi oddiy dict ishlaydi
                new_algo=pwd.new_algo,
                new_password_hash=yangi_hash,
                hint="Parolni eslab qoling!",
                email=None
            )
        ))
        print("✅ 2FA parol muvaffaqiyatli o‘zgartirildi!")
    except Exception as e:
        print(f"❌ Xato: {e}")

    await client.disconnect()
        
# ==================== CHAT BOSHQARISH ====================

async def chat_manager_one_acc():
    accs = [f for f in os.listdir(SESSION_DIR) if f.endswith(".session")]
    if not accs:
        print("⚠️ Akklar mavjud emas!")
        return
    print("📱 Akklar:")
    for i, a in enumerate(accs, start=1):
        print(f"{i}. {a.replace('.session','')}")
    idx = int(input("Qaysi akkni tanlaymiz? Raqam: ")) - 1
    phone = accs[idx].replace(".session","")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.start(phone)
    print(f"✅ {phone} endi chat boshqarish holatida ishlaydi.")

    # Vaqt filtri
    vaqt_input = input("Qachongacha bo‘lgan xabarlar ko‘rsin? (1d,1h,1m,1.1h,23h12m): ").strip()
    delta = timedelta()
    try:
        if "d" in vaqt_input:
            delta += timedelta(days=float(vaqt_input.replace("d","").split(".")[0]))
        if "h" in vaqt_input:
            delta += timedelta(hours=float(vaqt_input.replace("h","").split(".")[0]))
        if "m" in vaqt_input:
            delta += timedelta(minutes=float(vaqt_input.replace("m","")))
    except:
        delta = timedelta(days=1)  # default 1 kun
    cutoff_time = datetime.now() - delta

    dialogs = await client.get_dialogs()
    chats = [d for d in dialogs if d.is_user or d.is_group or d.is_channel]

    for i, chat in enumerate(chats, start=1):
        print(f"{i}. {chat.name if hasattr(chat,'name') else chat.title}")

    chat_idx = int(input("Qaysi chatni boshqaramiz? Raqam: ")) - 1
    chat = chats[chat_idx]

    messages = []
    async for msg in client.iter_messages(chat, offset_date=cutoff_time):
        messages.append(msg)
    messages = messages[:50]

    print("\n📨 Oxirgi xabarlar:")
    for i, m in enumerate(messages, start=1):
        print(f"{i}. {m.sender_id}: {m.text}")

    while True:
        print("\n1. Xabar yuborish")
        print("2. Xabar o‘chirish")
        print("3. Xabar taxrirlash")
        print("4. Ortga")
        choice = input("Tanlang: ").strip()

        if choice == "1":
            text = input("📨 Yuboriladigan xabar matni: ")
            try:
                await client.send_message(chat, text)
                print("✅ Xabar yuborildi!")
            except errors.ChatAdminRequiredError:
                print("❌ Chat admin privileges kerak!")
        elif choice == "2":
            msg_idx = int(input("Qaysi xabarni o‘chirilsin? Raqam: ")) - 1
            try:
                await messages[msg_idx].delete()
                print("✅ Xabar o‘chirildi!")
            except:
                print("❌ Xabarni o‘chira olmadi!")
        elif choice == "3":
            msg_idx = int(input("Qaysi xabarni taxrirlash? Raqam: ")) - 1
            new_text = input("Yangi matn: ")
            try:
                await messages[msg_idx].edit(new_text)
                print("✅ Xabar taxrirlandi!")
            except:
                print("❌ Taxrirlash mumkin emas!")
        elif choice == "4":
            print("🔙 Ortga qaytildi.")
            break
        else:
            print("❌ Noto‘g‘ri tanlov!")
    
# ==================== KANAL FUNKSIYALARI ====================
def get_channel():
    if os.path.exists(CHANNEL_FILE):
        with open(CHANNEL_FILE, "r") as f:
            return f.read().strip()
    return None

def set_channel():
    kanal = input("Kanal username yoki linkini kiriting (@kanal yoki https://t.me/kanal): ").strip()
    if kanal:
        with open(CHANNEL_FILE, "w") as f:
            f.write(kanal)
        print(f"✅ Kanal o‘rnatildi: {kanal}")
    else:
        print("❌ Kanal kiritilmadi")

# ==================== AKK RO'YXATI ====================
def list_accounts():
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)
    return [f for f in os.listdir(SESSION_DIR) if f.endswith(".session")]

if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)

async def add_account():
    phone = input("Telefon raqam (+998901234567): ").strip()
    if not phone:
        print("❌ Telefon raqam kiritilmadi!")
        return

    session_path = os.path.join(SESSION_DIR, f"{phone}.session")
    if os.path.exists(session_path):
        print("⚠️ Bu akk allaqachon mavjud!")
        return

    client = TelegramClient(session_path, API_ID, API_HASH)
    await client.connect()

    try:
        if not await client.is_user_authorized():
            try:
                sent_code = await client.send_code_request(phone)
                code = input(f"📨 {phone} ga yuborilgan kodni kiriting: ")
                try:
                    await client.sign_in(phone, code)
                except SessionPasswordNeededError:
                    password = input("🔑 2FA parolni kiriting: ")
                    await client.sign_in(password=password)
            except PhoneNumberInvalidError:
                print("❌ Telefon raqam noto‘g‘ri yoki bloklangan!")
                await client.disconnect()
                return
        print(f"✅ {phone} muvaffaqiyatli qo‘shildi va session saqlandi!")
    except Exception as e:
        print(f"❌ Xatolik: {e}")
    finally:
        await client.disconnect()

def remove_account():
    accs = list_accounts()
    if not accs:
        print("⚠️ Akklar mavjud emas!")
        return
    print("\n📱 Akklar:")
    for i, acc in enumerate(accs, start=1):
        print(f"{i}. {acc.replace('.session','')}")
    try:
        tanlov = int(input("Qaysi akkni o‘chiramiz? (raqam): "))
        if tanlov < 1 or tanlov > len(accs):
            print("❌ Noto‘g‘ri tanlov!")
            return
    except:
        print("❌ Noto‘g‘ri tanlov!")
        return
    os.remove(os.path.join(SESSION_DIR, accs[tanlov-1]))
    print("✅ Akk o‘chirildi!")

async def go_online_interactive():
    accs = list_accounts()
    if not accs:
        print("⚠️ Akklar mavjud emas!")
        return

    selected_accounts = []

    while True:
        print("\n📱 Akklar:")
        for i, a in enumerate(accs, start=1):
            status = "✅ selected" if a in selected_accounts else ""
            print(f"{i}. {a.replace('.session','')} {status}")
        print("100. Stop va asosiy menyuga qaytish")

        try:
            idx = int(input("Qaysi akkni online qilamiz? (raqam): ")) - 1
            if idx == 99:  # 3 = stop
                print("🔴 Online funksiyadan chiqildi, asosiy menyuga qaytildi.")
                break
            if idx < 0 or idx >= len(accs):
                print("❌ Noto‘g‘ri tanlov!")
                continue
        except:
            print("❌ Noto‘g‘ri tanlov!")
            continue

        acc = accs[idx]
        if acc in selected_accounts:
            print("⚠️ Bu akk allaqachon tanlangan!")
            continue

        # Akkni online qilish
        phone = acc.replace(".session","")
        client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
        await client.connect()
        if not await client.is_user_authorized():
            print(f"⚠️ {phone} avtorizatsiya qilinmagan!")
            await client.disconnect()
            continue
        try:
            await client(functions.account.UpdateStatusRequest(offline=False))
            print(f"✅ {phone} online holatiga keldi")
            selected_accounts.append(acc)
        except Exception as e:
            print(f"❌ {phone} online bo‘la olmadi: {e}")
        finally:
            await client.disconnect()

def show_accounts():
    accs = list_accounts()
    if not accs:
        print("⚠️ Akklar mavjud emas!")
        return
    print("\n📱 Mavjud akkauntlar:")
    for i, acc in enumerate(accs, start=1):
        print(f"{i}. {acc.replace('.session','')}")

# ==================== RASM VA CAPTION ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
rasmlar = [os.path.join(BASE_DIR, f"rasm{i}.jpg") for i in range(1,11)]
captions = [f"Caption {i}" for i in range(1,11)]

# ==================== GURUH YARATISH ====================
async def create_groups(client_list, soni_per_acc):
    from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest, LeaveChannelRequest
    from telethon.tl.functions.messages import ExportChatInviteRequest

    kanal = get_channel()
    if not kanal:
        print("⚠️ Kanal o‘rnatilmagan! Kanal qo‘ying.")
        return
    counter = get_next_counter()

    for acc in client_list:
        phone = acc.replace(".session", "")
        client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
        await client.connect()

        if not await client.is_user_authorized():
            print(f"⚠️ {phone} avtorizatsiya qilinmagan!")
            await client.disconnect()
            continue

        for i in range(soni_per_acc):
            try:
                title = f"Group_{phone[-4:]}_{random.randint(1000, 9999)}"
                print(f"🔑 {phone} bilan guruh yaratilmoqda... ({i+1}/{soni_per_acc})")

                # Guruh yaratish (megagroup=True supergroup yaratadi)
                result = await client(CreateChannelRequest(
                    title=title,
                    about="Avtomatik guruh",
                    megagroup=True
                ))

                new_group = result.chats[0]

                # Botlarni guruhga qo‘shish va admin qilish
                for bot_username in ["kuynavobot", "Oxang_bot", "Tele_Save_Bot"]:
                    try:
                        await client(InviteToChannelRequest(new_group, [bot_username]))
                        print(f"✅ @{bot_username} guruhga qo‘shildi.")
                    except Exception as e:
                        print(f"⚠️ @{bot_username} ni qo‘shishda xato: {e}")

                # Link olish
                invite = await client(ExportChatInviteRequest(peer=new_group.id))
                text = f"{counter}. {invite.link}"
                counter += 1
                increment_counter()

                # Kanalga yuborish
                try:
                    await client.send_message(kanal, text)
                    print(f"📤 Link yuborildi: {text}")
                except Exception as e:
                    print(f"⚠️ Kanalga yuborib bo‘lmadi: {e}")

                # Rasm va caption yuborish
                for rasm, caption in zip(rasmlar, captions):
                    if os.path.exists(rasm):
                        await client.send_file(new_group.id, rasm, caption=caption)
                    else:
                        print(f"⚠️ {rasm} topilmadi!")

                # Guruhdan chiqish
                await client(LeaveChannelRequest(new_group.id))
                print(f"🚪 {phone} shu guruhdan chiqdi.")

            except Exception as e:
                print(f"❌ Guruh yaratib bo‘lmadi: {e}")

        await client.disconnect()

# ==================== KUZATUV FUNKSIYASI ==================
async def account_inspector():
    accs = list_accounts()
    if not accs:
        print("⚠️ Akklar mavjud emas!")
        return

    # Akk tanlash
    print("📱 Akklar:")
    for i, a in enumerate(accs, start=1):
        print(f"{i}. {a.replace('.session','')}")
    try:
        idx = int(input("Qaysi akkni tanlaymiz? Raqam: ")) - 1
        if idx < 0 or idx >= len(accs):
            print("❌ Noto‘g‘ri tanlov!")
            return
    except:
        print("❌ Noto‘g‘ri tanlov!")
        return

    phone = accs[idx].replace(".session","")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.start(phone)

    # Dialoglarni olish
    dialogs = await client.get_dialogs()
    print(f"\n📂 {phone} akkauntidagi barcha jildlar/chatlar:")
    for i, d in enumerate(dialogs, start=1):
        name = getattr(d.entity, "title", getattr(d.entity, "username", "No Name"))
        print(f"{i}. {name}")

    try:
        chat_idx = int(input("Qaysi chatni tanlaymiz? Raqam: ")) - 1
        if chat_idx < 0 or chat_idx >= len(dialogs):
            print("❌ Noto‘g‘ri tanlov!")
            await client.disconnect()
            return
    except:
        print("❌ Noto‘g‘ri tanlov!")
        await client.disconnect()
        return

    chat = dialogs[chat_idx].entity
    seven_days_ago = datetime.now() - timedelta(days=7)
    print(f"\n📨 Oxirgi 7 kunlik xabarlar ({dialogs[chat_idx].name}):\n")

    async for message in client.iter_messages(chat, offset_date=seven_days_ago):
        sender = await message.get_sender()
        sender_name = getattr(sender, "first_name", "") if sender else "Unknown"
        print(f"[{message.date}] {sender_name}: {message.text}")

    await client.disconnect()
    
# ==================== REKLAMA FUNKSIYASI ==================
async def reklama_function_one_acc():
    accs = list_accounts()
    if not accs:
        print("⚠️ Akklar mavjud emas!")
        return

    # Akk tanlash
    print("Qaysi akkni ishlatamiz?")
    for i, acc in enumerate(accs, start=1):
        print(f"{i}. {acc.replace('.session','')}")
    try:
        idx = int(input("Raqam kiriting: ")) - 1
        if idx < 0 or idx >= len(accs):
            print("❌ Noto‘g‘ri tanlov!")
            return
    except:
        print("❌ Noto‘g‘ri tanlov!")
        return

    phone = accs[idx].replace(".session","")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        print(f"⚠️ {phone} avtorizatsiya qilinmagan!")
        await client.disconnect()
        return

    # Guruhlarni so'rash
    reklama_gr_list = []
    while True:
        gr = input("Reklama yuboriladigan guruh linki yoki username (@gr): ").strip()
        if gr:
            reklama_gr_list.append(gr)
        else:
            print("❌ Guruh kiritilmadi!")
            continue
        yana = input("Yana bormi? (1 = Ha, 2 = Yo‘q): ").strip()
        if yana == "2":
            break

    # Reklama xabarini so'rash
    reklama_text = input("Reklama matnini kiriting: ").strip()
    if not reklama_text:
        print("❌ Reklama matni kiritilmadi!")
        await client.disconnect()
        return

    # Vaqt oralig'i
    while True:
        try:
            interval = int(input("Vaqt oralig‘ini sekundda kiriting (>=10): "))
            if interval < 10:
                print("❌ Kamida 10 sekund bo‘lishi kerak!")
                continue
            break
        except:
            print("❌ Noto‘g‘ri son!")

    print("🚀 Reklama boshlanmoqda...")
    sent_users = set()

    for gr in reklama_gr_list:
        try:
            entity = await client.get_entity(gr)
            participants = await client.get_participants(entity)
            random.shuffle(participants)
            for user in participants:
                if user.id in sent_users:
                    continue
                try:
                    await client.send_message(user.id, reklama_text)
                    print(f"📤 Reklama yuborildi: {user.first_name} ({user.id})")
                    sent_users.add(user.id)
                except:
                    pass
                await asyncio.sleep(interval)
        except Exception as e:
            print(f"❌ Guruhga ulanish yoki foydalanuvchilarni olishda xato: {e}")

    print("✅ Reklama tugadi.")
    await client.disconnect()
    
# ==================== STARS FUNKSIYASI ====================
async def stars_function():
    accs = list_accounts()
    if not accs:
        print("⚠️ Akklar mavjud emas!")
        return
    majburiy_kanallar = []
    while True:
        kanal = input("Majburiy kanal kiriting (@kanal): ").strip()
        if kanal:
            majburiy_kanallar.append(kanal)
        else:
            print("❌ Kanal kiritilmadi!")
            continue
        yana = input("Yana bormi? (1 = Ha, 2 = Yo‘q): ").strip()
        if yana == "2":
            break

    bot_user = input("Bot username/referal kiriting (@BotUser): ").strip()

    for acc in accs:
        phone = acc.replace(".session","")
        client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
        await client.connect()
        if not await client.is_user_authorized():
            print(f"⚠️ {phone} avtorizatsiya qilinmagan!")
            await client.disconnect()
            continue

        # Majburiy kanallarga qo‘shish
        for kanal in majburiy_kanallar:
            try:
                entity = await client.get_entity(kanal)
                await client(functions.channels.JoinChannelRequest(entity))
                print(f"✅ {phone} kanalga qo‘shildi: {kanal}")
            except Exception as e:
                print(f"❌ {phone} kanalga qo‘shilmadi {kanal}: {e}")

        # Botga referal bosish
        if bot_user:
            try:
                await client.send_message(bot_user, "/start")
                print(f"📤 {phone} botga referal bosdi: {bot_user}")
            except Exception as e:
                print(f"❌ {phone} botga bosilmadi: {e}")

        # Faqat majburiy kanallardan chiqmaydi, boshqa kanallardan chiqadi
        dialogs = await client.get_dialogs()
        for d in dialogs:
            if d.is_channel:
                username = getattr(d.entity, "username", None)
                if username and username not in [k.replace("@","") for k in majburiy_kanallar]:
                    try:
                        await client(functions.channels.LeaveChannelRequest(d.entity.id))
                        print(f"🚪 {phone} {username} kanalidan chiqdi")
                    except:
                        pass
        await client.disconnect()

# ==================== RANDOM USER FUNKSIYASI (1 akk) ====================
async def random_user_function_one_acc():
    accs = list_accounts()
    if not accs:
        print("⚠️ Akklar mavjud emas!")
        return

    print("Qaysi akkni ishlatamiz?")
    for i, acc in enumerate(accs, start=1):
        print(f"{i}. {acc.replace('.session','')}")
    try:
        idx = int(input("Raqam kiriting: ")) - 1
        if idx < 0 or idx >= len(accs):
            print("❌ Noto‘g‘ri tanlov!")
            return
    except:
        print("❌ Noto‘g‘ri tanlov!")
        return

    phone = accs[idx].replace(".session","")
    client = TelegramClient(os.path.join(SESSION_DIR, phone), API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        print(f"⚠️ {phone} avtorizatsiya qilinmagan! @PythonCodersUz")
        await client.disconnect()
        return

    # Random 5-7 harfli username tekshirish
    while True:
        username = ''.join(random.choices(string.ascii_letters, k=random.randint(5,7)))
        try:
            entity = await client.get_entity(username)
            print(f"⚠️ Username band: {username} @PyhtonCodersuz")
        except:
            print(f"✅ Bo‘sh username topildi: {username} @PythonCodersUz")
            # Shu username bilan kanal yaratish
            try:
                result = await client(functions.channels.CreateChannelRequest(
                    title=f"Channel_{username}",
                    about="Avtomatik ochilgan kanal",
                    megagroup=False
                ))
                print(f"📤 Kanal yaratildi: {username}")
            except Exception as e:
                print(f"❌ Kanal yaratib bo‘lmadi: {e}")
            break
    await client.disconnect()

# ==================== ASOS MENYU ====================
async def main():
    while True:
        print("\n=== MENYU ===")
        print("@PythonCodersUz manba, manba buzilmasin !!!")
        print("1 - Akk qo‘shish")
        print("2 - Akk o‘chirish")
        print("3 - Akklar ro‘yxati")
        print("4 - Kanal linkini sozlash / ko‘rish")
        print("5 - Hamma akkdan guruh yaratish")
        print("6 - Faqat bitta akkdan guruh yaratish")
        print("7 - Stars funksiyasi")
        print("8 - Random user funk (1 akk)")
        print("9 - Reklama funksiyasi (1 akk)")
        print("10 - Online qilish")
        print("11 - OTP funksiya")
        print("12 - kuzatuv funksiya")
        print("13 - kuzatuv + xabar boshqaruvi funksiya")
        print("14 - 2FA parolni o‘zgartirish")
        print("15 - Kanal ochish")
        print("16 - Kanal oʻchirish")
        print("17 - Kanalga xabar yuborish")
        print("18 - Kanalni tark etish")
        print("19 - Kanal sozlamalarini tahrirlash")
        print("20 - Qurilmalarni chiqarib tashlash")
        print("0 - Chiqish")
        print("@PythonCodersUz manba, manba buzilmasin !!!")

        tanlov = input("Tanlang: ")

        if tanlov == "1":
            await add_account()
        elif tanlov == "2":
            remove_account()
        elif tanlov == "3":
            show_accounts()
        elif tanlov == "4":
            kanal = get_channel()
            if kanal:
                print(f"Hozirgi kanal: {kanal}")
            if input("O‘zgartirmoqchimisiz? (ha/yo‘q): ").lower() in ["ha","h"]:
                set_channel()
        elif tanlov == "5":
            accs = list_accounts()
            if accs:
                soni = int(input("Har bitta akk nechta guruh yaratsin? (1-100): "))
                await create_groups(accs, soni)
        elif tanlov == "6":
            accs = list_accounts()
            if accs:
                print("Qaysi akkni ishlatamiz?")
                for i, a in enumerate(accs, start=1):
                    print(f"{i}. {a.replace('.session','')}")
                idx = int(input("Raqam kiriting: ")) - 1
                soni = int(input("Nechta guruh yarataylik? (1-100): "))
                await create_groups([accs[idx]], soni)
        elif tanlov == "7":
            await stars_function()
        elif tanlov == "8":
            await random_user_function_one_acc()
        elif tanlov == "9":
            await reklama_function_one_acc()
        elif tanlov == "10":
            await go_online_interactive()
        elif tanlov == "11":
           await otp_monitor_one_acc()
        elif tanlov == "12":
           await account_inspector()
        elif tanlov == "13":
           await chat_manager_one_acc()
        elif tanlov == "14":
           await change_2fa_password_one_acc()
        elif tanlov == "15":
           await create_channel_one_acc()
        elif tanlov == "16":
           await delete_channel_one_acc()
        elif tanlov == "17":
           await send_message_to_channel_one_acc()
        elif tanlov == "18":
           await join_or_leave_channel_one_acc()
        elif tanlov == "19":
           await edit_channel_settings_one_acc()
        elif tanlov == "20":
          await terminate_other_sessions_one_acc()
        elif tanlov == "0":
            print("Dasturdan chiqildi.")
            break
        else:
            print("❌ Noto‘g‘ri tanlov!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Dastur to‘xtatildi!")