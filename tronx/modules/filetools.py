import os
import shutil
import time
import asyncio
import zipfile
import sys
from pathlib import Path

from pyrogram.types import Message
from pyrogram import filters, Client

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX,
	USER_NAME, 
	USER_ID,
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
	delete,
	long,
	types,
	mymention,
	create_file,
)





CMD_HELP.update(
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
	extract_path = f"tronx/downloads/{foldername}"
	shutil.unpack_archive(zippath, extract_path)
	return extract_path



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.on_message(gen("zip"))
async def zipit(_, m: Message):
	reply = m.reply_to_message
	if not reply:
		return await send_edit(m, f"Reply to some media file . . .", mono=True, delme=2)

	elif reply:
		if reply.text:
			return await send_edit(m, "Reply to some media not text . . .", mono=True)
		await send_edit(m, "Zipping . . .", mono=True)

		if Config.TEMP_DICT:
			loc = Config.TEMP_DICT
		else:
			loc = "tronx/downloads"
		dl = await app.download_media(
			reply,
			block=False
		)
		zipfile.ZipFile(dl.replace("/app/downloads/", "") + ".zip", "w").write(dl)
		place = dl.replace("/app/downloads/", "") + ".zip"
		await send_edit(m, f"**Your file is compressed and saved here:** \n`{place}`")
	else:
		await send_edit(m, "Something went wrong . . .", delme=2, mono=True)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.on_message(gen("unzip"))
async def unzipit(_, m: Message):
	if long(m) == 2:
		if long(m) <= 4096:
			loc = m.text.split(None, 1)[1]
			await send_edit(m, "Unzipping file . . .")
			extract_path = await unzipfiles(loc)
			await send_edit(m, f"File unzipped and saved here: `{extract_path}`")
			return
		else:
			await send_edit(m, "The path length exceeds 4096 character, please check again ...", delme=2, mono=True)
	else:
		await send_edit(m, "Give me the file path to unzip the file ...", delme=2, mono=True)





@app.on_message(gen("new"))
async def create_anyfile(app, m:Message):
	reply = m.reply_to_message
	await send_edit(m, "making file ...")
	cmd = m.command
	try:
		if long(m) < 4096 and long(m) > 2:
			data = m.text.split(None, 2)[2]
			givename = cmd[1]
			await create_file(
				m, 
				filename=givename, 
				text=data
			)
		# if replied to text without file name
		elif long(m) == 1 and reply:
			data = reply.text
			await create_file(
				m, 
				filename="file.py", 
				text=data
			)
		# if replied to text with file name
		elif long(m) > 1 and reply:
			givename = cmd[1]
			data = reply.text
			await create_file(
				m, 
				filename=givename, 
				text=data
			)
		else:
			await send_edit(
				m, 
				f"Use cmd correctly: `{PREFIX}new [ file name ] [content]`\n\nNote: use filename with extention, ex: file.py, file.txt, etc",
				)
	except Exception as e:
		await error(m, e)



