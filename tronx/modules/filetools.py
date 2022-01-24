import os
import sys
import time
import shutil
import asyncio
import zipfile
from pathlib import Path

from pyrogram.types import Message
from pyrogram import filters, Client

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




@app.on_message(gen("zip"))
async def zipit(_, m: Message):
	reply = m.reply_to_message
	if not reply:
		return await app.send_edit(m, f"Reply to some media file . . .", mono=True, delme=2)

	elif reply:
		if not reply.media:
			return await app.send_edit(m, "Reply to some media not text . . .", mono=True)
		await app.send_edit(m, "Zipping . . .", mono=True)

		if app.TEMP_DICT:
			loc = app.TEMP_DICT
		else:
			loc = "tronx/downloads"
		dl = await app.download_media(
			reply,
			block=False
		)
		zipfile.ZipFile(dl.replace("/app/downloads/", "") + ".zip", "w").write(dl)
		place = dl.replace("/app/downloads/", "") + ".zip"
		await app.send_edit(m, f"**Your file is compressed and saved here:** \n`{place}`")
	else:
		await app.send_edit(m, "Something went wrong . . .", delme=2, mono=True)




@app.on_message(gen("unzip"))
async def unzipit(_, m: Message):
	if app.long(m) == 2:
		if app.long(m) <= 4096:
			loc = m.text.split(None, 1)[1]
			await app.send_edit(m, "Unzipping file . . .", mono=True)
			extract_path = await unzipfiles(loc)
			await app.send_edit(m, f"File unzipped and saved here: `{extract_path}`")
		else:
			await app.send_edit(m, "Text is too long !", delme=2, mono=True)
	else:
		await app.send_edit(m, "Give me the file path to unzip the file . . .", delme=2, mono=True)




@app.on_message(gen("new"))
async def create_anyfile(app, m:Message):
	reply = m.reply_to_message
	await app.send_edit(m, "making file . . .", mono=True)
	cmd = m.command
	try:
		if app.long(m) < 4096 and app.long(m) > 2:
			data = m.text.split(None, 2)[2]
			givename = cmd[1]
			await app.create_file(
				m, 
				filename=givename, 
				text=data
			)
		# if replied to text without file name
		elif app.long(m) == 1 and reply:
			data = reply.text
			await app.create_file(
				m, 
				filename="file.py", 
				text=data
			)
		# if replied to text with file name
		elif app.long(m) > 1 and reply:
			givename = cmd[1]
			data = reply.text
			await app.create_file(
				m, 
				filename=givename, 
				text=data
			)
		else:
			await app.send_edit(m, f"Use cmd correctly: `{app.PREFIX}new [ file name ] [content]`\n\nNote: use filename with extention, ex: file.py, file.txt, etc",)
	except Exception as e:
		await app.error(m, e)




