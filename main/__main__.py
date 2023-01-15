"""
Run after main.__init__.py, this file mainly installs plugins
for both assistant & userbot and starts their clients.
"""

import asyncio
from main.userbot import app




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.start_bot())
