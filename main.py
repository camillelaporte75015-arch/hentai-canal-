import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.custom import Button
from flask import Flask
import threading
import locale

# ================= CONFIG =================
API_ID = 36767235
API_HASH = "6a36bf6c4b15e7eecdb20885a13fc2d7"
BOT_TOKEN = "8705272085:AAFA5k3ZD9w0_6S-z3C56fgAZEgVMBY-XOM"

# Canal messages anonymes
ANON_CHANNEL_ID = -1003207447518  # https://t.me/assistante

# Groupe logs
LOGS_CHANNEL_ID = -1003769561519  # https://t.me/djsbsjalalisbsbz

# ================= CLIENT =================
client = TelegramClient("anon_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ================= KEEP ALIVE =================
app = Flask("")

@app.route("/")
def home():
    return "Bot en ligne!"

threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()

# ================= DATE FR =================
try:
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
except:
    pass

def format_date():
    now = datetime.now()
    return now.strftime("%d %B - %H:%M %Ss")

# ================= ÉTATS =================
user_states = {}

# ================= COMMANDES =================

@client.on(events.NewMessage(pattern=r"^/start$"))
async def start(event):
    if not event.is_private:
        return
    await event.respond(
        "Salut ! Je peux t'aider à envoyer des messages anonymes. Utilise /anonyme pour commencer."
    )

@client.on(events.NewMessage(pattern=r"^/anonyme$"))
async def start_anonyme(event):
    if not event.is_private:
        return

    user_states[event.sender_id] = {
        "step": "ask_name",
        "media": []
    }

    await event.respond(
        "Quel est le @ ou prénom de la personne à qui tu veux envoyer le message ?"
    )

# ================= GESTION =================

@client.on(events.NewMessage)
async def handle_message(event):

    if not event.is_private:
        return

    if event.text and event.text.startswith("/"):
        return

    uid = event.sender_id

    if uid not in user_states:
        return

    state = user_states[uid]

    if state["step"] == "ask_name":
        state["dest_name"] = event.text.strip()
        state["step"] = "ask_text"
        await event.respond("Maintenant envoie le texte du message :")
        return

    if state["step"] == "ask_text":
        if not event.text:
            await event.respond("Tu dois envoyer un texte.")
            return

        state["text"] = event.text.strip()
        state["step"] = "ask_media"

        await event.respond(
            "Tu peux envoyer des photos/vidéos (optionnel).\n"
            "Quand tu as terminé, tape /done"
        )
        return

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
            await event.respond("Photo ajoutée.")
            return

        if event.video:
            state["media"].append(event.video)
            await event.respond("Vidéo ajoutée.")
            return

        await event.respond("Envoie un média ou tape /done.")
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

        final_text = (
            header +
            text +
            "\n\nSauras-tu savoir qui a écrit ce message ? 👀"
        )

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

        user = await client.get_entity(uid)

        log_text = (
            "**Logs des messages anonymes**\n\n"
            f"UserID: {uid}\n"
            f"Username: @{user.username if user.username else 'N/A'}\n"
            f"Date: {format_date()}\n"
            f"Message: {text}\n"
            f"Médias envoyés: {len(media)}"
        )

        await client.send_message(LOGS_CHANNEL_ID, log_text)

        await event.respond("Message envoyé anonymement ✅")

        user_states.pop(uid)

# ================= LANCEMENT =================
print("Bot lancé...")
client.run_until_disconnected()
