import os
import asyncio

from sys import platform

from pyrogram import filters
from pyrogram.types import Message, User

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX
	)

from tronx.helpers import (
	gen,
	error,
	mymention,
	send_edit,
)




name = os.getenv("BOT_OWNER_USERNAME", "tronuserbot")

owner_name = name.replace("@", "")


CMD_HELP.update(
    {
        "song": f"""
**PLUGIN:** `song`\n\n
**COMMAND:** `{PREFIX}lyrics «song title»` or `{PREFIX}ly «song title»` \n**USAGE:** Get Song Lyrics [ Japanese Songs Doesn't Work For Now.]"\n\n
**COMMAND:** `{PREFIX}song «song name»` or `{PREFIX}music «song name»` \n**USAGE:** Get songs in mp3 format.\n\n
**COMMAND:** `{PREFIX}dz «song name»` or `{PREFIX}deezer «song name»` \n**USAGE:**  Get songs from deezer bot in mp3 format.\n\n
"""
    }
)


@app.on_message(gen(["song", "music"]))
async def send_music(_, m: Message):
	await send_edit(
		m, 
		"Getting song ..."
		)
	try:
		cmd = m.command
		song_name = ""
		if len(cmd) > 1:
			song_name = " ".join(cmd[1:])
		elif m.reply_to_message and len(cmd) == 1:
			song_name = (
				m.reply_to_message.text or m.reply_to_message.caption
			)
		elif not m.reply_to_message and len(cmd) == 1:
			await m.edit("Give a song name")
			await asyncio.sleep(2)
			await m.delete()
			return

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
			reply_to = (
				m.reply_to_message.message_id
				if m.reply_to_message
				else None
			)
			await app.send_audio(
				chat_id=m.chat.id,
				audio=str(saved.audio.file_id),
				reply_to_message_id=reply_to,
				caption=f"**Song:** `{song_name}`\n**Uploaded By:** {mymention()}",
			)

			# delete the message from Saved Messages
			await app.delete_messages("me", saved.message_id)
		except TimeoutError:
			await m.edit("That didn't work out")
			await asyncio.sleep(2)
		await m.delete()
	except Exception as e:
		await error(m, e)
		await send_edit(
			m, 
			"`Failed to find song ...`"
			)
		await asyncio.sleep(2)
		await m.delete()




@app.on_message(gen(["dz", "deezer"]))
async def send_music(_, m: Message):
	await send_edit(
		m, 
		"Searching on deezer ..."
		)
	try:
		cmd = m.command
		song_name = ""
		if len(cmd) > 1:
			song_name = " ".join(cmd[1:])
		elif m.reply_to_message and len(cmd) == 1:
			song_name = (
				m.reply_to_message.text or m.reply_to_message.caption
			)
		elif not m.reply_to_message and len(cmd) == 1:
			await send_edit(
				m, 
				"Give a song name"
				)
			await asyncio.sleep(1.50)
			await m.delete()
			return

		song_results = await app.get_inline_bot_results("DeezerMusicBot", song_name)

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
			reply_to = (
				m.reply_to_message.message_id
				if m.reply_to_message
				else None
			)
			await app.send_audio(
				chat_id=m.chat.id,
				audio=str(saved.audio.file_id),
				reply_to_message_id=reply_to,
				caption=f"**Song:** `{song_name}`\n**Uploaded By:** {mymention()}",
			)

			# delete the message from Saved Messages
			await app.delete_messages("me", saved.message_id)
		except TimeoutError:
			await send_edit(
				m, 
				"That didn't work out"
				)
		await asyncio.sleep(2)
		await m.delete()
	except Exception as e:
		await error(m, e)
		await send_edit(
			m, 
			"`Failed to find song`"
			)
		await asyncio.sleep(2)
		await m.delete()




@app.on_message(gen(["ly", "lyrics"]))
async def lyrics(_, m: Message):
	try:
		cmd = m.command

		song_name = ""
		if len(cmd) > 1:
			song_name = " ".join(cmd[1:])
		elif m.reply_to_message:
			if m.reply_to_message.audio:
				song_name = f"{m.reply_to_message.audio.title} {m.reply_to_message.audio.performer}"
			elif len(cmd) == 1:
				song_name = m.reply_to_message.text
		elif not m.reply_to_message and len(cmd) == 1:
			await send_edit(
				m, 
				"Give me a song name..."
				)
			await asyncio.sleep(2)
			await m.delete()
			return

		await send_edit(
			m, 
			f"Finding lyrics for •> `{song_name}`"
			)
		lyrics_results = await app.get_inline_bot_results("ilyricsbot", song_name)

		try:
			# send to cloud because hide_via doesn't work sometimes
			saved = await app.send_inline_bot_result(
				chat_id="me",
				query_id=lyrics_results.query_id,
				result_id=lyrics_results.results[0].id,
				hide_via=True,
			)
			await asyncio.sleep(3)

			# forward from Saved Messages
			await app.copy_message(
				chat_id=m.chat.id,
				from_chat_id="me",
				message_id=saved.updates[1].message.id,
			)

			# delete the message from Saved Messages
			await app.delete_messages("me", saved.updates[1].message.id)
		except TimeoutError:
			await send_edit(
				m, 
				"Something went Wrong !"
				)
			await asyncio.sleep(2)
			await m.delete()
	except Exception as e:
		await error(m, e)
		await send_edit(
			m, 
			"`Failed to get the lyrics !`"
			)
		await asyncio.sleep(2)
		await m.delete()
