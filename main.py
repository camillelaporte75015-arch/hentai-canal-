import asyncio
import time
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# ================= CONFIG =================
api_id = 36767235
api_hash = "6a36bf6c4b15e7eecdb20885a13fc2d7"

client = TelegramClient("userbot", api_id, api_hash)

# ================= COOLDOWN =================
cooldowns = {}
COOLDOWN_TIME = 5

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

# ================= CLEAR =================
@client.on(events.NewMessage(pattern=r"\.clear"))
async def clear_handler(event):
    sender_id = event.sender_id

    # cooldown
    remaining = check_cooldown(sender_id)
    if remaining > 0:
        await event.reply(f"⏳ veuillez patienter {remaining}s")
        return

    args = event.raw_text.split()
    if len(args) < 2:
        await event.reply("Utilisation:\n.clear 40\n.clear @username")
        return

    target = args[1]
    chat = await event.get_chat()

    # ===== CLEAR PAR NOMBRE =====
    if target.isdigit():
        number = int(target)
        if number > 40:
            number = 40
        deleted = 0
        async for msg in client.iter_messages(chat.id, limit=number):
            try:
                await msg.delete()
                deleted += 1
                await asyncio.sleep(0.2)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
        await event.reply(f"🧹 {deleted} message(s) supprimé(s).")
        return

    # ===== CLEAR PAR USER =====
    if target.startswith("@"):
        try:
            entity = await client.get_entity(target)
        except:
            await event.reply("Utilisateur introuvable.")
            return

        deleted = 0
        async for msg in client.iter_messages(chat.id, from_user=entity.id, limit=100):
            try:
                await msg.delete()
                deleted += 1
                await asyncio.sleep(0.2)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)

        await event.reply(
            f"✅ Les messages de {target} ont bien été supprimés."
        )

# ================= NUKE =================
@client.on(events.NewMessage(pattern=r"\.nuke"))
async def nuke_handler(event):
    wait = check_cooldown(event.sender_id)
    if wait:
        await event.reply(f"⏳ veuillez patienter {wait}s")
        return

    try:
        await event.delete()
    except:
        pass

    chat = await event.get_chat()
    deleted = 0
    async for msg in client.iter_messages(chat.id, limit=None):
        try:
            await msg.delete()
            deleted += 1
            await asyncio.sleep(0.2)  # Supprime doucement pour éviter FloodWait
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)

    await client.send_message(chat.id, f"💥 Nuke terminé ! {deleted} message(s) supprimé(s).")

# ================= WAKEUP =================
@client.on(events.NewMessage(pattern=r"\.wakeup (@\S+)"))
async def wakeup(event):
    wait = check_cooldown(event.sender_id)
    if wait:
        await event.reply(f"⏳ veuillez patienter {wait}s")
        return

    user = event.pattern_match.group(1)

    try:
        await event.delete()
    except:
        pass

    # ping 10 fois avec 0.5s pause pour éviter FloodWait
    for _ in range(10):
        await client.send_message(event.chat_id, f"{user} lève toi ta mère")
        await asyncio.sleep(0.5)

# ================= START =================
client.start()
print("Userbot lancé avec say, clear (40) et wakeup + nuke !")
client.run_until_disconnected()
