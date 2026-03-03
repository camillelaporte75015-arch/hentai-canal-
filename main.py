from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import datetime

# ================= CONFIG =================
BOT_TOKEN = "8705272085:AAFdbGOdnFgcobP-mTbmEgUV9bHBurzaJ-Y"
OWNER_ID = 7891919458  # @botassistante
MAIN_CHANNEL_ID = -1003696703161  # Canal principal pour anonymes
LOGS_CHANNEL_ID = -1003769561519  # Canal pour logs

# Stockage temporaire des messages et médias
user_data = {}

# ================= UTIL =================
def format_date():
    now = datetime.datetime.now()
    return now.strftime("%d %B - %H:%M %Ss")

# ================= COMMANDES =================
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Salut ! Je peux t'aider à envoyer des messages anonymes. Utilise /anonyme pour commencer."
    )

def anonyme(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("✅", callback_data="confirm_yes"),
         InlineKeyboardButton("❌", callback_data="confirm_no")]
    ]
    update.message.reply_text(
        "Es-tu sûr de vouloir envoyer ce message anonymement ? 👀",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= CALLBACK =================
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    if query.data == "confirm_no":
        query.edit_message_text("❌ Envoi annulé.")
        if user_id in user_data:
            user_data.pop(user_id, None)
        return

    # confirm_yes
    query.edit_message_text("Envoie-moi ton message texte. Tu peux mettre un @ ou un prénom.")
    user_data[user_id] = {"text": "", "media": []}

def text_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_data or user_data[user_id]["text"]:
        return  # ignore si pas en train d'envoyer un message ou déjà reçu texte

    user_data[user_id]["text"] = update.message.text
    update.message.reply_text(
        "Envoie maintenant tes médias (photos, vidéos, etc.). Tu peux en envoyer plusieurs. "
        "Si pas de médias, tape /done"
    )

def media_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        return

    media_list = user_data[user_id]["media"]

    if update.message.photo:
        media_list.append(InputMediaPhoto(update.message.photo[-1].file_id))
    elif update.message.video:
        media_list.append(InputMediaVideo(update.message.video.file_id))

def done(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        return

    data = user_data.pop(user_id)
    text = data["text"]
    media = data["media"]

    # Envoi dans le canal principal
    context.bot.send_message(
        chat_id=MAIN_CHANNEL_ID,
        text=f"Quelqu’un a quelque chose à te dire @destinataire\n\n{text}\n\nSauras-tu savoir qui a écrit ce message ? 👀"
    )
    if media:
        context.bot.send_media_group(chat_id=MAIN_CHANNEL_ID, media=media)

    # Envoi des logs
    log_text = f"Logs des messages anonymes\nUserID: {user_id} / @{update.message.from_user.username or 'Aucun'}\n" \
               f"Message: {text}\n" \
               f"Media: {len(media)} fichier(s) attaché(s)\n" \
               f"Date: {format_date()}\n" \
               f"Channel: https://t.me/ahscwysksoaizvz"
    context.bot.send_message(chat_id=LOGS_CHANNEL_ID, text=log_text)

    update.message.reply_text("✅ Ton message a été envoyé anonymement !")

# ================= MAIN =================
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("anonyme", anonyme))
dp.add_handler(CommandHandler("done", done))
dp.add_handler(CallbackQueryHandler(button))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))
dp.add_handler(MessageHandler(Filters.photo | Filters.video, media_handler))

updater.start_polling()
updater.idle()
