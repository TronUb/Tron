from typing import Union

from pyrogram import raw



class LeaveGroupCall:
    async def leave_group_call(
        self: "pyrogram.Client",
        chat_id: Union[int, str]
    ) -> "pyrogram.raw.base.Updates":
        """ Leave group call
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call
        participants = group_call.participants
        source = None

        for user in participants:
            if user and user.is_self:
                source = user.source

        if source is None:
            return None

        return await self.invoke(
            raw.functions.phone.LeaveGroupCall(
                call=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                ),
                source=source
            )
        )
