import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.custom import Button
from flask import Flask
import threading

# ================= CONFIG =================
API_ID = 36767235
API_HASH = "6a36bf6c4b15e7eecdb20885a13fc2d7"
BOT_TOKEN = "8729391763:AAEVm0J0PKUoT8QHo5N15LnYlPFeHv70kqU"

ANON_CHANNEL_ID = -1003207447518
LOGS_CHANNEL_ID = -1003769561519

# ================= CLIENT =================
client = TelegramClient('anon_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ================= KEEP ALIVE (UPTIMEROBOT) =================
app = Flask("")

@app.route("/")
def home():
    return "Bot en ligne!"

threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()

# ================= ÉTATS =================
user_states = {}

def format_date():
    return datetime.now().strftime("%d %B - %H:%M %Ss")

# ================= COMMANDES =================
@client.on(events.NewMessage(pattern=r"/start"))
async def start(event):
    await event.respond(
        "Salut ! Je peux t'aider à envoyer des messages anonymes. Utilise /anonyme pour commencer."
    )

@client.on(events.NewMessage(pattern=r"/anonyme"))
async def start_anonyme(event):
    user_states[event.sender_id] = {
        "step": "ask_name",
        "media": []
    }
    await event.respond("Quel est le @ ou prénom de la personne à qui tu veux envoyer le message ?")

@client.on(events.NewMessage)
async def handle_message(event):
    uid = event.sender_id

    if uid not in user_states:
        return

    state = user_states[uid]

    # Étape 1 : destinataire
    if state["step"] == "ask_name":
        state["dest_name"] = event.text
        state["step"] = "ask_text"
        await event.respond("Maintenant envoie le texte du message :")
        return

    # Étape 2 : texte
    if state["step"] == "ask_text":
        state["text"] = event.text
        state["step"] = "ask_media"
        await event.respond(
            "Tu peux envoyer des photos/vidéos (optionnel). Quand tu as fini, tape /done"
        )
        return

    # Étape 3 : médias
    if state["step"] == "ask_media":

        if event.text and event.text.lower() == "/done":
            state["step"] = "confirm"
            buttons = [
                [Button.inline("✅", b"confirm_yes"),
                 Button.inline("❌", b"confirm_no")]
            ]
            await event.respond(
                "Es-tu sûr de vouloir envoyer ce message anonymement ? 👀",
                buttons=buttons
            )
            return

        if event.photo:
            state["media"].append(event.photo)
        if event.video:
            state["media"].append(event.video)

        await event.respond("Média ajouté. Continue ou tape /done.")
        return

# ================= CONFIRMATION =================
@client.on(events.CallbackQuery)
async def callback(event):
    uid = event.sender_id

    if uid not in user_states:
        return

    state = user_states[uid]

    if event.data == b"confirm_no":
        await event.respond("Envoi annulé ❌")
        user_states.pop(uid)
        return

    if event.data == b"confirm_yes":

        dest = state["dest_name"]
        text = state["text"]
        media = state["media"]

        if dest.startswith("@"):
            header = f"Quelqu’un a quelque chose à te dire {dest}\n\n"
        else:
            header = f"Quelqu’un a quelque chose à te dire ({dest})\n\n"

        final_text = header + text + "\n\nSauras-tu savoir qui a écrit ce message ? 👀"

        # Envoi canal
        if media:
            await client.send_file(
                ANON_CHANNEL_ID,
                file=media,
                caption=final_text
            )
        else:
            await client.send_message(
                ANON_CHANNEL_ID,
                final_text
            )

        # Logs
        user = await client.get_entity(uid)

        log_text = (
            "**Logs des messages anonymes**\n\n"
            f"UserID: {uid}\n"
            f"Username: @{user.username if user.username else 'N/A'}\n"
            f"Date: {format_date()}\n"
            f"Message: {text}\n"
            f"Médias envoyés: {len(media) if media else 0}"
        )

        await client.send_message(LOGS_CHANNEL_ID, log_text)

        await event.respond("Message envoyé anonymement ✅")
        user_states.pop(uid)

# ================= LANCEMENT DU BOT =================
print("Bot lancé...")
client.run_until_disconnected()
