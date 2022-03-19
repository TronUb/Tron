import os
import sys
import time
import shutil
import asyncio
import zipfile
from pathlib import Path

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"zip" : (
		"zip",
		{
		"zip [reply to file]" : "Zip a file and save it in your local directories.",
		"unzip [file path]" : "Unzip a file and save it in your local directories.",
		"new [file name]" : "Create a python file with your codes."
		}
		)
	}
)




def zipdir(dirName):
	dice = []
	for root, directories, files in os.walk(dirName):
		for filename in files:
			filePath = os.path.join(root, filename)
			dice.append(filePath)
	return filePaths


async def unzipfiles(zippath):
	foldername = zippath.split("/")[-1]
	extract_path = f"tronx/downloads/{foldername}"
	shutil.unpack_archive(zippath, extract_path)
	return extract_path




@app.on_message(gen("zip", allow =["sudo"]))
async def zip_handler(_, m: Message):
	reply = m.reply_to_message
	if not reply:
		return await app.send_edit(m, f"Reply to some media file . . .", text_type=["mono"], delme=4)

	elif reply:
		if not reply.media:
			return await app.send_edit(m, "Reply to some media not text . . .", text_type=["mono"])

		m = await app.send_edit(m, "Zipping . . .", text_type=["mono"])

		if app.TEMP_DICT:
			loc = app.TEMP_DICT
		else:
			loc = "./downloads"
		dl = await app.download_media(
			reply,
			block=False
		)
		zipfile.ZipFile(dl.replace("/app/downloads/", "") + ".zip", "w").write(dl)
		place = dl.replace("/app/downloads/", "") + ".zip"
		await app.send_edit(m, f"**Your file is compressed and saved here:** \n`{place}`")
	else:
		await app.send_edit(m, "Something went wrong . . .", delme=2, text_type=["mono"])




@app.on_message(gen("unzip", allow =["sudo"]))
async def unzip_handler(_, m: Message):
	if app.long(m) == 2:
		if app.long(m) <= 4096:
			loc = m.text.split(None, 1)[1]
			m = await app.send_edit(m, "Unzipping file . . .", text_type=["mono"])
			extract_path = await unzipfiles(loc)
			await app.send_edit(m, f"File unzipped and saved here: `{extract_path}`")
		else:
			await app.send_edit(m, "Text is too long !", delme=2, text_type=["mono"])
	else:
		await app.send_edit(m, "Give me the file path to unzip the file . . .", delme=4, text_type=["mono"])




@app.on_message(gen("new", allow =["sudo"]))
async def createfile_handler(app, m:Message):
	reply = m.reply_to_message
	mytext = "Making file . . ."
	oldmsg = m # workaround
	filepath = None

	try:
		if app.textlen(m) > 4096:
			return await app.send_edit(m, "The message is too long. (it must be <= 4096)", delme=4, text_type=["mono"])

		if app.long(m) == 1:
			return await app.send_edit(m, "Give me filename & content of file after command.", text_type=["mono"], delme=4)

		if reply and app.long(m) >= 2:
			name = oldmsg.text.split(None, 1)[1]
			m = await app.send_edit(m, mytext, text_type=["mono"])
			text = reply.text or reply.caption
			await app.create_file(
				message=m, 
				filename=name, 
				content=text,
				send=True
			)

		# if replied to text without file name
		elif not reply and app.long(m) >= 3:
			m = await app.send_edit(m, mytext, text_type=["mono"])
			name = oldmsg.text.split(None, 1)[1]
			text = oldmsg.text.split(None, 2)[2]
			await app.create_file(
				message=m, 
				filename="file.py", 
				content=text,
				send=True
			)

		# if replied to text with file name
		elif not reply and app.long(m) <= 2:
			await app.send_edit(m, "Are you dumb, give me the file contents with the file name.", text_type=["mono"], delme=4)

		else:
			await app.send_edit(m, "Something went wrong !")

	except Exception as e:
		await app.error(m, e)





