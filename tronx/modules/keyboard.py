from pyrogram.types import (
	InlineKeyboardMarkup, 
	InlineKeyboardButton,
)

from tronx import (
	app,
	bot,
)

from tronx.helpers import (
	gen,
	error,
	long,
	send_edit,
)




@app.on_message(gen("kbd"))
async def create_keyboard(_, m):
	if long(m) >= 3:
		await bot.send_message(
			m.chat.id, 
			m.text.split()[3],
        		reply_markup=InlineKeyboardMarkup(
				[
					[
                    			InlineKeyboardButton( 
						m.command[1],
						url=m.command[2]
					),
					],
				]
				)
			)
	else:
		await send_edit(m, f"`{PREFIX}kbd [ Button text ] [ Button url ] [ Text ]`")
