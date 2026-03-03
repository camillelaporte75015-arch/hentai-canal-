from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime
import threading
from flask import Flask

# ================= CONFIG =================
BOT_TOKEN = "8705272085:AAFdbGOdnFgcobP-mTbmEgUV9bHBurzaJ-Y"
LOGS_GROUP_ID = -1003769561519
ANON_CHANNEL_ID = -1003207447518
OWNER_ID = 7891919458  # ton id Telegram pour les logs

# ================= KEEP ALIVE FLASK =================
app = Flask("")

@app.route("/")
def home():
    return "Bot en ligne ! ✅"

threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()

# ================= BOT =================
application = ApplicationBuilder().token(BOT_TOKEN).build()

# stocke les états des utilisateurs
user_state = {}

# ================= COMMANDES =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salut ! Je peux t'aider à envoyer des messages anonymes. Utilise /anonyme pour commencer."
    )

async def anonyme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # démarrer le processus
    user_state[user_id] = {"step": "ask_target"}
    await update.message.reply_text(
        "Quel est le @ ou prénom de la personne destinataire ?"
    )

# ================= MESSAGE HANDLER =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_state:
        return  # pas dans le flux anonyme

    state = user_state[user_id]

    if state["step"] == "ask_target":
        state["target"] = update.message.text
        state["step"] = "ask_text"
        await update.message.reply_text(
            "Envoie maintenant le texte que tu veux envoyer anonymement."
        )

    elif state["step"] == "ask_text":
        state["text"] = update.message.text
        state["step"] = "ask_media"
        await update.message.reply_text(
            "Si tu veux, envoie maintenant des photos ou vidéos à joindre (sinon tape /done pour passer)."
        )

    elif state["step"] == "ask_media":
        if update.message.text and update.message.text.lower() == "/done":
            state["step"] = "confirm"
        else:
            # collecter médias
            if "media" not in state:
                state["media"] = []
            if update.message.photo:
                # récupérer la plus grande résolution
                state["media"].append(InputMediaPhoto(update.message.photo[-1].file_id))
            if update.message.video:
                state["media"].append(InputMediaVideo(update.message.video.file_id))
            await update.message.reply_text(
                "Média ajouté. Tu peux en envoyer d'autres ou taper /done pour passer."
            )
            return

        # demander confirmation
        keyboard = [
            [
                InlineKeyboardButton("✅", callback_data="confirm_yes"),
                InlineKeyboardButton("❌", callback_data="confirm_no")
            ]
        ]
        await update.message.reply_text(
            "Es-tu sûr de vouloir envoyer ce message anonymement ? 👀",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        state["step"] = "waiting_confirmation"

# ================= CALLBACKS =================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in user_state:
        return

    state = user_state[user_id]

    if query.data == "confirm_no":
        await query.edit_message_text("Envoi annulé.")
        user_state.pop(user_id)
        return

    if query.data == "confirm_yes":
        # envoyer le message dans le canal
        target = state.get("target")
        text = state.get("text")
        media = state.get("media", [])

        message_text = f"Quelqu’un a quelque chose à te dire {target}\n\n{text}\n\nSauras-tu savoir qui a écrit ce message ? 👀"

        if media:
            # si texte + médias
            media[0].caption = message_text
            await context.bot.send_media_group(chat_id=ANON_CHANNEL_ID, media=media)
        else:
            await context.bot.send_message(chat_id=ANON_CHANNEL_ID, text=message_text)

        # envoyer les logs dans le groupe
        log_text = f"**Logs des messages anonymes**\n\nUserID: {user_id} / @{update.effective_user.username if update.effective_user.username else ''}\nDate: {datetime.now().strftime('%d %B - %H:%M %Ss')}\nMessage: {text}\nMedia: {'Oui' if media else 'Aucun'}"
        await context.bot.send_message(chat_id=LOGS_GROUP_ID, text=log_text)

        await query.edit_message_text("Message envoyé avec succès ! ✅")
        user_state.pop(user_id)

# ================= HANDLERS =================
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("anonyme", anonyme))
application.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), handle_message))
application.add_handler(CallbackQueryHandler(button_callback))

# ================= RUN =================
application.run_polling()
