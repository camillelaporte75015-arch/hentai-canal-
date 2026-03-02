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

owners={OWNER_ID}
blacklist={OWNER_ID}
cooldowns={}

# ================= CLIENT =================
client=TelegramClient(SESSION,API_ID,API_HASH)

# ================= KEEP ALIVE =================
app=Flask("")

@app.route("/")
def home():
    return "online"

threading.Thread(
    target=lambda: app.run(host="0.0.0.0",port=5000)
).start()

# ================= GIFS =================

havva_gifs=[
"https://media1.tenor.com/m/LNZFR9avDkQAAAAd/anime-goblin.gif",
"https://64.media.tumblr.com/9ab9f749f74da4d7c8a3bc0ee664b87d/f0357f052aaf7e93-bd/s540x810/d649c09f79bdbef721928b79a5062b0c64e18672.gif",
"https://64.media.tumblr.com/78ac1cbebb39eba62aba91f2d153fe03/f0357f052aaf7e93-88/s540x810/8f34d3d77fc583615303f7789232edd1ffc4fb71.gif",
"https://64.media.tumblr.com/2b1c2523d3d2a46516a984cd9118b74d/f0357f052aaf7e93-27/s640x960/820c39b1847b5d7c40ea41bfbd76bfff264b2d3a.gif",
"https://64.media.tumblr.com/1f55e704017af977b8693889ed1a1a9e/f0357f052aaf7e93-ce/s540x810/36cb824edb1f39d59c781f131ee198dadd5eacf6.gif",
"https://64.media.tumblr.com/fde1d3b3542b0dcf4c8344661f3956ad/f0357f052aaf7e93-f1/s640x960/64ed1b5af03e5c9fd7b06aa04a1a681264222e37.gif",
"https://i.imgur.com/xB308Yj.gif",
"https://animesher.com/orig/2/210/2100/21004/animesher.com_sword-maiden-goblin-slayer-gif-2100449.gif",
"https://animesher.com/orig/2/212/2121/21218/animesher.com_gif-goblin-slayer-anime-girl-2121854.gif",
"https://animesher.com/orig/2/212/2121/21218/animesher.com_anime-girl-gif-goblin-slayer-2121851.gif",
"https://animesher.com/orig/2/212/2121/21218/animesher.com_anime-girl-gif-goblin-slayer-2121850.gif",
"https://animesher.com/orig/2/212/2121/21218/animesher.com_goblin-slayer-gif-inspiration-2121849.gif",
"https://animesher.com/orig/2/212/2121/21218/animesher.com_inspiration-goblin-slayer-gif-2121848.gif",
"https://animesher.com/orig/2/212/2121/21218/animesher.com_goblin-slayer-gif-2121847.gif",
"https://animesher.com/orig/2/212/2121/21218/animesher.com_gif-goblin-slayer-anime-girl-2121846.gif",
"https://animesher.com/orig/2/212/2121/21218/animesher.com_gif-anime-girl-goblin-slayer-2121845.gif",
"https://animesher.com/orig/2/212/2121/21218/animesher.com_gif-goblin-slayer-2121844.gif",
"https://animesher.com/orig/2/212/2121/21218/animesher.com_gif-anime-girl-goblin-slayer-2121843.gif",
"https://i.pinimg.com/originals/c8/18/2f/c8182f1b51d97b9bdee71a39e5a01f24.gif",
"https://i.pinimg.com/originals/b3/24/98/b32498b3f1cf2068dcbfad9379ac2b4e.gif",
"https://i.pinimg.com/originals/69/39/2c/69392cab3d63300d16cb3d3f3977cdf9.gif",
"https://media1.tenor.com/m/jUihEwTQbsQAAAAC/erza-erza-scarlet.gif",
"https://media1.tenor.com/m/E70kKlPKWwkAAAAd/erza-scarlet-erza.gif",
"https://media1.tenor.com/m/u89cN-Ec_XUAAAAd/erza-erza-scarlet.gif",
"https://media1.tenor.com/m/hZxwGUjcx6gAAAAC/erza-erza-scarlet.gif",
"https://media1.tenor.com/m/Qtoq_kzFKHAAAAAC/erza-erza-scarlet.gif",
"https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYW4xYTltNm96MW9leG84a281ZG82ZGF1cWhsMWYwazFkNmF0dW9ubSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/6ebDLRv1gMKM8/giphy.gif",
"https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUybnd2bTg2YjFmaXg5ODR5c2IzeHo2Z2dmMzhzeWlkb2lrMGFzZWxzbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bqUlSwVBKwt4k/giphy.gif",
"https://media4.giphy.com/media/v1.Y2lkPTZjMDliOTUyYTJ5cW80dXVlYWw0bzhjbnM5ZXByZjh3NTJ4bmRjd2FzbWpyaGl6byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6ebDLRv1gMKM8/giphy.gif",
"https://ekladata.com/NVtGa8STD1vFEgKZ65x7M6Ya8Zk.gif",
"https://media.tenor.com/SmC5VuEUjNoAAAAM/fairy-tail-erza-scarlet.gif",
"https://media.tenor.com/y-NVGA6m5mIAAAAM/erza-scarlet-fairy-tail.gif",
"https://media1.tenor.com/m/y3F3W2y-oOUAAAAd/natsu-erza.gif",
"https://media1.tenor.com/m/WL6s-zWoPtAAAAAC/juvia-juvia-lockser.gif"
"https://media1.tenor.com/m/WL6s-zWoPtAAAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/h8ScQjGETB0AAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/14HyJSsUM6EAAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/9tvycQFqs1AAAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/k4KkgFxJ71gAAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/JRz5qqG9JVkAAAAC/gray-gray-fullbuster.gif",
"https://media1.tenor.com/m/EPCfd9dUp_cAAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/VUlwW8qmJfEAAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/Pe8-JiQKDuoAAAAC/gray-juvia.gif",
"https://media1.tenor.com/m/33iXQ1Svy6gAAAAd/gray-juvia.gif",
"https://media1.tenor.com/m/l5u3PAb0Tu0AAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/6bxpy1fzdlcAAAAd/juvia-gray.gif",
"https://media1.tenor.com/m/pSU5wX8A7Z8AAAAC/gray-gray-fullbuster.gif",
"https://media1.tenor.com/m/bW48xc4cfW8AAAAd/gray-juvia.gif",
"https://media1.tenor.com/m/7K6nvxRymsUAAAAC/juvia-gray.gif",
"https://media1.tenor.com/m/H8l1pgrvD_oAAAAd/juvia-gray.gif",
"https://media1.tenor.com/m/WrNzOyQJeRAAAAAC/gray-gray-fullbuster.gif",
"https://media1.tenor.com/m/ubausj3_AC8AAAAC/gray-gray-fullbuster.gif",
"https://media1.tenor.com/m/4ZiZbxlE7nIAAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/4YN3oPxfuH4AAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/xXWrDcnUYfkAAAAC/juvia-gray.gif",
"https://media1.tenor.com/m/SmC5VuEUjNoAAAAd/fairy-tail-erza-scarlet.gif",
"https://media1.tenor.com/m/uEKm3KVdH58AAAAC/erza-erza-knightwalker.gif",
"https://media1.tenor.com/m/6OGD3QN55qQAAAAC/erza-erza-scarlet.gif",
"https://media1.tenor.com/m/ZyYbQYqf61oAAAAC/erza-erza-scarlet.gif",
"https://media1.tenor.com/m/dPTXhlBruIEAAAAC/erza-erza-scarlet.gif",
"https://media1.tenor.com/m/yeYPW5t6hwEAAAAd/erza-erza-knightwalker.gif",
"https://media1.tenor.com/m/WLShWwMLD8kAAAAC/juvia-juvia-lockser.gif",
"https://media1.tenor.com/m/kL8mlgncWGAAAAAC/erza-erza-scarlet.gif",
"https://media1.tenor.com/m/WMBra4P1YQcAAAAC/fairy-tail-anime.gif",
"https://media1.tenor.com/m/lfpoq9pfvlIAAAAC/erza-mirajane.gif",
"https://media1.tenor.com/m/0VjN2FEpHaUAAAAC/erza-erza-scarlet.gif",
"https://media1.tenor.com/m/cqKoOfhg54gAAAAC/natsu-natsu-dragneel.gif",
"https://media1.tenor.com/m/G-ugxocvvIAAAAAC/jellal-erza.gif",
"https://media1.tenor.com/m/5oNWUNnLep0AAAAC/juvia-erza.gif",
"https://media1.tenor.com/m/m6m1BUcMqDsAAAAC/erza-erza-scarlet.gif",
"https://media1.tenor.com/m/MhL--4WZ59MAAAAC/erza-erza-scarlet.gif",
"https://media1.tenor.com/m/c5hzNKgKiBkAAAAC/erza-erza-scarlet.gif",
"https://i.imgur.com/xB308Yj.gif",
"https://media1.tenor.com/m/XlCYcVw7hs8AAAAd/mirajane-mira.gif",
"https://media1.tenor.com/m/jdcwIxGCeeYAAAAd/mira-mirajane.gif",
"https://media1.tenor.com/m/1zPucZOuKzkAAAAd/mira-mira-jane.gif",
"https://media1.tenor.com/m/LO4ay9jvc7UAAAAd/mirajane-mirajane-strauss.gif",
"https://media1.tenor.com/m/uuJpQBBlKNwAAAAd/mirajane-fairy-tail.gif",
"https://media1.tenor.com/m/3ee_RbgYOrYAAAAd/mirajane-mirajane-strauss.gif",
"https://media1.tenor.com/m/0w_I3v4GPl0AAAAd/lisanna-lisanna-strauss.gif",
"https://media1.tenor.com/m/RMcG_fM5brkAAAAd/mirajane-mirajane-strauss.gif",
"https://media1.tenor.com/m/p1lH8QT0MpMAAAAd/mirajane-mirajane-strauss.gif",
"https://media1.tenor.com/m/QNx_W6uTpTIAAAAd/mirajane-mirajane-strauss.gif",
"https://media1.tenor.com/m/RtjuJFMtmWwAAAAd/mirajane-mirajane-strauss.gif",
"https://media1.tenor.com/m/-B3LLW966pIAAAAd/mirajane-fairy-tail.gif",
"https://media1.tenor.com/m/HiiAHKtOuMsAAAAd/lisanna-lisanna-strauss.gif",
"https://media1.tenor.com/m/kzyr7A5g2kUAAAAd/lisanna-mirajane.gif",
"https://media1.tenor.com/m/GAvydp9Jh2sAAAAd/mirajane-mirajane-strauss.gif",
"https://media1.tenor.com/m/JNH5q7j1dQYAAAAd/mirajane-lisanna.gif",
"https://media1.tenor.com/m/USlnAyl6VhQAAAAd/mirajane-lisanna.gif"
"https://media1.tenor.com/GLrB5-BLTt8AAAAd/fairy-tail.gif",
"https://media1.tenor.com/yELzaQnFQcEAAAAd/mirajane-lisanna.gif",
"https://media1.tenor.com/otZk_8yofWcAAAAd/mira-cana.gif",
"https://media1.tenor.com/l6BzipnbIZMAAAAd/mirajane-mirajane-strauss.gif",
"https://media1.tenor.com/_JEniyMT-VwAAAAC/mirajane-mirajane-strauss.gif",
"https://media1.tenor.com/MgG05kCDC9sAAAAC/mirajane-fairy-tail.gif",
"https://media1.tenor.com/tuHjpSZ_K7IAAAAC/super-sonico-soniani.gif",
"https://media1.tenor.com/Wb48pJc69fEAAAAC/super-sonico-soniani.gif",
"https://media1.tenor.com/chkZ6YWIKzYAAAAC/super-sonico-anime.gif",
"https://media1.tenor.com/H3XNgz040zkAAAAC/bisous.gif",
"https://media1.tenor.com/DisM3WC9QrwAAAAC/super-sonico.gif",
"https://media1.tenor.com/oZTqHzB-Fd8AAAAC/super-sonico-soniani.gif",
"https://media1.tenor.com/yS5S0c6zHycAAAAC/super-sonico-soniani.gif",
"https://media1.tenor.com/6yI58CI-BO0AAAAd/sonico-anime.gif",
"https://media1.tenor.com/Jk_b8o1tCv0AAAAC/super-sonico.gif",
"https://media1.tenor.com/Rx8z0qm9N4oAAAAC/super-sonico-soniani.gif",
"https://media1.tenor.com/UYUCcZRjDE8AAAAC/super-sonico-soniani.gif",
"https://media1.tenor.com/21IETFb6I8gAAAAC/super-sonico-anime.gif",
"https://media1.tenor.com/OT8Jr0gcL-sAAAAC/super-sonico-anime.gif",
"https://media1.tenor.com/Ia_ob5NX2rEAAAAC/sonico-anime.gif",
"https://media1.tenor.com/bzfsPWYv6XAAAAAC/bonniekaz-sonico.gif",
"https://media1.tenor.com/Z2moPWD6FXAAAAAC/super-supersonico.gif",
"https://media1.tenor.com/r4AsWNnkrQgAAAAC/super-sonico-guitar.gif",
"https://media1.tenor.com/9-XsJ17-lP4AAAAC/hibana-princess.gif",
"https://media1.tenor.com/D1IIF2tgyxoAAAAC/princess-hibana.gif",
"https://media1.tenor.com/wBoLjXg3o-IAAAAC/hibana-princess-hibana.gif",
"https://media1.tenor.com/de9J0dzpymgAAAAC/dey.gif",
"https://media1.tenor.com/B7x7JiNwW8EAAAAC/hibana.gif",
"https://media1.tenor.com/0_2myW2vF8wAAAAC/fire-force-hibana.gif",
"https://media1.tenor.com/AoixA6mmrKUAAAAC/princess-hibana-anime.gif",
"https://media1.tenor.com/vVkTw9-rhDcAAAAC/fire-force-princess.gif",
"https://media1.tenor.com/Fcg5UOR8MUUAAAAC/ah.gif",
"https://media1.tenor.com/amqvMLN1xNAAAAAC/princess-hibana-hibana.gif",
"https://media1.tenor.com/kZjWeKPnAr0AAAAC/fire-force.gif",
"https://media1.tenor.com/3lcf95PS9ZMAAAAC/hibana-fireforcehibana.gif",
"https://media1.tenor.com/vzmM5aNrBe4AAAAd/karyl-kyaru.gif",
"https://media1.tenor.com/NRp4EN0is64AAAAC/camila-fireemblem.gif",
"https://media1.tenor.com/Iarjrj_5n8MAAAAd/camilla-fire-emblem.gif",
"https://media1.tenor.com/N-IGf7aEKFIAAAAd/oneesan-fire-emblem.gif",
"https://media1.tenor.com/ejBrmfVq86oAAAAC/joooo-que-mono.gif",
"https://media1.tenor.com/glERRY9rNVgAAAAC/robin-robin-one-piece.gif",
"https://media1.tenor.com/NQAP1Z6TlZcAAAAC/anime.gif",
"https://media1.tenor.com/vLzpoz4H0u4AAAAC/one-piece-miss-all-sunday.gif",
"https://media1.tenor.com/Xz60BywMwQ0AAAAC/robin.gif",
"https://media1.tenor.com/GrsxVO4oHzMAAAAC/nami-nico-robin.gif",
"https://media1.tenor.com/gXn_7h_z_54AAAAC/one-piece-robin.gif",
"https://media1.tenor.com/dLn4vizWAfEAAAAC/sanji-robin.gif",
"https://media1.tenor.com/5rXCiayvg7EAAAAC/nico-robin.gif",
"https://media1.tenor.com/GwlELKRKfWoAAAAC/one-piece-red.gif",
"https://media1.tenor.com/n8oK123WyrYAAAAC/mai-sakurajima-rascal-does-not-dream-of-bunny-girl-senpai.gif",
"https://media1.tenor.com/KOJURHAYHyoAAAAC/sakuta-azusagawa-mai-sakurajima.gif",
"https://media1.tenor.com/g03B9VrrrUMAAAAC/childegf-cici-core.gif",
"https://media1.tenor.com/su3IohR6YmoAAAAC/mai-sakurajima-rascal-does-not-dream-of-bunny-girl-senpai.gif",
"https://media1.tenor.com/mJTNx0oqM1EAAAAC/bunny-girl-senpai.gif",
"https://media1.tenor.com/SjR8qyLStLMAAAAC/mai-sakurajima-rascal-does-not-dream.gif",
"https://media1.tenor.com/T1i875yCcU4AAAAd/bunny-girl-senpai-mai-sakurajima.gif",
"https://media1.tenor.com/iHtcDRaw9ewAAAAC/mai-sakurajima-rascal-does-not-dream.gif",
"https://media1.tenor.com/NdmeHWEhGmcAAAAC/mai-sakurajima-anime.gif",
"https://media1.tenor.com/nXZMJeARXFgAAAAC/rascal-does-not-dream-of-a-knapsack-kid-mai-sakurajima.gif",
"https://media1.tenor.com/NdmeHWEhGmcAAAAd/mai-sakurajima-anime.gif",
"https://media1.tenor.com/p3A7o71R1sIAAAAC/nodoka-toyohama-mai-sakurajima.gif",
"https://media1.tenor.com/W8tLUQWHGGMAAAAC/sakuta-azusagawa-seishun-buta-yarou-wa-bunny-girl-senpai-no-yume-wo-minai.gif"
"https://media1.tenor.com/FesEnU-SLqoAAAAC/rascal-does-not-dream-of-a-knapsack-kid-mai-sakurajima.gif",
"https://media1.tenor.com/bQr9rm3YUzEAAAAC/sakuta-azusagawa-mai-sakurajima.gif",
"https://media1.tenor.com/mz_ko9bpa7oAAAAC/sakuta-azusagawa-mai-sakurajima.gif",
"https://media1.tenor.com/d5uA23lvoM8AAAAC/rascal-does-not-dream-of-a-knapsack-kid-mai-sakurajima.gif",
"https://media1.tenor.com/v1YVaUQ8PRwAAAAC/rascal-does-not-dream-of-a-knapsack-kid-buta-yarou.gif",
"https://media1.tenor.com/UYQilGUINREAAAAC/kyouka-uzen-submit.gif",
"https://media1.tenor.com/A-ZgphGi_agAAAAC/kyouka-uzen-chained-soldier.gif",
"https://media1.tenor.com/bNUPSdlGlTcAAAAC/%E9%AD%94%E9%83%BD%E7%B2%BE%E5%85%B5%E7%9A%84%E5%A5%B4%E9%9A%B8-mato-seihei-no-slave.gif",
"https://media1.tenor.com/D8k1Jt4e8GkAAAAd/kyouka-uzen-chained-soldier.gif",
"https://media1.tenor.com/-wHPUZtxVqEAAAAC/%E9%AD%94%E9%83%BD%E7%B2%BE%E5%85%B5%E7%9A%84%E5%A5%B4%E9%9A%B8-%E9%AD%94%E9%83%BD%E7%B2%BE%E5%85%B5%E3%81%AE%E3%82%B9%E3%83%AC%E3%82%A4%E3%83%96.gif",
"https://media1.tenor.com/59bz1I8P-80AAAAC/%E9%AD%94%E9%83%BD%E7%B2%BE%E5%85%B5%E7%9A%84%E5%A5%B4%E9%9A%B8-mazu-seihei-no-sureibu.gif",
"https://media1.tenor.com/kb-FisG269IAAAAd/kyouka-uzen-kyouka.gif",
"https://media1.tenor.com/D8k1Jt4e8GkAAAAd/kyouka-uzen-chained-soldier.gif",
"https://media1.tenor.com/-wHPUZtxVqEAAAAd/%E9%AD%94%E9%83%BD%E7%B2%BE%E5%85%B5%E7%9A%84%E5%A5%B4%E9%9A%B8-%E9%AD%94%E9%83%BD%E7%B2%BE%E5%85%B5%E3%81%AE%E3%82%B9%E3%83%AC%E3%82%A4%E3%83%96.gif",
"https://media1.tenor.com/59bz1I8P-80AAAAd/%E9%AD%94%E9%83%BD%E7%B2%BE%E5%85%B5%E7%9A%84%E5%A5%B4%E9%9A%B8-mazu-seihei-no-sureibu.gif",
"https://media1.tenor.com/onwat3s5DigAAAAd/fubuki-%E7%99%BD%E4%B8%8A%E3%83%95%E3%83%96%E3%82%AD.gif",
"https://media1.tenor.com/8qJgDDrL-v8AAAAC/rune-factory-rfgoa.gif",
"https://media1.tenor.com/hywGzFjtWpwAAAAC/anime-seven-deadly-sins.gif",
"https://media1.tenor.com/8Tu72eUJp2sAAAAC/anime-seven-deadly-sins.gif",
"https://media1.tenor.com/a6VC2TOjdkEAAAAC/anime-seven-deadly-sins.gif",
"https://media1.tenor.com/3tq9sAECd_0AAAAC/elizabeth-diane.gif",
"https://media1.tenor.com/AMx0IYvf3fYAAAAC/anime-seven-deadly-sins.gif",
"https://media1.tenor.com/7-bndeN2OsgAAAAC/anime-seven-deadly-sins.gif",
"https://media1.tenor.com/VrZnpVUuh_YAAAAC/anime-seven-deadly-sins.gif",
"https://media1.tenor.com/7-bndeN2OsgAAAAd/anime-seven-deadly-sins.gif",
"https://media1.tenor.com/1vxCFLvpXcIAAAAC/anime-seven-deadly-sins.gif",
"https://media1.tenor.com/xWLNneBARwYAAAAC/happy-hug-while-crying-kneeling-down.gif",
"https://media1.tenor.com/ZE2UDjHzxrAAAAAC/anime-seven-deadly-sins.gif",
"https://media1.tenor.com/SHNSB_R6W5UAAAAd/nanatsu-no.gif",
"https://media1.tenor.com/WA1IrPazRMIAAAAC/seven-deadly.gif",
"https://media1.tenor.com/dz7GqavEA60AAAAC/seven-deadly.gif",
"https://media1.tenor.com/pfG35eQvkmYAAAAd/merlin-restored-the-buildings.gif",
"https://media1.tenor.com/f76_sKAR33MAAAAC/merlin-seven.gif",
"https://media1.tenor.com/CDivXbfqfxwAAAAC/merlin-seven.gif",
"https://media1.tenor.com/fXOABc2gwIUAAAAC/merlin-nanatsu-no-taizai.gif",
"https://media1.tenor.com/pfQklYdXj-0AAAAC/seven-deadly.gif",
"https://media1.tenor.com/5g6baUwtt3AAAAAd/anime.gif",
"https://media1.tenor.com/X8jZvFc13fYAAAAd/madamelucifer-anime.gif",
"https://media1.tenor.com/Ky8fG5hn7bYAAAAC/seven-deadly.gif",
"https://media1.tenor.com/JcGjbuF61KcAAAAd/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/TI6kZcqU6jEAAAAd/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/fFklq54VnaMAAAAC/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/W3j7ufz80k4AAAAC/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/g2RdI2kt1I4AAAAC/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/_KbvbLXIojIAAAAC/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/QmLbLOno13AAAAAC/seven-deadly-sins-7ds.gif",
"https://media1.tenor.com/yAFn3pjI_iYAAAAC/ludociel-angel.gif",
"https://media1.tenor.com/0EZRdpEOgX0AAAAC/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/6BG6y_ygwfoAAAAC/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/8As5Go3vUsoAAAAC/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/0EZRdpEOgX0AAAAd/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/6BG6y_ygwfoAAAAd/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/6uPNzzUaNagAAAAC/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/GU5l9icDH3gAAAAd/ludociel-angel.gif",
"https://media1.tenor.com/GOvYxqC6tzgAAAAC/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/BDAbFNUCzusAAAAC/seven-deadly-sins-sds.gif",
"https://media1.tenor.com/bXcbNDzLyqQAAAAd/rita-rossweisse-honkai-impact3rd.gif",
"https://media1.tenor.com/0yIV8X46HAIAAAAC/crying-tears.gif",
"https://media1.tenor.com/MoEAlnvz6ioAAAAd/fallen-rosemary-hi3rd.gif",
"https://media1.tenor.com/WpdON9dcoZAAAAAd/honkai-impact.gif",
"https://media1.tenor.com/hVRnbpF6EQMAAAAd/rita-rossweise-honkai-impact.gif",
"https://media1.tenor.com/z-tTOF3q1wgAAAAd/honkai-series-rita-rossweisse.gif",
"https://media1.tenor.com/7TS2V1HGEnQAAAAd/hi3-honkai-impact-3.gif",
"https://media1.tenor.com/CKlWMXF0_8kAAAAd/fallen-rosemary-honkai-impact.gif",
"https://media1.tenor.com/vC_IG0boZmgAAAAd/hontaki.gif"
]

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

# ================= UTILS =================

def cd_left(uid):
    if uid not in cooldowns:
        return 0
    return max(0,int(COOLDOWN-(time.time()-cooldowns[uid])))

def on_cd(uid):
    return cd_left(uid)>0

def set_cd(uid):
    cooldowns[uid]=time.time()

async def resolve_user(arg):
    if arg.isdigit():
        return int(arg)
    user=await client.get_entity(arg)
    return user.id

async def user_tag(uid):
    try:
        u=await client.get_entity(uid)
        if u.username:
            return f"@{u.username} / {uid}"
    except:
        pass
    return f"{uid}"

async def giphy_random(q):
    url=f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY}&q={q}&limit=50"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data=await r.json()

    gifs=[g["images"]["original"]["url"]
          for g in data["data"]]

    return random.choice(gifs)

# ================= HAVVA =================
@client.on(events.NewMessage(pattern=r"\.havva"))
async def havva(e):

    if on_cd(e.sender_id):
        return await e.reply(
        f"attends encore {cd_left(e.sender_id)}s pour faire la commande")

    set_cd(e.sender_id)

    await e.reply(file=random.choice(havva_gifs))

# ================= MSS =================
chars=[
"yumeko jabami",
"nelliel bleach",
"bambietta bleach",
"boa hancock",
"rin tohsaka",
"misa amane",
"ichinose classroom elite",
"kurumu kurono"
]

@client.on(events.NewMessage(pattern=r"\.mss"))
async def mss(e):

    if on_cd(e.sender_id):
        return await e.reply(
        f"attends encore {cd_left(e.sender_id)}s")

    set_cd(e.sender_id)

    gif=await giphy_random(
        random.choice(chars)+" anime gif")

    await e.reply(file=gif)

# ================= HENTAI =================
@client.on(events.NewMessage(pattern=r"\.hentai"))
async def hentai(e):

    if e.sender_id not in blacklist:
        return

    if on_cd(e.sender_id):
        return await e.reply(
        f"attends encore {cd_left(e.sender_id)}s")

    set_cd(e.sender_id)

    msg=await e.reply(
        file=random.choice(hentai_gifs))

    await asyncio.sleep(7)
    await msg.delete()

# ================= SLAP / KISS =================
@client.on(events.NewMessage(pattern=r"\.(kiss|slap) (.+)"))
async def action(e):

    if e.sender_id not in blacklist:
        return

    if on_cd(e.sender_id):
        return await e.reply(
        f"attends encore {cd_left(e.sender_id)}s")

    set_cd(e.sender_id)

    act=e.pattern_match.group(1)
    target=e.pattern_match.group(2)

    gif=await giphy_random(
        f"anime {act} gif")

    sender=await user_tag(e.sender_id)

    await e.reply(f"{sender} {act} {target}")
    await e.reply(file=gif)

# ================= OWNER =================
@client.on(events.NewMessage(pattern=r"\.owner (.+)"))
async def add_owner(e):

    if e.sender_id!=OWNER_ID:
        return

    uid=await resolve_user(
        e.pattern_match.group(1))

    owners.add(uid)
    blacklist.add(uid)

    await e.reply(
    f"✅ {await user_tag(uid)} est maintenant propriétaire")

@client.on(events.NewMessage(pattern=r"\.unowner (.+)"))
async def rem_owner(e):

    if e.sender_id!=OWNER_ID:
        return

    uid=await resolve_user(
        e.pattern_match.group(1))

    owners.discard(uid)

    await e.reply(
    f"✅ {await user_tag(uid)} retiré des propriétaires")

# ================= BLACKLIST =================
@client.on(events.NewMessage(pattern=r"\.bl (.+)"))
async def bl(e):

    if e.sender_id not in owners:
        return

    uid=await resolve_user(
        e.pattern_match.group(1))

    blacklist.add(uid)

    await e.reply(
    f"✅ {await user_tag(uid)} a été ajouté à la blacklist")

@client.on(events.NewMessage(pattern=r"\.unbl (.+)"))
async def unbl(e):

    if e.sender_id not in owners:
        return

    uid=await resolve_user(
        e.pattern_match.group(1))

    blacklist.discard(uid)

    await e.reply(
    f"✅ {await user_tag(uid)} a été retiré de la blacklist")

# ================= LIST =================
@client.on(events.NewMessage(pattern=r"\.blacklist"))
async def show(e):

    if e.sender_id not in owners:
        return

    msg="**propriétaire 🛠️**\n"

    for o in owners:
        msg+=f"{await user_tag(o)}\n"

    msg+="\n**bl list 📔**\n"

    for u in blacklist:
        if u not in owners:
            msg+=f"{await user_tag(u)}\n"

    await e.reply(msg)

# ================= RUN =================
async def main():
    await client.start()
    print("USERBOT ONLINE")
    await client.run_until_disconnected()

asyncio.run(main())
