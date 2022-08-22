from typing import Union, Optional
from datetime import datetime

from pyrogram import raw



class EditGroupCallParticipant:
    async def edit_group_call_participant(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        user_id: Union[int, str],
        muted: Optional[bool] = None,
        volume: Optional[int] = None,
        raise_hand: Optional[bool] = None,
        video_stopped: Optional[bool] = None,
        video_paused: Optional[bool] = None,
        presentation_paused: Optional[bool] = None
    ) -> "pyrogram.raw.base.Updates":
        """ Join group call
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call

        peer = await self.resolve_peer(user_id)

        return await self.invoke(
            raw.functions.phone.EditGroupCallParticipant(
                call=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                ),
                participant=peer,
                muted=muted,
                volume=volume,
                raise_hand=raise_hand,
                video_stopped=video_stopped,
                video_paused=video_paused,
                presentation_paused=presentation_paused
            )
        )
 
