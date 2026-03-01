import asyncio
import random
import time
from telethon import TelegramClient, events
from flask import Flask
import threading
import aiohttp

# ================= CONFIG =================
API_ID = 36767235
API_HASH = "6a36bf6c4b15e7eecdb20885a13fc2d7"

OWNER_ID = 7891919458
SESSION_NAME = "userbot_session"

GIPHY_API_KEY = "YLLksuIyKHZcaMKuAOYR1s27dz2uy8Xr"
COOLDOWN = 5

# ================= LISTES =================
owners = {OWNER_ID}
blacklist = {OWNER_ID}

cooldowns = {}
bl_added_by = {}

used_havva = set()

# ================= CLIENT =================
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ================= KEEP ALIVE =================
app = Flask("")

@app.route("/")
def home():
    return "Userbot online"

def run():
    app.run(host="0.0.0.0", port=5000)

threading.Thread(target=run).start()

# ================= UTILS =================
def cooldown_left(uid):
    if uid not in cooldowns:
        return 0
    return max(0, int(COOLDOWN - (time.time()-cooldowns[uid])))

def in_cd(uid):
    return cooldown_left(uid) > 0

def set_cd(uid):
    cooldowns[uid] = time.time()

def is_bl(uid):
    return uid in blacklist

# ================= GIPHY =================
async def giphy_search(query):
    url=f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=50"

    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data=await r.json()

    gifs=[g["images"]["original"]["url"] for g in data["data"]]

    random.shuffle(gifs)
    return gifs

# ================= HAVVA =================
@client.on(events.NewMessage(pattern=r"\.havva"))
async def havva(event):

    uid=event.sender_id

    if in_cd(uid):
        await event.reply(f"attends {cooldown_left(uid)}s")
        return

    set_cd(uid)

    gifs=await giphy_search(
        "anime swordmaiden juvia erza hibana"
    )

    for gif in gifs:
        if gif not in used_havva:
            used_havva.add(gif)
            await event.reply(file=gif)
            return

# ================= HENTAI =================
hentai_gifs = [
    # garde ta liste ici
]

@client.on(events.NewMessage(pattern=r"\.hentai"))
async def hentai(event):

    uid=event.sender_id

    if not is_bl(uid):
        return

    if in_cd(uid):
        await event.reply(f"attends {cooldown_left(uid)}s")
        return

    set_cd(uid)

    msg=await event.reply(
        file=random.choice(hentai_gifs)
    )

    await asyncio.sleep(7)
    await msg.delete()

# ================= KISS / SLAP =================
@client.on(events.NewMessage(pattern=r"\.(kiss|slap)(?: @(\w+))?"))
async def actions(event):

    uid=event.sender_id

    if not is_bl(uid):
        return

    action=event.pattern_match.group(1)
    target=event.pattern_match.group(2)

    if not target:
        await event.reply("❌ guignol mentionne quelqu’un")
        return

    if in_cd(uid):
        await event.reply(f"attends {cooldown_left(uid)}s")
        return

    set_cd(uid)

    query="anime kiss" if action=="kiss" else "anime slap"
    gifs=await giphy_search(query)

    sender=event.sender.username or uid
    emoji="💋" if action=="kiss" else "👋"

    await event.reply(
        f"@{sender} {action} @{target} {emoji}"
    )

    await event.reply(file=random.choice(gifs))

# ================= BLACKLIST =================
@client.on(events.NewMessage(pattern=r"\.bl (@?\w+|\d+)"))
async def bl(event):

    if event.sender_id not in owners:
        return

    user=event.pattern_match.group(1).replace("@","")

    try:
        user=int(user)
    except:
        pass

    blacklist.add(user)
    bl_added_by[user]=event.sender_id

    await event.reply(f"✅ {user} BL")

@client.on(events.NewMessage(pattern=r"\.unbl (@?\w+|\d+)"))
async def unbl(event):

    if event.sender_id not in owners:
        return

    user=event.pattern_match.group(1).replace("@","")

    try:
        user=int(user)
    except:
        pass

    blacklist.discard(user)
    bl_added_by.pop(user,None)

    await event.reply("✅ retiré")

# ================= OWNER =================
@client.on(events.NewMessage(pattern=r"\.owner (@?\w+|\d+)"))
async def add_owner(event):

    if event.sender_id!=OWNER_ID:
        return

    user=event.pattern_match.group(1).replace("@","")

    try:
        user=int(user)
    except:
        pass

    owners.add(user)
    await event.reply("✅ owner ajouté")

@client.on(events.NewMessage(pattern=r"\.unowner (@?\w+|\d+)"))
async def rem_owner(event):

    if event.sender_id!=OWNER_ID:
        return

    user=int(event.pattern_match.group(1).replace("@",""))
    owners.discard(user)

    await event.reply("✅ owner retiré")

# ================= LIST =================
@client.on(events.NewMessage(pattern=r"\.blacklist"))
async def show(event):

    if event.sender_id not in owners:
        return

    msg=f"**Propriétaire**\n@botassistante / {OWNER_ID}\n\n**BL bot guapo**\n"

    for u in blacklist:
        if u!=OWNER_ID:
            msg+=f"@ / {u}\n"

    await event.reply(msg)

# ================= RUN =================
async def main():
    await client.start()
    print("USERBOT ONLINE")
    await client.run_until_disconnected()

asyncio.run(main())
