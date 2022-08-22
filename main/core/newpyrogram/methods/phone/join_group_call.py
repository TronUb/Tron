from typing import Union, Optional
from datetime import datetime

from pyrogram import raw



class JoinGroupCall:
    async def join_group_call(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        muted: Optional[bool] = None,
        video_stopped: Optional[bool] = None,
        invite_hash: Optional[str] = None,
    ) -> "pyrogram.raw.base.Updates":
        """ Join group call
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call

        return await self.invoke(
            raw.functions.phone.JoinGroupCall(
                call=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                ),
                join_as=raw.types.InputUserSelf(),
                params=await self.invoke(
                    raw.functions.phone.GetCallConfig()
                ),
                muted=muted,
                video_stopped=video_stopped,
                invite_hash=invite_hash
            )
        )
