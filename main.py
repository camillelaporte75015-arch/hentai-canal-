import asyncio
import time
import random
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# ================= CONFIG =================
api_id = 36767235
api_hash = "6a36bf6c4b15e7eecdb20885a13fc2d7"

client = TelegramClient("userbot", api_id, api_hash)

# ================= VARIABLES =================
cooldowns = {}
COOLDOWN_TIME = 5

STOP_CLEAR = False
deleted_count = 0

media_cooldown = 0

# ================= GIFS =================
HAVVA_GIFS = ["gif1.gif", "gif2.gif", "gif3.gif"]   # tes gifs havva
HENTAI_GIFS = ["anime1.gif", "anime2.gif", "anime3.gif"]  # pas de vrai hentai, juste anime safe

# ================= COOLDOWN =================
def check_cooldown(user_id):
    now = time.time()
    if user_id in cooldowns:
        remaining = COOLDOWN_TIME - (now - cooldowns[user_id])
        if remaining > 0:
            return int(remaining)
    cooldowns[user_id] = now
    return 0

# ================= SAY =================
@client.on(events.NewMessage(pattern=r"\.say (.+)"))
async def say(event):
    text = event.pattern_match.group(1)
    try:
        await event.delete()
    except:
        pass
    await client.send_message(event.chat_id, text)

# ================= RAID =================
@client.on(events.NewMessage(pattern=r"\.raid (@\S+)"))
async def raid(event):
    user = event.pattern_match.group(1)
    try:
        await event.delete()
    except:
        pass

    messages = [
        f"{user} réveille toi",
        f"{user} t'es mort ?",
        f"{user} répond",
        f"{user} on t'attend",
        f"{user} WAKE UP"
    ]

    for msg in messages:
        await client.send_message(event.chat_id, msg)
        await asyncio.sleep(0.4)

# ================= WAKEUP =================
@client.on(events.NewMessage(pattern=r"\.wakeup (@\S+)"))
async def wakeup(event):
    user = event.pattern_match.group(1)
    try:
        await event.delete()
    except:
        pass

    async def ping_loop():
        for _ in range(10):
            try:
                await client.send_message(event.chat_id, f"{user} lève toi ta mère")
                await asyncio.sleep(0.5)
            except FloodWaitError as e:
                await client.send_message(event.chat_id, f"⏸ pause {e.seconds}s")
                await asyncio.sleep(e.seconds)

    asyncio.create_task(ping_loop())

# ================= MEDIA GENERIC FUNCTION =================
async def send_media(event, media_list):
    global media_cooldown
    now = time.time()
    if now - media_cooldown < 4:
        return
    media_cooldown = now

    gif = random.choice(media_list)

    try:
        await event.delete()
    except:
        pass

    msg = await client.send_file(event.chat_id, gif)
    await asyncio.sleep(5)
    try:
        await msg.delete()
    except:
        pass

# ================= HAVVA =================
@client.on(events.NewMessage(pattern=r"\.havva"))
async def havva(event):
    await send_media(event, HAVVA_GIFS)

# ================= HENTAI =================
@client.on(events.NewMessage(pattern=r"\.hentai"))
async def hentai(event):
    await send_media(event, HENTAI_GIFS)

# ================= STOP =================
@client.on(events.NewMessage(pattern=r"\.stop"))
async def stop(event):
    global STOP_CLEAR
    global deleted_count

    STOP_CLEAR = True

    chat = await event.get_chat()

    last_msg = await client.get_messages(chat.id, limit=1)
    remaining = last_msg[0].id if last_msg else 0

    await event.reply(
        f"⛔ clear arrêté\n\n"
        f"j’ai supprimé {deleted_count} message(s)\n"
        f"il reste environ {remaining} message(s) dans ce canal"
    )

# ================= CLEAR =================
@client.on(events.NewMessage(pattern=r"\.clear"))
async def clear_handler(event):
    global STOP_CLEAR
    global deleted_count

    STOP_CLEAR = False
    deleted_count = 0

    args = event.raw_text.split()
    if len(args) < 2:
        return

    number = int(args[1])
    if number > 40:
        number = 40

    chat = await event.get_chat()
    async for msg in client.iter_messages(chat.id, limit=number):
        if STOP_CLEAR:
            break
        try:
            await msg.delete()
            deleted_count += 1
            await asyncio.sleep(0.2)
        except FloodWaitError as e:
            await client.send_message(chat.id, f"pause {e.seconds}s")
            await asyncio.sleep(e.seconds)

# ================= NUKE =================
@client.on(events.NewMessage(pattern=r"\.nuke"))
async def nuke_handler(event):
    global STOP_CLEAR
    global deleted_count

    STOP_CLEAR = False
    deleted_count = 0

    try:
        await event.delete()
    except:
        pass

    async def nuke_loop():
        chat = await event.get_chat()
        async for msg in client.iter_messages(chat.id):
            if STOP_CLEAR:
                break
            try:
                await msg.delete()
                deleted_count += 1
                await asyncio.sleep(0.2)
            except FloodWaitError as e:
                await client.send_message(chat.id, f"pause {e.seconds}s")
                await asyncio.sleep(e.seconds)

    asyncio.create_task(nuke_loop())

# ================= START =================
client.start()
print("Userbot lancé avec say, clear, nuke, stop, wakeup, raid, havva et hentai !")
client.run_until_disconnected()
