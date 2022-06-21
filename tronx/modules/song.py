import asyncio
from pyrogram.types import Message

from tronx import app, gen




app.CMD_HELP.update(
	{"song" : (
		"song",
		{
		"ly [song title]" : "Get Song Lyrics [ Japanese Songs Doesn't Work For Now.]",
		"song [song name]" : "Get songs in mp3 format.",
		"dz [song name]" : "Get songs from deezer bot in mp3 format."
		}
		)
	}
)




@app.on_message(gen(["song", "music"], allow = ["sudo", "channel"]))
async def song_handler(_, m: Message):
	await app.send_edit("Getting song . . .")
	try:
		cmd = m.command
		reply = m.reply_to_message
		if len(cmd) > 1:
			song_name = m.text.split(None, 1)[1]
		elif reply and len(cmd) == 1:
			song_name = reply.text or reply.caption
		elif not reply and len(cmd) == 1:
			return await app.send_edit("Give me a song name . . .", text_type=["mono"], delme=3)

		song_results = await app.get_inline_bot_results("audio_storm_bot", song_name)

		try:
			# send to Saved Messages because hide_via doesn't work sometimes
			saved = await app.send_inline_bot_result(
				chat_id="me",
				query_id=song_results.query_id,
				result_id=song_results.results[0].id,
				hide_via=True,
			)

			# forward as a new message from Saved Messages
			saved = await app.get_messages("me", int(saved.updates[1].message.id))
			reply_to = m.reply_to_message.message_id if m.reply_to_message else None

			await app.send_audio(
				chat_id=m.chat.id,
				audio=str(saved.audio.file_id),
				reply_to_message_id=reply_to,
				caption=f"**Song:** `{song_name}`\n**Uploaded By:** {app.UserMention()}",
			)

			# delete the message from Saved Messages
			await app.delete_messages("me", saved.message_id)
		except TimeoutError:
			return await app.send_edit("Something went wrong, tru again !")
	except Exception as e:
		await app.error(e)
		await app.send_edit("failed to process your request, please check logs")




@app.on_message(gen(["dz", "deezer"], allow = ["sudo", "channel"]))
async def deezer_handler(_, m: Message):
	try:
		await app.send_edit("Searching on deezer . . .")
		cmd = m.command
		reply = m.reply_to_message
		if app.long() > 1:
			song_name = m.text.split(None, 1)[1]
		elif reply and app.long() == 1:
			song_name = reply.text or reply.caption
		elif not reply and app.long() == 1:
			return await app.send_edit("Give a song name . . .", delme=3, text_type=["mono"])

		song_results = await app.get_inline_bot_results("DeezerMusicBot", song_name)

		try:
			# send to Saved Messages because hide_via doesn't work sometimes
			saved = await app.send_inline_bot_result(
				chat_id="me",
				query_id=song_results.query_id,
				result_id=song_results.results[0].id,
			)

			# forward as a new message from Saved Messages
			saved = await app.get_messages("me", int(saved.updates[1].message.id))
			reply_to = m.reply_to_message.message_id if m.reply_to_message else None

			await app.send_audio(
				chat_id=m.chat.id,
				audio=str(saved.audio.file_id),
				reply_to_message_id=reply_to,
				caption=f"**Song:** `{song_name}`\n**Uploaded By:** {app.UserMention()}",
			)

			# delete the message from Saved Messages
			await app.delete_messages("me", [saved.message_id, m.message_id])
		except TimeoutError:
			return await app.send_edit("Something went wrong, try again . . .", delme=3, text_type=["mono"])
	except Exception as e:
		await app.error(e)
		await app.send_edit("Something went wrong, try again !", text_type=["mono"], delme=3)




@app.on_message(gen(["ly", "lyrics"], allow = ["sudo", "channel"]))
async def lyrics_handler(_, m: Message):
	try:
		cmd = m.command
		reply = m.reply_to_message

		if not reply and len(cmd) > 1:
			song_name = m.text.split(None, 1)[1]
		elif reply:
			if reply.audio:
				song_name = f"{reply.audio.title} {reply.audio.performer}"
			elif reply.text or reply.caption and len(cmd) == 1:
				song_name = reply.text or reply.caption
			elif reply.text and len(cmd) > 1:
				song_name = m.text.split(None, 1)[1]
			else:
				return await app.send_edit("Give me a song name . . .", text_type=["mono"], delme=3)

		elif not reply and len(cmd) == 1:
			return await app.send_edit("Give me a song name . . .", text_type=["mono"], delme=3)

		await app.send_edit(f"**Finding lyrics for:** `{song_name}`")

		lyrics_results = await app.get_inline_bot_results("ilyricsbot", song_name)

		try:
			# send to cloud because hide_via doesn't work sometimes
			saved = await app.send_inline_bot_result(
				chat_id="me",
				query_id=lyrics_results.query_id,
				result_id=lyrics_results.results[0].id,
				hide_via=True,
			)
			await asyncio.sleep(0.50)

			# forward from Saved Messages
			await app.copy_message(
				chat_id=m.chat.id,
				from_chat_id="me",
				message_id=saved.updates[1].message.id,
			)

			# delete the message from Saved Messages
			await app.delete_messages("me", saved.updates[1].message.id)
		except TimeoutError:
			return await app.send_edit("Something went Wrong !", text_type=["mono"], delme=3)
	except Exception as e:
		await app.error(e)
		await app.send_edit("Something went wrong, please try again later !", text_type=["mono"], delme=3)
