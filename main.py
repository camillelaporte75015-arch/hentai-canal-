import asyncio
import time
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# ================= CONFIG =================
api_id = 36767235
api_hash = "6a36bf6c4b15e7eecdb20885a13fc2d7"

client = TelegramClient("clear_userbot", api_id, api_hash)

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

# ================= COMMANDE CLEAR =================
@client.on(events.NewMessage(pattern=r"\.clear"))
async def clear_handler(event):

    # Autoriser groupes + canaux
    if not (event.is_group or event.is_channel):
        return

    sender_id = event.sender_id

    # ===== COOLDOWN =====
    remaining = check_cooldown(sender_id)
    if remaining > 0:
        await event.reply(f"⏳ veuillez patienter {remaining}s")
        return

    args = event.raw_text.split()

    if len(args) < 2:
        await event.reply("Utilisation:\n.clear 20\n.clear @username")
        return

    target = args[1]
    chat = await event.get_chat()

    # ================= CLEAR GLOBAL (CHIFFRE) =================
    if target.isdigit():

        number = int(target)

        # limite max 20
        if number > 20:
            number = 20

        deleted = 0

        async for msg in client.iter_messages(chat.id, limit=number):
            try:
                await msg.delete()
                deleted += 1
                await asyncio.sleep(0.3)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)

        total = 0
        async for _ in client.iter_messages(chat.id):
            total += 1

        await event.reply(
            f"🧹 {deleted} message(s) supprimé(s).\n\n"
            f"Il reste encore {total} message(s) sur ce canal !"
        )
        return

    # ================= CLEAR PAR @ =================
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
                await asyncio.sleep(0.3)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)

        remaining_msgs = 0
        async for _ in client.iter_messages(chat.id, from_user=entity.id):
            remaining_msgs += 1

        await event.reply(
            f"✅ Les messages de {target} ont bien été supprimés.\n\n"
            f"Il reste encore {remaining_msgs} message(s) de cette personne ici !"
        )
        return

    await event.reply("Commande invalide.")

client.start()
print("Userbot clear lancé...")
client.run_until_disconnected()
