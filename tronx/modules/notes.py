import time

from pyrogram.types import (
	InlineKeyboardMarkup, 
	InlineKeyboardButton, 
	Message
)

from tronx import app

from tronx.helpers import (
	gen,
	regex,
)




app.CMD_HELP.update(
	{"notes" : (
		"notes",
		{
		"save [note mame ] [reply to message]" : "Save A Note Of Any Type Of Media In Your Database.", 
		">" : "Get Your Note. Example: `>mynote`, Where mynote is note name and command ( >)",
		"notes" : "Get Your Saved Note List.",
		"clear" : "Delete A Note."
		}
		)
	}
)




GET_FORMAT = {
	app.TEXT: app.send_message,
	app.DOCUMENT: app.send_document,
	app.PHOTO: app.send_photo,
	app.VIDEO: app.send_video,
	app.STICKER: app.send_sticker,
	app.AUDIO: app.send_audio,
	app.VOICE: app.send_voice,
	app.VIDEO_NOTE: app.send_video_note,
	app.ANIMATION: app.send_animation,
	app.ANIMATED_STICKER: app.send_sticker,
	app.CONTACT: app.send_contact
}




@app.on_message(gen("save", allow = ["sudo"]))
async def savenote_hanlder(_, m: Message):
	if len(m.command) < 2:
		return await app.send_edit(m, "A note name is required with command to save a note.", text_type=["mono"])

	if len(m.command) < 3:
		return await app.send_edit(m, "A note name & content is required to save a note.", text_type=["mono"])

	note_name, text, message_type, content = app.GetNoteType(m)
	if not note_name:
		return await app.send_edit(m, "A note name is necessary to save a note !", text_type=["mono"])

	if message_type == app.TEXT:
		file_id = None
		teks, button = app.ParseButton(text)
		if not teks:
			await app.send_edit(m, f"Text: `{m.text}`\n\nError: There is no text in here !")

	app.save_selfnote(m.from_user.id, note_name, text, message_type, content)
	await app.send_edit(m, "Saved note = **[ `{}` ]**".format(note_name))




@app.on_message(regex(">"))
async def getnote_handler(_, m: Message):
	reply = m.reply_to_message
	if m.text and m.text.startswith(">"):
		if app.long(m) == 1:
			note = m.text.replace(">", "")
		else:
			return # no response

		getnotes = app.get_selfnote(m.from_user.id, note)

		if not getnotes:
			return await app.send_edit(m, "This note does not exist !")

		msg_id = reply.message_id if reply else None

		if getnotes['type'] == app.TEXT:
			teks, button = app.ParseButton(getnotes.get('value'))
			button = app.BuildKeyboard(button)
			if button:
				button = InlineKeyboardMarkup(button)
			else:
				button = False
			if button:
				return await app.send_edit(m, "Inline button not supported in this userbot version :(")
			else:
				await app.send_edit(m, teks)

		elif getnotes['type'] in (app.STICKER, app.VOICE, app.VIDEO_NOTE, app.CONTACT, app.ANIMATED_STICKER):
			await m.delete()
			try:
				if msg_id:
					await GET_FORMAT[getnotes['type']](message.chat.id, getnotes['file'], reply_to_message_id=msg_id)
				else:
					await GET_FORMAT[getnotes['type']](message.chat.id, getnotes['file'])
			except errors.exceptions.bad_request_400.BadRequest:
				msg = await app.get_messages(m.chat.id, getnotes['message_id'])
				note_name, text, message_type, content = app.FetchNoteType(msg)
				app.save_selfnote(m.chat.id, note, "", getnotes['type'], content, getnotes['message_id'])
				if msg_id:
					await GET_FORMAT[getnotes['type']](m.chat.id, content, reply_to_message_id=msg_id)
				else:
					await GET_FORMAT[getnotes['type']](m.chat.id, content)
		else:
			await m.delete()
			if getnotes.get('value'):
				teks, button = app.ParseButton(getnotes.get('value'))
				button = app.BuildKeyboard(button)
				if button:
					button = InlineKeyboardMarkup(button)
				else:
					button = False
			else:
				teks = False
				button = False

			if button:
				return await app.send_edit(m, "Inline button not supported in this userbot.")
			else:
				try:
					if msg_id:
						await GET_FORMAT[getnotes['type']](m.chat.id, getnotes['file'], caption=teks, reply_to_message_id=msg_id)
					else:
						await GET_FORMAT[getnotes['type']](m.chat.id, getnotes['file'], caption=teks)
				except errors.exceptions.bad_request_400.BadRequest:
					msg = await app.get_messages(m.chat.id, getnotes['message_id'])
					note_name, text, message_type, content = app.FetchNoteType(msg)
					app.save_selfnote(m.chat.id, note, teks, getnotes['type'], content, getnotes['message_id'])
					if msg_id:
						await GET_FORMAT[getnotes['type']](m.chat.id, getnotes['file'], caption=teks, reply_to_message_id=msg_id)
					else:
						await GET_FORMAT[getnotes['type']](m.chat.id, getnotes['file'], caption=teks)
	else:
		return




@app.on_message(gen("notes", allow = ["sudo"]))
async def notelist_handler(_, m: Message):	
	getnotes = app.get_all_selfnotes(m.from_user.id)
	if not getnotes:
		return await app.send_edit(m, "There are no saved notes !", text_type=["mono"], delme=4)

	notelist = "**NOTEBOOK:**\n\n"
	for x in getnotes:
		notelist += f"`>{x}`\n"

	await app.send_edit(m, notelist)




@app.on_message(gen("clear"))
async def clearnote_handler(_, m: Message):	
	if app.long(m) <= 1:
		return await app.send_edit(m, f"Sir, give me a note name after command, Ex: `{app.PREFIX}clear cat`")

	notename = m.text.split()[1]
	getnotes = app.rm_selfnote(m.from_user.id, notename)
	if not getnotes:
		return await app.send_edit(m, "This note does not exist!")
	else:
		await app.send_edit(m, f"Deleted note = **[ `{notename}` ]**")
        
