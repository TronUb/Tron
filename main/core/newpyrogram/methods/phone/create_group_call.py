from typing import Union, Optional
from datetime import datetime

from pyrogram import raw



class CreateGroupCall:
    async def create_group_call(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        rtmp_stream: bool = False,
        title: Optional[str] = None,
        schedule_date: datetime = None
    ) -> "pyrogram.raw.base.Updates":
        """ Create group call
        """
        peer = await self.resolve_peer(chat_id)

        return await self.invoke(
            raw.functions.phone.CreateGroupCall(
                peer=peer,
                random_id=message_id,
                rtmp_stream=rtmp_stream,
                title=title,
                schedule_date=schedule_date
            )
        )
