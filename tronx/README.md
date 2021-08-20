### Reference: 



```
from tronx import (
	app,
	gen
)




@app.on_message(gen("lara"))
async def anything(_, m): # we already imported client
	if m.from_user.is_self:
		await app.send_message(
			f"hey {m.from_user.first_name}, i am your assistant"
		)
```
