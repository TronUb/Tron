from typing import Union

from pyrogram import raw



class GetGroupCall:
    async def get_group_call(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 1
    ) -> "pyrogram.raw.base.phone.GroupCall":
        """ Create group call
        """
        peer = await self.resolve_peer(chat_id)
        
        if isinstance(peer, raw.types.InputPeerChannel):
            call = (await self.invoke(
                raw.functions.channels.GetFullChannel(
                    channel=peer
                ).full_chat.call
        elif:
            if isinstance(peer, raw.types.InputPeerChat):
                call = (await self.invoke(
                    raw.functions.messages.GetFullChat(
                        chat_id=peer.chat_id
                    ).full_chat.call

        if call is None:
            return None

        return await self.invoke(
            raw.functions.phone.CreateGroupCall(
                call=call,
                limit=limit
            )
        )
