import asyncio
from datetime import datetime
from telethon import TelegramClient, events, types
from telethon.tl.types import InputMediaPhoto, InputMediaVideo
from flask import Flask
import threading

# ================= CONFIG =================
API_ID = 36767235
API_HASH = "6a36bf6c4b15e7eecdb20885a13fc2d7"
BOT_TOKEN = "8705272085:AAFA5k3ZD9w0_6S-z3C56fgAZEgVMBY-XOM"

# Canal où les messages anonymes seront envoyés
ANON_CHANNEL_ID = -1003207447518  # https://t.me/assistante

# Groupe pour recevoir les logs
LOGS_CHANNEL_ID = -1003769561519  # https://t.me/djsbsjalalisbsbz

# ID du seul utilisateur qui peut voir les logs
OWNER_ID = 7891919458  # @botassistante

# ================= CLIENT =================
client = TelegramClient('anon_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ================= KEEP ALIVE =================
app = Flask("")

@app.route("/")
def home():
    return "Bot en ligne!"

threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()

# ================= GESTION DES ÉTATS =================
# Pour chaque utilisateur, on garde son état
user_states = {}

# ================= UTIL =================
def format_date():
    return datetime.now().strftime("%d %B - %H:%M %Ss")

# ================= COMMANDES =================
@client.on(events.NewMessage(pattern=r"/start"))
async def start(event):
    await event.respond("Salut ! Je peux t'aider à envoyer des messages anonymes. Utilise /anonyme pour commencer.")

@client.on(events.NewMessage(pattern=r"/anonyme"))
async def start_anonyme(event):
    user_states[event.sender_id] = {"step": "ask_name", "media": []}
    await event.respond("Quel est le @ ou prénom de la personne à qui tu veux envoyer le message ?")

@client.on(events.NewMessage)
async def handle_message(event):
    uid = event.sender_id
    if uid not in user_states:
        return
    state = user_states[uid]

    # Étape 1: demander le prénom ou @
    if state["step"] == "ask_name":
        state["dest_name"] = event.text
        state["step"] = "ask_text"
        await event.respond("Maintenant, envoie-moi ton message texte à envoyer anonymement :")

    # Étape 2: demander le texte
    elif state["step"] == "ask_text":
        state["text"] = event.text
        state["step"] = "ask_media"
        await event.respond("Tu peux maintenant envoyer des photos/vidéos (optionnel). Envoie tout ce que tu veux puis tape /done quand c'est fini.")

    # Étape 3: récupérer les médias
    elif state["step"] == "ask_media":
        # Vérifie si l'utilisateur tape /done
        if event.text and event.text.lower() == "/done":
            state["step"] = "waiting_confirmation"
            # demander confirmation
            from telethon.tl.custom import Button
            buttons = [
                [Button.inline("✅", b"confirm_yes"), Button.inline("❌", b"confirm_no")]
            ]
            await event.respond("Es-tu sûr de vouloir envoyer ce message anonymement ? 👀", buttons=buttons)
            return

        # collecter les médias
        if event.photo:
            state["media"].append(InputMediaPhoto(event.photo))
        if event.video:
            state["media"].append(InputMediaVideo(event.video))

        await event.respond("Média ajouté. Tu peux en envoyer d'autres ou taper /done pour passer.")

# ================= CALLBACK POUR CONFIRMATION =================
@client.on(events.CallbackQuery)
async def callback(event):
    uid = event.sender_id
    if uid not in user_states:
        return
    state = user_states[uid]

    if state.get("step") != "waiting_confirmation":
        return

    if event.data == b"confirm_yes":
        # Préparer le message
        dest = state.get("dest_name", "")
        text = state.get("text", "")
        media = state.get("media", [])

        # Construire le texte
        if dest.startswith("@"):
            header = f"Quelqu’un a quelque chose à te dire {dest}\n"
        else:
            header = f"Quelqu’un a quelque chose à te dire ({dest})\n"

        final_message = f"{header}\n{text}\n\n"

        # Ajouter média si présent
        if media:
            # envoi d'un seul message media + texte
            await client.send_file(
                ANON_CHANNEL_ID,
                file=media,
                caption=final_message + "Sauras-tu savoir qui a écrit ce message ? 👀"
            )
        else:
            await client.send_message(
                ANON_CHANNEL_ID,
                final_message + "Sauras-tu savoir qui a écrit ce message ? 👀"
            )

        # Logs
        log_text = f"**Logs des messages anonymes**\n\n"
        log_text += f"UserID: {uid}\n"
        log_text += f"Username: @{(await client.get_entity(uid)).username or 'N/A'}\n"
        log_text += f"Date: {format_date()}\n"
        log_text += f"Message: {text}\n"
        if media:
            log_text += f"Médias envoyés: {len(media)} fichier(s)\n"
        else:
            log_text += "Médias envoyés: Aucun\n"

        await client.send_message(LOGS_CHANNEL_ID, log_text)

        await event.respond("Ton message a été envoyé anonymement ✅")
        user_states.pop(uid)

    elif event.data == b"confirm_no":
        await event.respond("Envoi annulé ❌")
        user_states.pop(uid)
