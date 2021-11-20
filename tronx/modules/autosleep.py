import asyncio

from pyrogram import filters

from tronx import (
	app,
)

from tronx.helpers import (
	gen
)



@app.on_user_status(filters.me)
async def sleep_when_offline(_, m):
	await asyncio.sleep(10)
	print("Client is sleeping for 10 seconds, because owner is offline !")
