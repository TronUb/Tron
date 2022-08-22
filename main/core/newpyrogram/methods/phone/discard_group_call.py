from typing import Union

from pyrogram import raw



class DiscardGroupCall:
    async def discard_group_call(
        self: "pyrogram.Client",
        chat_id: Union[int, str]
    ) -> "pyrogram.raw.base.Updates":
        """ Discard group call
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call

        return await self.invoke(
            raw.functions.phone.DiscardGroupCall(
                call=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                )
            )
        )
