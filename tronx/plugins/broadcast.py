from tronx import app
from pyrogram.filters import command, user
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid




@app.bot.on_message(command("broadcast") & user(app.id))    
async def broadcast_message(_, m: Message):
	tlen = len(m.text.split())
	
	if tlen == 1:
		await app.bot.send_message(m.from_user.id, "Give me some broadcasting message.")    
		return

	text = m.text.split(None, 1)[1]
	count = 0

	for ids in [int(x) for x in app.getdv("BOT_STARTED_ID").split()]:
		try:
			await app.bot.resolve(ids)
			done = await app.bot.send_message(ids, text)
			if done:
				count += 1
		except PeerIdInvalid:
			pass
	await app.bot.send_message(m.from_user.id, f"Broadcast done, messages sent to {count} users.")
