import os
import shutil
import zipfile
from pathlib import Path

from pyrogram.types import Message
from pyrogram import filters

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
)




CMD_HELP.update(
	{"zip" : (
		"zip",
		{
		"zip [reply to file]" : "Zip a file and save it in your local directories.",
		"unzip [file path]" : "Unzip a file and save it in your local directories."
		}
		)
	}
)




#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def zipdir(dirName):
	dice = []
	for root, directories, files in os.walk(dirName):
		for filename in files:
			filePath = os.path.join(root, filename)
			dice.append(filePath)
	return filePaths


async def unzipfiles(zippath):
	foldername = zippath.split("/")[-1]
	extract_path = f"tronx/cache/unzip/{foldername}"
	shutil.unpack_archive(zippath, extract_path)
	return extract_path



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.on_message(gen("zip"))
async def zipit(c: app, m: Message):
	if not m.reply_to_message:
		await send_edit(
			m, 
			f"Reply to some media file ..."
			)
		return
	elif m.reply_to_message:
		doc = m.reply_to_message
		if doc.document:
			name = doc.document.file_name
		elif doc.photo:
			name = doc.photo.file_name
		elif doc.video:
			name = doc.video.file_name
		elif doc.sticker:
			name = doc.sticker.file_name
		elif doc.animation:
			name = doc.animation.file_name
		else:
			await send_edit(
				m, 
				"The file does not have a name, please give a name after command ..."
				)
			return
		if m.reply_to_message:
			if not os.path.isdir(Config.TEMP_DICT):
				os.makedirs("tronx/downloads/")
			dl = await app.download_media(
				doc,
				Config.TEMP_DICT + name)
			zipfile.ZipFile(dl + ".zip", "w", zipfile.ZIP_DEFLATED).write(
				dl
				)
			tron = dl + ".zip"
			await send_edit(
				m, 
				f"Your file is compressed and saved here: \n`{tron}`"
				)
			return
		else:
			await send_edit(
				m, 
				f"Reply to a file and give a name after cmd. \nEx: `{PREFIX}.zip myfile`"
				)
	else:
		await send_edit(
			m, 
			"Reply to some media please ...")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.on_message(gen("unzip"))
async def unzipit(c: app, m: Message):
	if len(m.command) == 2:
		if len(m.command) <= 4096:
			loc = m.text.split(None, 1)[1]
			await send_edit(
				m, 
				"__Unzipping file...__"
				)
			extract_path = await unzipfiles(loc)
			await send_edit(
				m, 
				f"File unzipped and saved here: `{extract_path}`"
				)
			return
		else:
			await send_edit(
				m, 
				"The path length exceeds 4096 character, please check again ..."
				)
			time.sleep(2.5)
			await m.delete()
	else:
		await send_edit(
			m, 
			"Give me the file path to unzip the file ..."
			)
		time.sleep(2.5)
		await m.delete()
