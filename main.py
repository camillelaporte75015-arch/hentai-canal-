import random
import asyncio
import time
import requests

from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# =====================
# CONFIG
# =====================

API_ID = 36767235
API_HASH = "6a36bf6c4b15e7eecdb20885a13fc2d7"
SESSION = "userbot"

GIPHY_KEY = "YLLksuIyKHZcaMKuAOYR1s27dz2uy8Xr"

COOLDOWN = 5

# =====================
# HENTAI GIFS
# =====================

hentai_gifs = [
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd459eaf877.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd459f14394.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd459f6d267.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd459fc75eb.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a02bca8.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a084d62.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a0ddb2f.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a1423d8.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a19b1cb.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a1f3e10.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a258610.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a2b141b.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a3168ea.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a36f3fd.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a3c845d.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a42b35a.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a484425.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a4dcad1.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a5415e3.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a598901.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a5f1ec8.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a656046.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a6af1aa.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a712990.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a769d40.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a7c1a1c.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a825a91.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a87d47b.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a938976.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a9903a5.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45a9e8c1f.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45aa4d0de.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45aaa711e.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45ab0b8ee.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45ab635cf.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45abbc4c0.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45ac20f25.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45ac786a5.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45acd0644.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45ad346c7.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45ad8c3fd.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45ade45d4.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45ae47e32.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45ae9f066.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45af02a47.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45af5b435.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45afb3c6c.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45b017ac6.gif",
"https://s2.pictoa.com/media/galleries/296/760/2967605ffd459cac8ec/38322265ffd45b070efd.gif",
"https://www.cougarillo.com/wp-content/uploads/2023/12/porno-hentai.gif",
"https://www.cougarillo.com/wp-content/uploads/2023/12/levrette-gif-hentai.gif",
"https://www.cougarillo.com/wp-content/uploads/2023/12/gif-hentai-gros-seins.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai145.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai125.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai143.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai129.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai119.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai127.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai122.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai120.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai141.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai139.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai140.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai114.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai123.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai115.gif",
"https://www.cougarillo.com/wp-content/uploads/2024/04/gif-hentai142.gif",
"https://img2.gelbooru.com//images/40/5f/405f442f0a5b6631821708238aed7d9a.gif",
"https://img2.gelbooru.com//images/32/44/324418be5fba84ca057ce3601b944292.gif",
"https://img2.gelbooru.com//images/70/09/7009626c5baad944ab31565e9509109a.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-41.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-40.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-39.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-38.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-37.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-36.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-35.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-34.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-32.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-30.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-29.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-28.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-27.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-25.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-24.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-23.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-22.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-21.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-20.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-19.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-18.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-17.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-16.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-15.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-14.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-13.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-12.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-11.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-10.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-9.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-7.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-6.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-5.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-4.gif",
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-1.gif"
]

# =====================
# SYSTEM
# =====================

allowed_users = set()
cooldowns = {}

client = TelegramClient(SESSION, API_ID, API_HASH)

# =====================
# KEEP ALIVE
# =====================

app = Flask('')

@app.route('/')
def home():
    return "Alive"

def run():
    app.run(host="0.0.0.0", port=5000)

Thread(target=run).start()

# =====================
# COOLDOWN
# =====================

def cooldown_left(user):
    now = time.time()

    if user in cooldowns:
        left = COOLDOWN - (now - cooldowns[user])
        if left > 0:
            return int(left)

    cooldowns[user] = now
    return 0

async def anime(tag):
    url = "https://api.giphy.com/v1/gifs/search"

    r = requests.get(url, params={
        "api_key": GIPHY_KEY,
        "q": f"anime {tag}",
        "limit": 50
    }).json()

    return random.choice(r["data"])["images"]["original"]["url"]

# =====================
# BLACKLIST (= AUTORISÉS)
# =====================

@client.on(events.NewMessage(pattern=r"\.bl (.+)"))
async def bl(event):
    user = event.pattern_match.group(1).replace("@","").lower()
    allowed_users.add(user)
    await event.reply(f"✅ @{user} autorisé")

@client.on(events.NewMessage(pattern=r"\.unbl (.+)"))
async def unbl(event):
    user = event.pattern_match.group(1).replace("@","").lower()
    allowed_users.discard(user)
    await event.reply(f"❌ @{user} retiré")

@client.on(events.NewMessage(pattern=r"\.blacklist"))
async def show(event):

    if not allowed_users:
        await event.reply("Personne autorisé.")
        return

    await event.reply(
        "✅ Utilisateurs autorisés :\n" +
        "\n".join(f"@{u}" for u in allowed_users)
    )

# =====================
# CHECK ACCESS
# =====================

async def allowed(event):

    sender = await event.get_sender()
    username = sender.username.lower() if sender.username else ""

    if username not in allowed_users:
        return False

    left = cooldown_left(username)
    if left:
        await event.reply(
            f"❌ ta mere la pute t’attends {left}s"
        )
        return False

    return True

# =====================
# HENTAI (AUTO DELETE)
# =====================

@client.on(events.NewMessage(pattern=r"\.hentai"))
async def hentai(event):

    if not await allowed(event):
        return

    gif = random.choice(hentai_gifs)

    msg = await client.send_file(event.chat_id, gif)

    await asyncio.sleep(7)
    await msg.delete()

# =====================
# KISS
# =====================

@client.on(events.NewMessage(pattern=r"\.kiss"))
async def kiss(event):

    if not await allowed(event):
        return

    gif = await anime("kiss")
    await client.send_file(event.chat_id, gif)

# =====================
# SLAP
# =====================

@client.on(events.NewMessage(pattern=r"\.slap"))
async def slap(event):

    if not await allowed(event):
        return

    gif = await anime("slap")
    await client.send_file(event.chat_id, gif)

# =====================

print("✅ BOT LANCÉ")
client.start()
client.run_until_disconnected()
