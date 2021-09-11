import re
import os
import time
import json
import math
import asyncio
import traceback

from io import BytesIO

from pySmartDL import SmartDL
from datetime import datetime

from pyrogram import filters, errors
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP, 
	log,
	Config,
	PREFIX
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
	# others 
	progress_for_pyrogram, 
	humanbytes, 
	is_thumb_image_exists, 
	clear_string, 
	get_directory_size,
	delete,
	long,
)




CMD_HELP.update(
	{"download" : (
		"download",
		{
		"ls" : "Find file location in the local directories.",
		"download [Reply to media]" : "Downloads media files in local server.",
		"dl [reply to file]" : "Downloads media files in local server.",
		"upload [path]" : "Upload files from local server to telegram",
		"ul [path]" : "Upload files from local server to telegram.",
		"batchup [path]" : "Upload batch files from a local directories."
		}
		)
	}
)




#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.on_message(gen("ls"))
async def list_directories(_, m: Message):
	if len(m.text.split()) == 1:
		location = "."
	elif len(m.text.split()) >= 2:
		location = m.text.split(None, 1)[1]
	await send_edit(m, "Fetching files...")

	location = os.path.abspath(location)
	if not location.endswith("/"):
		location += "/"
	OUTPUT = f"Files in `{location}`:\n\n"
	try:
		files = os.listdir(location)
		files.sort()  # Sort the files
	except FileNotFoundError:
		await send_edit(m, f"No such file or directory {location}", delme=2)
		return
	for file in files:
		OUTPUT += f"• `{file}` ({get_directory_size(os.path.abspath(location+file))})\n"
	if len(OUTPUT) > 4096:
		OUTPUT = clear_string(OUTPUT)  # Remove the html elements using regex
		with BytesIO(str.encode(OUTPUT)) as f:
			f.name = "dict.txt"
			await app.send_document(
				m.chat.id,
				document=f,
				caption=f"`{location} ({get_directory_size(os.path.abspath(location))})`",
			)
		await m.delete()
	else:
		if OUTPUT.endswith("\n\n"):
			await send_edit(m, f"No files in {location}", delme=2)
			return
		await send_edit(m, OUTPUT)
	return




@app.on_message(gen(["download", "dl"]))
async def download_media(_, m: Message):
	await send_edit(m, "⏳ •Downloading...")
	if m.reply_to_message is not None:
		try:
			start_t = datetime.now()
			c_time = time.time()
			the_real_download_location = await app.download_media(
				message=m.reply_to_message,
				file_name="/app/tronx/downloads/",
				progress=progress_for_pyrogram,
				progress_args=("**__Trying to download . . .__**", c_time),
			)
			end_t = datetime.now()
			ms = (end_t - start_t).seconds
			await send_edit(
				m, 
				f"**Downloaded to •>**\n\n```{the_real_download_location}```\n\n**Time:** `{ms}` **seconds**",
				parse_mode="markdown",
			)
		except Exception:
			exc = traceback.format_exc()
			await send_edit(m, f"Failed To Download!\n{exc}")
			return
	elif long(m) > 1:
		try:
			start_t = datetime.now()
			the_url_parts = " ".join(m.command[1:])
			url = the_url_parts.strip()
			custom_file_name = os.path.basename(url)
			if "|" in the_url_parts:
				url, custom_file_name = the_url_parts.split("|")
				url = url.strip()
				custom_file_name = custom_file_name.strip()
			download_file_path = os.path.join("/app/tronx/downloads/", custom_file_name)
			downloader = SmartDL(url, download_file_path, progress_bar=False)
			downloader.start(blocking=False)
			c_time = time.time()
			while not downloader.isFinished():
				total_length = downloader.filesize if downloader.filesize else None
				downloaded = downloader.get_dl_size()
				display_message = ""
				now = time.time()
				diff = now - c_time
				percentage = downloader.get_progress() * 100
				speed = downloader.get_speed(human=True)
				elapsed_time = round(diff) * 1000
				progress_str = "**[{0}{1}]**\n**Progress:** __{2}%__".format(
					"".join(["●" for i in range(math.floor(percentage / 5))]),
					"".join(["○" for i in range(20 - math.floor(percentage / 5))]),
					round(percentage, 2),
				)
				estimated_total_time = downloader.get_eta(human=True)
				try:
					current_message = f"__**Trying to download...**__\n"
					current_message += f"**URL:** `{url}`\n"
					current_message += f"**File Name:** `{custom_file_name}`\n"
					current_message += f"{progress_str}\n"
					current_message += (
						f"__{humanbytes(downloaded)} of {humanbytes(total_length)}__\n"
					)
					current_message += f"**Speed:** __{speed}__\n"
					current_message += f"**ETA:** __{estimated_total_time}__"
					if round(diff % 10.00) == 0 and current_message != display_message:
						await send_edit(
							m,
							disable_web_page_preview=True, 
							text=current_message
						)
						display_message = current_message
						await asyncio.sleep(2)
				except errors.MessageNotModified:  # Don't log error if Message is not modified
					pass
				except Exception as e:
					log.info(str(e))
					pass
			if os.path.exists(download_file_path):
				end_t = datetime.now()
				ms = (end_t - start_t).seconds
				await sm.edit(
					f"Downloaded to •> <code>{download_file_path}</code> in <u>{ms}</u> seconds.\nDownload Speed: {round((total_length/ms), 2)}",
					parse_mode="html",
				)
		except Exception:
			exc = traceback.format_exc()
			await send_edit(
				m, 
				f"Failed Download!\n{exc}"
				)
			return
	else:
		await send_edit("`Reply to a Telegram Media to download it to local server.`", delme=2)
	return


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.on_message(gen(["upload", "ul"]))
async def upload_as_document(_, m: Message):
	await send_edit(m, "`...`")

	if long(m) > 1:
		local_file_name = m.text.split(None, 1)[1]
		if os.path.exists(local_file_name):
			await send_edit(
				m, 
				"`Uploading...`"
				)
			start_t = datetime.now()
			c_time = time.time()
			doc_caption = os.path.basename(local_file_name)
			await send_edit(m,f"Uploading __{doc_caption}__...")

			await m.reply_document(
				document=local_file_name,
				caption=doc_caption,
				parse_mode="html",
				disable_notification=True,
				reply_to_message_id=m.message_id,
				progress=progress_for_pyrogram,
				progress_args=("Uploading file...", m, c_time),
			)

			end_t = datetime.now()
			ms = (end_t - start_t).seconds
			await send_edit(m, f"**Uploaded in {ms} seconds**", delme=2)
		else:
			await send_edit(
				m, 
				"404: media not found ..."
				)
	else:
		await send_edit(m, f"`{PREFIX}upload [file path ]` to upload to current Telegram chat", delme=2)
	return


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.on_message(gen("batchup"))
async def covid(_, m: Message):
	if len(m.text.split()) == 1:
		await send_edit(m, "`Give me a location to upload files from the directory ...`", delme=2)
		return

	elif len(m.text.split()) >= 2:
		temp_dir = m.text.split(None, 1)[1]
		if not temp_dir.endswith("/"):
			temp_dir += "/"
	await send_edit(m, "`Uploading Files to Telegram...`")

	if os.path.exists(temp_dir):
		try:
			files = os.listdir(temp_dir)
			files.sort()
			for file in files:
				if not file.startswith("__"):
					c_time = time.time()
					required_file_name = temp_dir + file
					thumb_image_path = await is_thumb_image_exists(required_file_name)
					doc_caption = os.path.basename(required_file_name)
					log.info(
						f"Uploading <i>{required_file_name}</i> from {temp_dir} to Telegram."
					)
					await app.send_document(
						chat_id=m.chat.id,
						document=required_file_name,
						thumb=thumb_image_path,
						caption=doc_caption,
						disable_notification=True,
						progress=progress_for_pyrogram,
						progress_args=(
							f"Trying to upload __{file}__",
							sm,
							c_time,
						),
					)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(m, "Directory Not Found ...", delme=2)
		return
	await send_edit(m, f"Uploaded all files from Directory `{temp_dir}`", delme=3)
	log.info("Uploaded all files in batch !!")
	return
