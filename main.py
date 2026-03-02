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
SESSION = "userbot"

GIPHY = "YLLksuIyKHZcaMKuAOYR1s27dz2uy8Xr"
COOLDOWN = 5

# ================= DATA =================
owners = {OWNER_ID}
blacklist = {OWNER_ID}

cooldowns = {}

used_havva = set()
used_mss = set()

# ================= CLIENT =================
client = TelegramClient(SESSION, API_ID, API_HASH)

# ================= KEEP ALIVE =================
app = Flask("")

@app.route("/")
def home():
    return "online"

threading.Thread(
    target=lambda: app.run(host="0.0.0.0", port=5000)
).start()

# ================= UTILS =================
def cd_left(uid):
    if uid not in cooldowns:
        return 0
    return max(0, int(COOLDOWN-(time.time()-cooldowns[uid])))

def on_cd(uid):
    return cd_left(uid) > 0

def set_cd(uid):
    cooldowns[uid]=time.time()

async def resolve_user(event, arg):
    if arg.isdigit():
        return int(arg)

    user = await client.get_entity(arg)
    return user.id

async def giphy_random(query):
    url=f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY}&q={query}&limit=50"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data=await r.json()

    gifs=[g["images"]["original"]["url"]
          for g in data["data"]]

    random.shuffle(gifs)
    return gifs

# ================= PERSONNAGES =================
HAVVA_CHAR=[
"sword maiden goblin slayer",
"erza fairytail",
"juvia fairytail",
"mirajane fairytail",
"super sonico",
"mari kurihara prison school",
"princess hibana fire force",
"camilla fire emblem",
"nico robin one piece",
"mai sakurajima",
"kyouka uzen chained soldier",
"fubuki azuma chained soldier",
"elisabeth seven deadly sins",
"merlin seven deadly sins",
"margaret seven deadly sins",
"rossweisse high school dxd",
"victoria eminence in shadow"
]

MSS_CHAR=[
"yumeko jabami",
"nelliel bleach",
"bambietta bleach",
"boa hancock",
"rin tohsaka",
"misa amane",
"ichinose classroom elite",
"kurumu kurono"
]

# ================= HAVVA =================
@client.on(events.NewMessage(pattern=r"\.havva"))
async def havva(e):

    uid=e.sender_id

    if on_cd(uid):
        await e.reply(f"attends encore {cd_left(uid)}s pour faire la commande")
        return

    set_cd(uid)

    random.shuffle(HAVVA_CHAR)

    for char in HAVVA_CHAR:
        if char not in used_havva:
            used_havva.add(char)
            gifs=await giphy_random(char+" anime gif")
            await e.reply(file=random.choice(gifs))
            return

# ================= MSS =================
@client.on(events.NewMessage(pattern=r"\.mss"))
async def mss(e):

    uid=e.sender_id

    if on_cd(uid):
        await e.reply(f"attends encore {cd_left(uid)}s pour faire la commande")
        return

    set_cd(uid)

    random.shuffle(MSS_CHAR)

    for char in MSS_CHAR:
        if char not in used_mss:
            used_mss.add(char)
            gifs=await giphy_random(char+" anime gif")
            await e.reply(file=random.choice(gifs))
            return

# ================= HENTAI =================
hentai_gifs=[
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
"https://commentseduire.net/wp-content/uploads/2017/06/hentai-gif-1.gif",
 "https://wetgif.com/wp-content/uploads/hentai-1.gif",
 "https://m1.hentaiera.com/002/wrmde0u65c/1.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/2.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/3.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/4.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/5.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/6.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/7.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/8.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/9.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/12.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/13.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/15.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/17.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/18.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/19.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/20.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/21.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/22.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/23.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/24.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/25.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/26.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/28.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/30.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/31.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/32.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/33.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/34.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/35.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/36.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/37.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/38.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/39.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/40.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/41.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/42.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/43.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/44.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/45.gif",
    "https://m1.hentaiera.com/002/wrmde0u65c/46.gif",
    "https://m4.hentaiera.com/013/zbl8pwx6im/1.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/1.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/3.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/4.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/7.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/8.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/9.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/10.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/11.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/14.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/16.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/19.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/21.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/22.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/27.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/29.gif",
    "https://m2.hentaiera.com/009/wzchv6ndpy/30.gif"
]

@client.on(events.NewMessage(pattern=r"\.hentai"))
async def hentai(e):

    if e.sender_id not in blacklist:
        return

    if on_cd(e.sender_id):
        await e.reply(f"attends encore {cd_left(e.sender_id)}s pour faire la commande")
        return

    set_cd(e.sender_id)

    msg=await e.reply(file=random.choice(hentai_gifs))
    await asyncio.sleep(7)
    await msg.delete()

# ================= KISS / SLAP =================
@client.on(events.NewMessage(pattern=r"\.(kiss|slap)(?: (.+))?"))
async def action(e):

    if e.sender_id not in blacklist:
        return

    act=e.pattern_match.group(1)
    target=e.pattern_match.group(2)

    if not target:
        await e.reply("❌ guignol mentionne quelqu’un")
        return

    if on_cd(e.sender_id):
        await e.reply(f"attends encore {cd_left(e.sender_id)}s pour faire la commande")
        return

    set_cd(e.sender_id)

    gifs=await giphy_random(f"anime {act} gif")

    sender=(await e.get_sender()).username
    emoji="💋" if act=="kiss" else "👋"

    await e.reply(f"@{sender} {act} {target} {emoji}")
    await e.reply(file=random.choice(gifs))

# ================= OWNER =================
@client.on(events.NewMessage(pattern=r"\.owner (.+)"))
async def add_owner(e):

    if e.sender_id!=OWNER_ID:
        return

    uid=await resolve_user(e,e.pattern_match.group(1))
    owners.add(uid)
    blacklist.add(uid)

    await e.reply("✅ ajouté propriétaire")

@client.on(events.NewMessage(pattern=r"\.unowner (.+)"))
async def rem_owner(e):

    if e.sender_id!=OWNER_ID:
        return

    uid=await resolve_user(e,e.pattern_match.group(1))
    owners.discard(uid)

    await e.reply("✅ retiré propriétaire")

# ================= BL =================
@client.on(events.NewMessage(pattern=r"\.bl (.+)"))
async def bl(e):

    if e.sender_id not in owners:
        return

    uid=await resolve_user(e,e.pattern_match.group(1))
    blacklist.add(uid)

    await e.reply("✅ ajouté BL")

@client.on(events.NewMessage(pattern=r"\.unbl (.+)"))
async def unbl(e):

    if e.sender_id not in owners:
        return

    uid=await resolve_user(e,e.pattern_match.group(1))
    blacklist.discard(uid)

    await e.reply("✅ retiré BL")

# ================= LIST =================
@client.on(events.NewMessage(pattern=r"\.blacklist"))
async def show(e):

    if e.sender_id not in owners:
        return

    msg="**propriétaire 🛠️**\n"

    for o in owners:
        msg+=f"@ / {o}\n"

    msg+="\n**bl list 📔**\n"

    for u in blacklist:
        if u not in owners:
            msg+=f"@ / {u}\n"

    await e.reply(msg)

# ================= RUN =================
async def main():
    await client.start()
    print("USERBOT ONLINE")
    await client.run_until_disconnected()

asyncio.run(main())
