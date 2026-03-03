import asyncio
import random
import time
from telethon import TelegramClient, events
from flask import Flask
import threading
import aiohttp

# ================= CONFIG =================
API_ID = 35399015
API_HASH = "f93407152428bac353cd92a4d9c8b4e1"
SESSION = "userbot"
GIPHY = "YLLksuIyKHZcaMKuAOYR1s27dz2uy8Xr"
COOLDOWN = 5

# Propriétaires fixes
owners = {7891919458, 8388054272}

# ================= BLACKLIST =================
blacklist = set()
try:
    with open("blacklist.txt", "r") as f:
        for line in f:
            uid = int(line.strip())
            if uid not in owners:  # jamais blacklist les propriétaires
                blacklist.add(uid)
except FileNotFoundError:
    pass

cooldowns = {}

# ================= CLIENT =================
client = TelegramClient(SESSION, API_ID, API_HASH)

# ================= KEEP ALIVE =================
app = Flask("")

@app.route("/")
def home():
    return "online"

threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()

# ================= LIENS =================
sword_links = [
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141840170680502/IMG_7695.png?ex=69a7525d&is=69a600dd&hm=719e6464658b9a51027e8c0c3a004a0b72a77958bf56338bc586fbe64f40cdfd&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141840799699084/IMG_7696.png?ex=69a7525d&is=69a600dd&hm=e75492a972a2ce939a85a35e58d9838293dc11ce620d06d31e6b642dc2e25aab&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141841277976618/IMG_7697.png?ex=69a7525d&is=69a600dd&hm=7244f2e34580e4a15fd2bcfb207704b74bd70972d481691da5b8dedb583d50db&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141841667788923/IMG_7698.png?ex=69a7525d&is=69a600dd&hm=2412f5dd8a0168358b6f2e8e9ad3fbe0a9c477b3b2f6019d1bf75893a27d897c&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141842024300858/IMG_7699.png?ex=69a7525d&is=69a600dd&hm=659bca845da6aead7d2df77c8dee7caa202a985d22f53d3667c115653f6e892a&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141842423021660/IMG_7700.png?ex=69a7525d&is=69a600dd&hm=6e18637d3531eb0f10e94bf5e24e86f6706bfe0ddaf2661b30a2de22f9493c0a&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141842863161426/IMG_7701.png?ex=69a7525d&is=69a600dd&hm=c0edc9af508882e7006c4f8b60bc4334de6ebb8f13338a2206a224a80c44eecf&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141843282858125/IMG_7702.png?ex=69a7525d&is=69a600dd&hm=e7195191e5695377b63db47cda1b8a791728de547b989b145e5932e1881fb710&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141843588907153/IMG_7703.png?ex=69a7525e&is=69a600de&hm=c22d92fc0b0bc80e8fef9d740bfe014722835fbc9cd8d76fdb5ed4792050358e&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141843911999488/IMG_7704.png?ex=69a7525e&is=69a600de&hm=9f60d4ebdfe96843ad1c04879d62997a0083d82b7d04725b178105b3d987d49c&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141854154489926/IMG_7705.png?ex=69a75260&is=69a600e0&hm=66f44b762d192034f04229a0f35520a7d561b74188cb93318844717c6c4ffeb4&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141854510747788/IMG_7706.png?ex=69a75260&is=69a600e0&hm=d6ba818bd633f8de65f897534a5bd9c80a1d0be3dac9ec5e5cada69ef7b77dc9&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141855307792394/IMG_7707.png?ex=69a75260&is=69a600e0&hm=f8ec89cdb2d81b1166b804e7e077a39a2cd4620a55c0b547e3e5e8b44bc8a551&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141856255836301/IMG_7708.png?ex=69a75261&is=69a600e1&hm=5877b20d07edcaabda1c6516b43834e7ea2bd47d3238ebf9d68c584a3e1bd9e5&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141856943444028/IMG_7709.png?ex=69a75261&is=69a600e1&hm=cd9d30a09b61c6c14e4f27b6946deb0d91e32635c22773512404d5e8fbc736c3&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141857379778793/IMG_7710.jpg?ex=69a75261&is=69a600e1&hm=f5d099a7adf9d84e3a7f6d4631f14ff953f36753019bcfed8cb87cdfe8754b05&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141857711259819/IMG_7711.jpg?ex=69a75261&is=69a600e1&hm=18eafc0e193f336b866d2bcd0d2d6065171887c1ab5c76226255faef96f5e797&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141858046545991/IMG_7712.jpg?ex=69a75261&is=69a600e1&hm=544a17de6778da6849630c5db1c7c6cbdc8ffe8cb39884d213685147d6b42829&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141858373828668/IMG_7713.jpg?ex=69a75261&is=69a600e1&hm=74bda7a3611f044988949e172f4a2ff87eea0232f99e95e03dd89c51ba965c4d&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141858743058604/IMG_7714.jpg?ex=69a75261&is=69a600e1&hm=5847814dc4eefd83173b50e708654860e4a0eff209cb979399f17fc921e277b8&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141866301063410/IMG_7715.jpg?ex=69a75263&is=69a600e3&hm=8c86607d1ffad3c8d06862361a8409ceaed79d5f5125d63aebb7d2e794d1c9f1&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141866854846756/IMG_7716.jpg?ex=69a75263&is=69a600e3&hm=50f81bf05f28283cb6dcb9d6631b2423cf8d8af77ca7aeb9dbc5b72ae9f9c958&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141867303374899/IMG_7717.png?ex=69a75263&is=69a600e3&hm=ae042d6dec168768cc6f54b66a20961630fbd693eb7b6a99a70adfe4fb44722e&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141867676926065/IMG_7718.jpg?ex=69a75263&is=69a600e3&hm=c08ac37f8030442332573d85fbfbcc0378336cc3895f721bbf11ac45564f47d1&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141868070928425/IMG_7719.jpg?ex=69a75263&is=69a600e3&hm=43207acc68e1984922666163b5b348c2b0e51f8081d5835ed421d3f7904ab4d1&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141868452872359/IMG_7720.jpg?ex=69a75263&is=69a600e3&hm=9bb98c0ca283c096899d822ce6c13355b6ec65bf9d3d49dcd10022f6dfb79046&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141868792615102/IMG_7721.jpg?ex=69a75264&is=69a600e4&hm=a86f921ca8277f6be4b331bcaf703208d4b2cef72f0bef4ebc226580242da234&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141869090406411/IMG_7722.jpg?ex=69a75264&is=69a600e4&hm=7c450726bc32eacc51e9049f61dc9ff87086457294926b7eee16e40f7df34b09&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141869425823794/IMG_7723.jpg?ex=69a75264&is=69a600e4&hm=6dbb98fced131dff825cf3e016be706fde5a0effc2a131152bdc9774acdfac6e&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141869765693612/IMG_7724.jpg?ex=69a75264&is=69a600e4&hm=2188b602283f3ff21f0df8d228a2a0933694e2b9ee47e05509db1a4cbb7a29a3&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141889449295894/IMG_7725.jpg?ex=69a75268&is=69a600e8&hm=2be389cbe300db27e91e65fb8d97d76688a536ad67549c1d76d3bb21e41322e6&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141890015531171/IMG_7726.jpg?ex=69a75269&is=69a600e9&hm=81d4a17d9c40421136a1f78917d4bbbcbe8f3685dcb1467d2b9fe5668654325c&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141890640609360/IMG_7727.jpg?ex=69a75269&is=69a600e9&hm=983497bae70afb6209a5097a7bbff27fe0d6945766241583fbbb9153e066ada8&"
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141891621949691/IMG_7728.jpg?ex=69a75269&is=69a600e9&hm=b19436ca48f7babcabc17d5e06c3767da6477bb587e10c47c21dc3d47648cfc2",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141892381245543/IMG_7729.jpg?ex=69a75269&is=69a600e9&hm=9236cd13d87b09b3470e0a85b340cd67f8d57c70b89ecd80409ace53abaf865d",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141893136355408/IMG_7730.jpg?ex=69a75269&is=69a600e9&hm=0034b7dfab9b864426b5d86faa5ce6cd650069e71c6d9f229a4989415490db9a",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141893962498079/IMG_7731.jpg?ex=69a7526a&is=69a600ea&hm=e52cd95c0960eaa2a977edb2f313f88faecbd0518f8af66a016de3ab3f1ca6e6",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141895204016239/IMG_7732.jpg?ex=69a7526a&is=69a600ea&hm=7996fd2081ddf6182b8fdcf4d40180f933052f7cdf10069ae99d9f0a05f2e717",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141896147865621/IMG_7733.jpg?ex=69a7526a&is=69a600ea&hm=b68a566c676841d24357bf67966972fc9482958d553bb43dee37f44af1af12fa",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141896948842598/IMG_7734.jpg?ex=69a7526a&is=69a600ea&hm=70e1a79a8aff6b48fadb5c934c90ccb98e68e32ae546c1f3487cbf2efd58a712",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141916704145478/IMG_7735.jpg?ex=69a7526f&is=69a600ef&hm=cd689186d739c3322f65c473e5b426dfdaab79b667e68aa4e226d4fdcdc61f52",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141917463052564/IMG_7736.jpg?ex=69a7526f&is=69a600ef&hm=1f64f609f421e97e0012ba479e034c831393276c1cd4459b396d29743f6b3e08",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141918067163236/IMG_7737.jpg?ex=69a7526f&is=69a600ef&hm=b3372cb60b946b082e2a3154d5d74ea771fd32d8f499bebb7d20d4dc411bb736",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141918759092324/IMG_7738.png?ex=69a7526f&is=69a600ef&hm=fefa3cc02f386cdd91334cf43fc21c7b994f352a6790b219e09efd5f8d532545",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141919493357720/IMG_7739.jpg?ex=69a75270&is=69a600f0&hm=598e8ea544297cea6a66a84d37749fed87798c50fd0bcab94c359e58464cde14",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141920151601203/IMG_7740.jpg?ex=69a75270&is=69a600f0&hm=3d685283c414401410bb15398837ea28de595bf428e4cf77ae63a491270fb2ec",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141921003307191/IMG_7741.jpg?ex=69a75270&is=69a600f0&hm=c65218ea8e16a459a86d4c44f8861a977e80b8282fdbb9721cfe418e4c6388b5",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141921489715281/IMG_7742.jpg?ex=69a75270&is=69a600f0&hm=dda582381e4997043506252dd6ad815df28db97712a816a3dd54a4049a2da520",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141922047430706/IMG_7743.jpg?ex=69a75270&is=69a600f0&hm=abf34e8828b42e74e3d6974c2e9647036de11af8817be430be63d215cd213289",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141922513129763/IMG_7744.jpg?ex=69a75270&is=69a600f0&hm=8e27019757b80e8164d5c33870a3d2b876c443a70bbba820bcd9f3b302c6adab",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141943748759743/IMG_7745.jpg?ex=69a75275&is=69a600f5&hm=020f4e1f3302e937f68217f6ecac41308a1f3f37a7d80f078a95021924966080",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141944424169614/IMG_7747.jpg?ex=69a75276&is=69a600f6&hm=6ff5ac8cd190f8c4548f5ea1dd408559b01aaa96f5c95d9f1a592500e6655b37",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141945900437555/IMG_7746.jpg?ex=69a75276&is=69a600f6&hm=cbabb9222e02d0bd43794caa30234d194a8c3faa8b3f5e9327c2004435c8bbd6",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141947595063357/IMG_7748.jpg?ex=69a75276&is=69a600f6&hm=b6d69ade815a153c9307f857bd33dbe0b60127d46a0f6be6ff67ac321f209764",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141949352480832/IMG_7749.jpg?ex=69a75277&is=69a600f7&hm=21aaf2ae02ffde54c41df7d70bc0ff070cef84b876f99b1f4dc03442d9261922",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141950870814791/IMG_7750.jpg?ex=69a75277&is=69a600f7&hm=ac942149970422c41f3c776974617484c707039d921cda5ad88c9c36c0fd5844",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141952011534397/IMG_7751.jpg?ex=69a75277&is=69a600f7&hm=34ee48067a92999fd3cf2edb438cbb0daa2d16f7e75d49815404bb19a5334913",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141960572240033/IMG_7753.jpg?ex=69a75279&is=69a600f9&hm=a8e3452c2bdae8bb37a4a002f279db88ad5ba170d514b0f4863a7d92ae1d9f6d",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141961813757952/IMG_7754.jpg?ex=69a7527a&is=69a600fa&hm=8f36c95e5e9f224da925a06f7798f65534e98991721a008791b6d0f4c7089a70",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141962782638344/IMG_7752.jpg?ex=69a7527a&is=69a600fa&hm=991b37c61e30e32fa1dce19129992d3fd5b787d98a331d0d5b816216d42fdb4e",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141977689067651/IMG_7755.jpg?ex=69a7527e&is=69a600fe&hm=adef0a2551735f97463c3b9c2cb1d19e10861f0c8a4d5114c67fee05911dd13b",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141978050035813/IMG_7756.jpg?ex=69a7527e&is=69a600fe&hm=ea25aaa4a41a748a064b786d0d072a826cd2dacb1203e3e00d62142e1aa75c40",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141978578522367/IMG_7757.jpg?ex=69a7527e&is=69a600fe&hm=63043426e8b44fdbb7a0b1a09dc3ac784944277f9f4e02552990a242a0bd95be",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141978993627322/IMG_7758.jpg?ex=69a7527e&is=69a600fe&hm=d30e2abc954336e3e241d9759c51806b1ba46a3cc5d0fc475eaebb3e9a91739f",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141979387760670/IMG_7759.png?ex=69a7527e&is=69a600fe&hm=3ea79107e5603fb5f6ee69f257ec8920d77ce075a47c9ec5a274623673da1fd8",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141979731824650/IMG_7760.png?ex=69a7527e&is=69a600fe&hm=5686ca7707618ad04b731324ee0f4c9777e6e54c6d9f580b98021da54ab92e0c",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141980063170751/IMG_7761.png?ex=69a7527e&is=69a600fe&hm=ec1815a7a001dd3bed3ace54bb360cd8cc5576637a1bd0396f584d999ccef4d3",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141980574879914/IMG_7762.png?ex=69a7527e&is=69a600fe&hm=f604325077f6b0352baa501a3364140544708908220482965a4b370908411f11",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141980889579733/IMG_7763.png?ex=69a7527e&is=69a600fe&hm=8739c2ba35831d1f319d90a03a23f065ab765d5d15bc541d487c56bfb4bdb776",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141981283717151/IMG_7764.png?ex=69a7527e&is=69a600fe&hm=9cb8299129920821d8fc966fb3b8cc09ec977e1eb431227c1a0d006427529a5e",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141995590488189/IMG_7765.jpg?ex=69a75282&is=69a60102&hm=8b9279d2b42e11258e4e680cda9ba13fa4c85ae35b942b077c6423e957bd3eec",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141996005589084/IMG_7766.jpg?ex=69a75282&is=69a60102&hm=5844f7feab298b29af6dd923fb1b8362a27d7c00c43c1d45e015b2f2a43a0f31",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141996609831023/IMG_7767.jpg?ex=69a75282&is=69a60102&hm=33d2aef71fbb4db09f90d6c63bea9553c0a5c14549b0a8dd00df074a79f18154",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141997163348171/IMG_7768.jpg?ex=69a75282&is=69a60102&hm=0fad97d8df187587a74b6f17545bd454aebec8f05e71e18b0042421cde5dbb84",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141998262386882/IMG_7769.jpg?ex=69a75282&is=69a60102&hm=6a660c0a35b68625386c93355c43c0e78cc3d24237ca024006782af9980dfbfa",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141998861910016/IMG_7770.jpg?ex=69a75283&is=69a60103&hm=329c9a66c9dfa7e7a35864fbb5de1b0ee4b6e153c5ad97b0735a121d348679cd",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141999260635277/IMG_7771.jpg?ex=69a75283&is=69a60103&hm=cad9fdb91de344344f9df7234cc8a13a81baf7a665a44d6879721b214dab72f9",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478141999969337505/IMG_7772.jpg?ex=69a75283&is=69a60103&hm=65034da946abda78113e9a84bea407119f5fc995bde6cb13fe0753e08b7e0604",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142000984494161/IMG_7773.jpg?ex=69a75283&is=69a60103&hm=a8059bfefcf62a89d6198ada8cb015809a8a0e6049a44e295b7db32302b93d5e",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142001642737674/IMG_7774.jpg?ex=69a75283&is=69a60103&hm
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142001642737674/IMG_7774.jpg?ex=69a75283&is=69a60103&hm=aeb5dbc8bb0e8aa3bcd4f6757b2262b83c494c2694ef16b530a3f4e996cde1c2",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142024120271078/IMG_7775.jpg?ex=69a75289&is=69a60109&hm=67f32eae934a0065c15e3200a622075d1d1f2ab51085f985d83ea0fc2b4a8ec3",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142024472596542/IMG_7776.jpg?ex=69a75289&is=69a60109&hm=a01f14d5045b15335f6df0d31c9db33a6368329179d39f467bc48cd2a53f404e",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142024900411443/IMG_7777.jpg?ex=69a75289&is=69a60109&hm=c7b04f66a2e9666e25460fc1e98bae65210d85d6d4e114029831afe5aaa7acfe",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142025357328656/IMG_7778.jpg?ex=69a75289&is=69a60109&hm=308bf9b4616ade2adaa1aee42ee1a986b5c1b3c2bdf02b8bd9772c4ed02d58ee",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142025827221685/IMG_7779.jpg?ex=69a75289&is=69a60109&hm=0d10ef9d9f44f63435f91ac795e6c00c54225ec4760ed9ab6702fff92f12ca28",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142026238132234/IMG_7781.jpg?ex=69a75289&is=69a60109&hm=3cc8cfe01fdf5c5e2b4380f8312d8d9faa0b93810f505a27e5ad83a5f6ae2dab",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142026749968557/IMG_7780.png?ex=69a75289&is=69a60109&hm=b3cf156d33958254c5b8337ce56de2cd1954ab34d63783d9ab10a070f2c51f90",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142027274260521/IMG_7782.jpg?ex=69a75289&is=69a60109&hm=7f887f851b03d425d47a236c9246dcfbb84dbb9d6168097b1cf4737bd9487d81",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142027647549733/IMG_7783.jpg?ex=69a75289&is=69a60109&hm=c3886b560795d8d52dfe07748b605bafaed5ed1a47ce2e6168ca21005d5acae0",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142028318507181/IMG_7784.jpg?ex=69a7528a&is=69a6010a&hm=6a74cdcb3c0e4d0e10fa902116bc8e154a2a377283a7d72eca56fcfdb2dd7c87",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142044730953850/IMG_7785.jpg?ex=69a7528e&is=69a6010e&hm=8300d64592986904ee2867108496251e02d3903c876b4b0a89ce19e2ad8dedc5",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142045108436992/IMG_7786.jpg?ex=69a7528e&is=69a6010e&hm=d512d2f643e5e2b7e98e331eefb0a9cac0c77ea7629ebe64ca79cffbcfd64285",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142045485928548/IMG_7787.jpg?ex=69a7528e&is=69a6010e&hm=b250f39820c21d2b5b5f58b1270ab402dae9567fd06b9dd89ad41bebb9b5fda5",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142045804822699/IMG_7789.png?ex=69a7528e&is=69a6010e&hm=dd4a2e7ae70d41c35e8bb080acdec73630a5b62139b4c77e74bdb471927e3ce5",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142046144303375/IMG_7790.png?ex=69a7528e&is=69a6010e&hm=6b3eadd966b904568e24a86cefb7b210df3c6982495ff96f206a4fd010a32248",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142046542757960/IMG_7788.jpg?ex=69a7528e&is=69a6010e&hm=39851e40b9c2b324ee745d3dbd7c49538b37c4a129394550f64b0f51c286874e",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142046962319493/IMG_7791.jpg?ex=69a7528e&is=69a6010e&hm=81f3aae7cd76c967d8fac5945d70084ca4a4c9609361ee9a6ef1b206af4146bc",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142047302193392/IMG_7793.jpg?ex=69a7528e&is=69a6010e&hm=8bd17c123d9c7cebf83a233e640fc09275c4cd8b942e6d5fcf6bb1ad45383b51",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142047738138789/IMG_7792.jpg?ex=69a7528e&is=69a6010e&hm=d16a5662cb84958470266580e69c756b94d3fea0db1bc6cafe193cffe98707ad",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142048237391945/IMG_7794.jpg?ex=69a7528e&is=69a6010e&hm=b3d1b7805af231c3dbf3dbe37d6500ff7ea603df9c5a1a9734c59d18756fe8b9",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142066146939082/IMG_7795.jpg?ex=69a75293&is=69a60113&hm=208a776bc050a638335dfc5deb6a772e5ed0fd65aeefdae6e83ead031603ca5b",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142066683805828/IMG_7796.jpg?ex=69a75293&is=69a60113&hm=418418e32e92f23f19e786d8ed71bd99cce606292115f7c1f8d0343f260780a7",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142067120275617/IMG_7797.jpg?ex=69a75293&is=69a60113&hm=d6cc6644bd68b32129fdd5fb1d6857c167ce0bfb347e15058f8d798703f47c00",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142067652689920/IMG_7798.jpg?ex=69a75293&is=69a60113&hm=e30acae2fed76e00aef76bbe77180c391f54f101ac16e7c4dae9eafeacad10fa",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142068131106919/IMG_7799.jpg?ex=69a75293&is=69a60113&hm=0b052a04fac1d374666d65d11d443ad920c7b1424af0b83deb6d5ebb7fd849ad"
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142068659323006/IMG_7800.jpg?ex=69a75293&is=69a60113&hm=d4aeec402c19323a2be3680c65a9d8f318f7c4c719a568d4f54d140375c3d971",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142069410107585/IMG_7801.png?ex=69a75293&is=69a60113&hm=2370530eed821f077ef8b49d5132097093224a3f3ba301edea4c6011fee0cfc0",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142069892448327/IMG_7802.jpg?ex=69a75294&is=69a60114&hm=09a92e028ba11c310a1f1213f25d411f685bf6ad5da6ee12ff645e460729c05f",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142070483849237/IMG_7803.png?ex=69a75294&is=69a60114&hm=9e4e0e801440a844231252fb5273bd24983d52b228fd138fda7760eb8dfccc9b",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142071272636608/IMG_7804.png?ex=69a75294&is=69a60114&hm=dd43bef3d2a2d4b67955d1d31d150a7cb40595867bed97de70ec273f7f849322",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142089819721938/IMG_7805.png?ex=69a75298&is=69a60118&hm=bb3f037a9a9f9d51692a8520b5bffdfa38d0727edc4a8f5c313e754bbeb9f23b",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142090180301022/IMG_7807.png?ex=69a75298&is=69a60118&hm=4d5b449e5495035eeadae7185693b0bb14ed2fa44de58fe20f07607b9fbd0b89",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142090574696449/IMG_7808.jpg?ex=69a75298&is=69a60118&hm=bc67eee0cdc907ff833aaed163ca599a0afd031c9489e81d8a1bbf2633b7aa76",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142090952179714/IMG_7806.png?ex=69a75299&is=69a60119&hm=b8ddeef48b9221d7b2d2a385d5a5c8946e6141da06f049f91fb51cf8468aca5a",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142091178541156/IMG_7809.jpg?ex=69a75299&is=69a60119&hm=c4aba829783aa32bfd5f85b2cacda0637bc7d9c3e32f1e6307aeb550a829a3e5",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142091472277535/IMG_7810.jpg?ex=69a75299&is=69a60119&hm=277ab0ec11cb50f3676faaa05f50365c69163c941ac20c5bf0793e2088cb2fe9",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142091853955132/IMG_7811.jpg?ex=69a75299&is=69a60119&hm=de8bd9c5b5b0aa9e6a24d442898768dc20bd71ee5bfb3575d3d6329270ac2fc6",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142092160274549/IMG_7812.jpg?ex=69a75299&is=69a60119&hm=6449b54bf1c9858edb2cee4355736d3e2c902c627fc7fb688d2117e5d01a57aa",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142092554403900/IMG_7813.png?ex=69a75299&is=69a60119&hm=d84e633d7e26ac0a69b0b0c950f1f71ea34bbea3a3f2533351fe62b42821cb23",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142092977897644/IMG_7814.jpg?ex=69a75299&is=69a60119&hm=4d90c7a27ddbbf3f1d6482e0f6c3641b41adb3a9c7783c51cf9d442fb18976d1",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142112083218452/IMG_7815.jpg?ex=69a7529e&is=69a6011e&hm=e73b7d0fde93ed5fb23850fa356867c829053f3cea5a942b47d534c7c39bd6da",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142112477479084/IMG_7816.jpg?ex=69a7529e&is=69a6011e&hm=b07492c6fbd831764057a9021fb71b97fffd95a7c31599225f60e77ccd6b43bc",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142112854708284/IMG_7817.png?ex=69a7529e&is=69a6011e&hm=be88c67e95c5d5e61b1e46f05a6cf593075c5ee2801ef68690ee6290dbbb00be",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142113135853588/IMG_7818.jpg?ex=69a7529e&is=69a6011e&hm=782c50e986f4d5e02880b2c62c4072ff14716d1a8d1fda95f14dd6ea2ceb84e1",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142113492238631/IMG_7820.png?ex=69a7529e&is=69a6011e&hm=7725b512f22f1976807064740691d3793094035b9ac1bb603d5c30442ae9bfb7",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142113794359299/IMG_7819.png?ex=69a7529e&is=69a6011e&hm=b93c1bb193a408919152eaa3f9d6542556e66146b453aca8bea3c95da96182d6",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142114058473665/IMG_7821.jpg?ex=69a7529e&is=69a6011e&hm=f418f28ed596d3e0ad2744ea24df411d5b3634b7b53a949f68bc5f66b9e47803",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142114394144929/IMG_7822.jpg?ex=69a7529e&is=69a6011e&hm=43aedfa3d7955d0bb3edffcb57b29ec0e65dea1380165fb75f59f0dea87b21fe",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142114687881489/IMG_7823.jpg?ex=69a7529e&is=69a6011e&hm=db0779becfc674c110567e8bd44749c5f79eda3b2d687d32343138d91866a84b",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142114981478653/IMG_7824.jpg?ex=69a7529e&is=69a6011e&hm=e4d2f87f1bf742e7dbdf4f025d72a375fcdc7eac3cbfdc05e7775416d9ec3c04",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142132412747897/IMG_7825.jpg?ex=69a752a2&is=69a60122&hm=d45cb75529e6324538bb7d418ed88bca3d7329a2312273af9522ab7e5c4c201d",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142132865863870/IMG_7826.jpg?ex=69a752a3&is=69a60123&hm=6160252c7b46a6c491bef15152b274429f688699044f62b87565f18ae6037b60",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142133155397713/IMG_7827.jpg?ex=69a752a3&is=69a60123&hm=2fb2881d45f8e706d43efc1891988f14f822d575ed925ebfd97169fcddf0f2f5",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142133449003201/IMG_7828.jpg?ex=69a752a3&is=69a60123&hm=32fc4402587e00bad1aac406cc717b4deb8ff28db257294bd80912c7a8b7e149",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142133813641471/IMG_7829.jpg?ex=69a752a3&is=69a60123&hm=2a0fd5b73a7b825d43d49016d0b32fa630e79e7e3e047033547d561e7af1dd1f",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142134459695144/IMG_7830.jpg?ex=69a752a3&is=69a60123&hm=05fb33f533d09e8dd67173ac4bcde140f0dc094a442326ca412707c3747c3902",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142134870868091/IMG_7831.jpg?ex=69a752a3&is=69a60123&hm=8840c557d9a1cbac10c4c7cd30e7acd8569b12a65563c53362d799f4d3a52505",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142135172862043/IMG_7832.jpg?ex=69a752a3&is=69a60123&hm=5fe14e0f0200d8ce2e60aa539dad8e8e59758096101ec10ba72c2491cfeb6c8f",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142135449555236/IMG_7833.jpg?ex=69a752a3&is=69a60123&hm=dce17cb482e7643a195125568cbcdd4b72b4eb08eab40b94735417fbed0773d9",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142135764258816/IMG_7834.jpg?ex=69a752a3&is=69a60123&hm=2f76a09eeb57c1d868c010467715f134e08eaa16edfdda2519f24497997d8a17",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142162309877901/IMG_7835.jpg?ex=69a752aa&is=69a6012a&hm=85a15eb10606279e38f519c52f0a96d73a9838e97c82c8f6b7d719199b497a6e",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142162800742522/IMG_7836.jpg?ex=69a752aa&is=69a6012a&hm=a0d72c2646f8ad89113f79628e883a9d556997eef82b96e719a7d45041e9d526",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142163521896458/IMG_7837.jpg?ex=69a752aa&is=69a6012a&hm=d22a6855b6f149fe27ce8232d7c7826d4070bf34b71d029a6b5ca4d0507e50e4",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142164209766441/IMG_7838.jpg?ex=69a752aa&is=69a6012a&hm=afa068585eb5f543a19dc09f3bfea12e357bc93e1d23d67109b15dab7ca201a5",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142164826325195/IMG_7839.jpg?ex=69a752aa&is=69a6012a&hm=69f05f9c3100cee70cc3d532252eb971ed475462a44c382e5be38ee4d58d3de1",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142165321515032/IMG_7840.jpg?ex=69a752aa&is=69a6012a&hm=783603ce3df923387d7d1b8de64935a470066ac760d6ffe8152a6364cfaf3f27",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142166126559434/IMG_7841.png?ex=69a752aa&is=69a6012a&hm=47fa705b0698d878b72fc3105c5ed832377500db3d71000d2d84d24afc1253b6",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142166881800423/IMG_7842.png?ex=69a752ab&is=69a6012b&hm=3cf7eff39a5e29e6346b003fb4999e7aec2cc07cc45828ef08a9272ed18bd5c3",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142167745695836/IMG_7843.jpg?ex=69a752ab&is=69a6012b&hm=7b705270727226b3c6efdda52aa63c098c1f130ea7e5042c221b375f86b209af",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142168328572988/IMG_7844.jpg?ex=69a752ab&is=69a6012b&hm=a83de0aa09b3b1603ee32c4f19dbf36f73e6fe93a2599c006f0cdc8fe4b6a261",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142180894834738/IMG_7845.png?ex=69a752ae&is=69a6012e&hm=d9169e8149bf0fe5996ead37453d3513540c9a3387f440b5d10fb4b938ca42fa",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142181507207300/IMG_7846.jpg?ex=69a752ae&is=69a6012e&hm=80e1d8fa34e2ca3aada048bc51d2adcf767174b186e87cb1d255f5a20fe6755c&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142182119571606/IMG_7847.jpg?ex=69a752ae&is=69a6012e&hm=ecdb69c3f9743be6ff114e291c62929f3867f7b167c768335e5e0ee446738813&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142182778081512/IMG_7848.jpg?ex=69a752ae&is=69a6012e&hm=0dcbee3c63ec667339bc19035d96183291abc2197f4a1314582039847ed5cdd9&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142183176409231/IMG_7849.jpg?ex=69a752af&is=69a6012f&hm=02ce7880313fdba8a52b19301a9c6400abce65f859cf21d50d1c49151212d5f6&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142183629525083/IMG_7850.jpg?ex=69a752af&is=69a6012f&hm=92f5aba8a302761fb568bff128b6ad53090e021151964d3cdae1845ff0c8e6cd&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142184245956678/IMG_7851.png?ex=69a752af&is=69a6012f&hm=f980aeb672586c3ca2a22f498ac4c1462387f0723956ed09750a49fa7cd820a8&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142184632094975/IMG_7852.jpg?ex=69a752af&is=69a6012f&hm=0642a01aa84ceb3bbf679a65e1773f550655bb0e8ec8c0393b02f11c3b704c48&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142185319698563/IMG_7853.jpg?ex=69a752af&is=69a6012f&hm=f67976d53c13a716509c98ad5723acf691ecf78c14ba3a02fc41ca032f63b37c&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142185844248677/IMG_7854.jpg?ex=69a752af&is=69a6012f&hm=7b1616c4df487091d05be89b6e00d233b813f4d921d13e67dd8f4032303c5ac5&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142193003663520/IMG_7855.jpg?ex=69a752b1&is=69a60131&hm=2843b81725faf93af12a0c34096f32dd0ae1a02a54c0e676a0e3738d89c888f6&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142193888919724/IMG_7856.jpg?ex=69a752b1&is=69a60131&hm=893449cee6eff6b843866c28063bfd4e8cf1aced0400a8a58adec89bb3eb22f2&",
    "https://cdn.discordapp.com/attachments/1465439833034985475/1478142194480189652/IMG_7857.jpg?ex=69a752b1&is=69a60131&hm=d1898cadc9238954322ddbea78dda33a91711ed5f4a3b8fa9aa8faecb180169f&"
]
havva_links = [
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
hentai_links = [
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
    return max(0, int(COOLDOWN - (time.time() - cooldowns[uid])))

def on_cd(uid):
    return cd_left(uid) > 0

def set_cd(uid):
    cooldowns[uid] = time.time()

async def resolve_user(arg):
    if arg.isdigit():
        return int(arg)
    user = await client.get_entity(arg)
    return user.id

async def user_tag(uid):
    try:
        u = await client.get_entity(uid)
        if u.username:
            return f"@{u.username}"
    except:
        pass
    return str(uid)

async def giphy_random(q):
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY}&q={q}&limit=50"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data = await r.json()
    gifs = [g["images"]["original"]["url"] for g in data["data"]]
    return random.choice(gifs)

async def send_random_link(e, links, delete_after=None):
    tries = 0
    max_tries = 5
    while tries < max_tries:
        try:
            link = random.choice(links)
            msg = await e.reply(file=link)
            if delete_after:
                await asyncio.sleep(delete_after)
                await msg.delete()
            return
        except Exception as err:
            print(f"Erreur lien: {err}")
            tries += 1
            await asyncio.sleep(0.3)
    await e.reply("😅 Aucun lien valide disponible...")

# ================= COMMANDES =================
# Sword
@client.on(events.NewMessage(pattern=r"\.sword"))
async def sword(e):
    if e.sender_id in blacklist:
        return await e.reply("⛔ Vous êtes blacklisté et ne pouvez pas utiliser cette commande")
    if on_cd(e.sender_id):
        return await e.reply(f"Attends encore {cd_left(e.sender_id)}s")
    set_cd(e.sender_id)
    await send_random_link(e, sword_links, delete_after=6)

# Havva
@client.on(events.NewMessage(pattern=r"\.havva"))
async def havva(e):
    if e.sender_id in blacklist:
        return await e.reply("⛔ Vous êtes blacklisté et ne pouvez pas utiliser cette commande")
    if on_cd(e.sender_id):
        return await e.reply(f"Attends encore {cd_left(e.sender_id)}s")
    set_cd(e.sender_id)
    await send_random_link(e, havva_links)

# Hentai
@client.on(events.NewMessage(pattern=r"\.hentai"))
async def hentai(e):
    if e.sender_id in blacklist:
        return await e.reply("⛔ Vous êtes blacklisté et ne pouvez pas utiliser cette commande")
    if on_cd(e.sender_id):
        return await e.reply(f"Attends encore {cd_left(e.sender_id)}s")
    set_cd(e.sender_id)
    await send_random_link(e, hentai_links, delete_after=6)

# Slap / Kiss
@client.on(events.NewMessage(pattern=r"\.(kiss|slap) (.+)"))
async def action(e):
    if e.sender_id in blacklist:
        return await e.reply("⛔ Vous êtes blacklisté et ne pouvez pas utiliser cette commande")
    if on_cd(e.sender_id):
        return await e.reply(f"Attends encore {cd_left(e.sender_id)}s")
    set_cd(e.sender_id)
    act = e.pattern_match.group(1)
    target = e.pattern_match.group(2)
    try:
        target_id = await resolve_user(target)
        target = await user_tag(target_id)
    except:
        pass
    sender = await user_tag(e.sender_id)
    await e.reply(f"{sender} {act} {target}")
    try:
        gif = await giphy_random(f"anime {act} gif")
        await e.reply(file=gif)
    except:
        await e.reply("😅 Aucun GIF anime/manga trouvé pour cette action...")

# ================= BLACKLIST COMMANDES =================
@client.on(events.NewMessage(pattern=r"\.blacklist"))
async def show_blacklist(e):
    if e.sender_id not in owners:
        return await e.reply("⛔ Seuls les propriétaires peuvent voir la blacklist")
    msg = "**👑 Propriétaires :**\n"
    for o in owners:
        msg += f"{await user_tag(o)}\n"
    msg += "\n**⛔ Blacklist :**\n"
    for u in blacklist:
        if u not in owners:
            msg += f"{await user_tag(u)}\n"
    await e.reply(msg)

# Ajouter à la blacklist
@client.on(events.NewMessage(pattern=r"\.bl (.+)"))
async def add_blacklist(e):
    if e.sender_id not in owners:
        return await e.reply("⛔ Seuls les propriétaires peuvent gérer la blacklist")
    uid = await resolve_user(e.pattern_match.group(1))
    if uid in owners:
        return await e.reply("⛔ Impossible de blacklist un propriétaire !")
    blacklist.add(uid)
    with open("blacklist.txt", "w") as f:
        for u in blacklist:
            f.write(f"{u}\n")
    await e.reply(f"✅ {await user_tag(uid)} ajouté à la blacklist")

# Retirer de la blacklist
@client.on(events.NewMessage(pattern=r"\.unbl (.+)"))
async def remove_blacklist(e):
    if e.sender_id not in owners:
        return await e.reply("⛔ Seuls les propriétaires peuvent gérer la blacklist")
    uid = await resolve_user(e.pattern_match.group(1))
    if uid in blacklist:
        blacklist.remove(uid)
        with open("blacklist.txt", "w") as f:
            for u in blacklist:
                f.write(f"{u}\n")
        await e.reply(f"✅ {await user_tag(uid)} retiré de la blacklist")
    else:
        await e.reply("❌ L'utilisateur n'est pas dans la blacklist")

# ================= RUN =================
async def main():
    await client.start()
    print("USERBOT ONLINE")
    await client.run_until_disconnected()

asyncio.run(main())
