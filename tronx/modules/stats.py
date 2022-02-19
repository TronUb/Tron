from tronx import app
from tronx.helpers import gen
from pyrogram.types import Message




@app.on_message(gen("stats"))
async def dialog_stats(_, m: Message):
	try:
		m = await app.send_edit(m, "Getting stats . . .", mono=True)

		bot = 0
		user = 0
		group = 0
		channel = 0
		stat_format = f"""
		• **STATS FOR:** {}

		> **BOTS:** {}
		> **USERS:** {}
		> **GROUPS:** {}
		> **CHANNELS:** {}
		"""

		async for x in app.iter_dialogs():
			if x.chat.type == "channel":
				channel += 1
			if x.chat.type == "bot":
				bot += 1
			if x.chat.type in ("supergroup", "group"):
				group += 1
			if x.chat.type == "private":
				user += 1

		await app.send_edit(m, stat_format.format(bot, user, group, channel))
	except Exception as e:
		await app.error(m, e)