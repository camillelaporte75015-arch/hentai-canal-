@client.on(events.NewMessage(pattern=r"\.clear"))
async def clear_handler(event):

    sender_id = event.sender_id

    # ===== COOLDOWN =====
    remaining = check_cooldown(sender_id)
    if remaining > 0:
        await event.reply(f"⏳ veuillez patienter {remaining}s")
        return

    args = event.raw_text.split()

    if len(args) < 2:
        await event.reply("Utilisation:\n.clear 20\n.clear @username")
        return

    target = args[1]
    chat = await event.get_chat()

    # ================= CLEAR PAR NOMBRE =================
    if target.isdigit():

        number = int(target)
        if number > 20:
            number = 20

        deleted = 0

        async for msg in client.iter_messages(chat.id, limit=number):
            try:
                await msg.delete()
                deleted += 1
                await asyncio.sleep(0.3)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)

        await event.reply(f"🧹 {deleted} message(s) supprimé(s).")
        return

    # ================= CLEAR PAR @ (GROUPES / CANAUX) =================
    if target.startswith("@"):

        username = target.replace("@", "").lower()
        deleted = 0

        async for msg in client.iter_messages(chat.id, limit=1000):

            if msg.sender and msg.sender.username:
                if msg.sender.username.lower() == username:
                    try:
                        await msg.delete()
                        deleted += 1
                        await asyncio.sleep(0.3)
                    except FloodWaitError as e:
                        await asyncio.sleep(e.seconds)

                    if deleted >= 100:
                        break

        await event.reply(f"✅ {deleted} message(s) supprimé(s) pour @{username}.")
        return

    # ================= CLEAR EN DM =================
    if event.is_private:

        deleted = 0

        async for msg in client.iter_messages(chat.id, limit=100):
            try:
                await msg.delete()
                deleted += 1
                await asyncio.sleep(0.3)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)

        await event.reply(f"✅ {deleted} message(s) supprimé(s) en privé.")
        return
