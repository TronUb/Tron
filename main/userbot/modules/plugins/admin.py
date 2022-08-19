# pylint: disable=W0707, W0703, W0622, C0103, E0401, E0611, E1123

""" admin module """

from datetime import datetime, timedelta

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    Message,
    ChatPermissions,
    ChatPrivileges
)

from pyrogram.errors import (
    UsernameInvalid,
    UserNotParticipant,
    UsernameNotOccupied,
)

from main import app, gen




app.CMD_HELP.update(
    {"admin" : (
        "admin",
        {
        "ban [username | id | reply] [time]" : "bans a user, use it as timeban too",
        "banall [confirm]" : "Ban all members in chat by one command",
        "unban" : "unbans a user",
        "mute [username | id | reply] [time]" : "restricts a user from talking in groups",
        "unmute" : "unrestricts a user from talking in groups",
        "promote" : "promote a member to admin",
        "demote" : "demote a admin to a member",
        "pin" : "pin a message in group",
        "kick" : "kick a user out of your groups.",
        "unpin" : "unpin a pinned message.",
        "unpin all" : "unpin all pinned messages in one command"
        }
        )
    }
)



private = ("private", "bot")
def to_seconds(format, number): # number: int, format: s, m, h, d
    """ from hour/minutes/days to seconds converter """
    format_set = {"s": number, "m": number*60, "h": number*60*60, "d": number*60*60*24}
    return int(format_set[format])




@app.on_message(
    gen(
        commands="ban",
        exclude=["sudo", "channel"]
    )
)
async def ban_handler(_, m: Message):
    """
        name::
            ban_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        if await app.check_private():
            return

        reply = m.reply_to_message
        user = False
        cmd = m.command
        ban_time = False

        if app.long() == 1 and not reply:
            return await app.send_edit(
                "Reply or give some id | username after command.",
                text_type=["mono"],
                delme=4
            )

        if await app.IsAdmin("ban_users") is False:
            return await app.send_edit(
                "You're not an admin here or you don't have enough admin rights.",
                text_type=["mono"],
                delme=4
            )

        if reply:
            user = await app.get_chat_member(m.chat.id, reply.from_user.id)
            if app.long() > 1:
                arg = cmd[1]
                ban_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))

        elif not reply:
            if app.long() > 1:
                user = await app.get_chat_member(m.chat.id, cmd[1])
                if app.long() > 2:
                    arg = cmd[2]
                    ban_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))

        if user:
            if user.user.is_self:
                return await app.send_edit("You can't ban yourself !", text_type=["mono"], delme=4)
            elif user.status == "administrator":
                return await app.send_edit(
                    "How am i supposed to ban an admin ?",
                    text_type=["mono"],
                    delme=4
                )
            elif user.status == "creator":
                return await app.send_edit(
                    "How am i supposed to ban a creator of a group ?",
                    text_type=["mono"],
                    delme=4
                )
        else:
            return await app.send_edit("Something went wrong !", text_type=["mono"], delme=4)

        await app.send_edit("⏳ • Hold on . . .", text_type=["mono"])
        if ban_time:
            await app.ban_chat_member(m.chat.id, user.user.id, datetime.now() + timedelta(ban_time))
            await app.send_edit(f"Banned {user.user.mention} for {arg}", delme=4)
        else:
            await app.ban_chat_member(m.chat.id, user.user.id)
            await app.send_edit(f"Banned {user.user.mention} in this chat.", delme=4)

    except (UsernameInvalid, UsernameNotOccupied):
        await app.send_edit("The provided username | id is invalid !", text_type=["mono"], delme=4)
    except UserNotParticipant:
        await app.send_edit("This user doesn't exist in this group !", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)




@app.on_message(gen("banall", exclude = ["sudo", "channel"]))
async def banall_handler(_, m: Message):
    """
        name::
            banall_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        if await app.check_private():
            return

        if await app.IsAdmin("ban_users") is False:
            return await app.send_edit(
                "You're not an admin or you don't have enough admin rights.",
                text_type=["mono"],
                delme=3
            )

        count = 0
        data = []
        data.clear()

        if app.long() == 1:
            return await app.send_edit(
                "Use '`confirm`' text after command to ban all members.",
                text_type=["mono"],
                delme=4
            )

        elif app.long() > 1 and m.command[1] == "confirm":
            async for x in app.get_chat_members(m.chat.id):
                if x.status == ChatMemberStatus.MEMBER:
                    await app.ban_chat_member(m.chat.id, x.user.id)
                    count += 1
                    await app.send_edit(f"Banned {x.user.mention} . . .")
            await app.send_edit(f"Banned {count} members !")
        elif app.long() > 1 and m.command[1] != "confirm":
            await app.send_edit(
                "Use '`confirm`' text after command to ban all members.",
                text_type=["mono"],
                delme=4
            )

    except Exception as e:
        await app.error(e)




@app.on_message(
    gen(
        commands="unban",
        exclude=["sudo", "channel"]
    )
)
async def unban_handler(_, m: Message):
    """
        name::
            unban_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        if await app.check_private():
            return

        reply = m.reply_to_message
        user = False

        if not reply and app.long() == 1:
            return await app.send_edit(
                "Reply to a user or give me the username | id of that user.",
                text_type=["mono"],
                delme=4
            )

        if await app.IsAdmin("ban_users") is False:
            return await app.send_edit(
                "You're not an admin or you don't have enough admin rights.",
                text_type=["mono"],
                delme=4
            )

        if reply:
            user = await app.get_chat_member(m.chat.id, reply.from_user.id)
        elif not reply:
            if app.long() > 1:
                user = await app.get_chat_member(m.chat.id, m.command[1])
        else:
            return await app.send_edit("Something went wrong !", text_type=["mono"], delme=4)

        if user:
            if user.user.is_self:
                return await app.send_edit(
                    "You can't unban yourself !",
                    text_type=["mono"],
                    delme=4
                )
            elif user.status == "administrator":
                return await app.send_edit(
                    "How am i supposed to unban an admin ?",
                    text_type=["mono"],
                    delme=4
                )
            elif user.status == "creator":
                return await app.send_edit(
                    "How am i supposed to unban a creator of a group ?",
                    text_type=["mono"],
                    delme=4
                )
        else:
            return await app.send_edit("Something went wrong !", text_type=["mono"], delme=4)

        await app.send_edit("Unbanning . . .", text_type=["mono"])
        done = await app.unban_chat_member(m.chat.id, user.user.id)
        if done:
            await app.send_edit(f"Unbanned {user.user.mention} in this chat.", delme=4)
        else:
            await app.send_edit("Failed to unabn this user.", text_type=["mono"], delme=4)

    except (UsernameInvalid, UsernameNotOccupied):
        await app.send_edit(
            "The provided username | id is invalid !",
            text_type=["mono"],
            delme=4
        )
    except UserNotParticipant:
        await app.send_edit(
            "This user doesn't exist in this group !",
            text_type=["mono"],
            delme=4
        )
    except Exception as e:
        await app.error(e)




async def mute_user(chat_id, user_id, duration=datetime.now()):
    """ mute function to admin plugin """
    return await app.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_send_polls=False,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=False
            ),
            until_date=duration
        )





@app.on_message(
    gen(
        commands="mute",
        exclude=["sudo"]
    )
)
async def mute_handler(_, m: Message):
    """
        name::
            mute_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        if await app.check_private():
            return

        reply = m.reply_to_message
        user = False
        mute_time = False
        cmd = m.command

        if not reply and app.long() == 1:
            return await app.send_edit(
                "Reply to a user or give me username | id of that user.",
                text_type=["mono"],
                delme=4
            )

        if await app.IsAdmin("ban_users") is False:
            return await app.send_edit(
                "You're not an admin or you don't have enough admin rights.",
                text_type=["mono"],
                delme=4
            )

        if reply:
            user = await app.get_chat_member(m.chat.id, reply.from_user.id)
            if app.long() > 1:
                arg = cmd[1]
                mute_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))

        elif not reply:
            if app.long() > 1:
                user = await app.get_chat_member(m.chat.id, m.command[1])
                if app.long() > 2:
                    arg = cmd[2]
                    mute_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))
        else:
            return await app.send_edit("Something went wrong !", text_type=["mono"], delme=4)

        if user:
            if user.user.is_self:
                return await app.send_edit("You can't mute yourself !", text_type=["mono"], delme=4)
            elif user.status == "administrator":
                return await app.send_edit(
                    "How am i supposed to mute an admin ?",
                    text_type=["mono"],
                    delme=4
                )
            elif user.status == "creator":
                return await app.send_edit(
                    "How am i supposed to mute a creator of a group ?",
                    text_type=["mono"],
                    delme=4
                )
        else:
            return await app.send_edit("Something went wrong !", text_type=["mono"], delme=4)

        if mute_time:
            await mute_user(m.chat.id, user.user.id, datetime.now() + timedelta(mute_time))
            await app.send_edit(f"Muted {user.user.mention} for {arg}")
        else:
            await mute_user(m.chat.id, user.user.id)
            await app.send_edit(f"Muted {user.user.mention} in this chat for forever.", delme=4)

    except (UsernameInvalid, UsernameNotOccupied):
        await app.send_edit("The provided username | id is invalid !", text_type=["mono"], delme=4)
    except UserNotParticipant:
        await app.send_edit("This user doesn't exist in this group !", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)




@app.on_message(
    gen(
        commands="unmute",
        exclude=["sudo"]
    )
)
async def unmute_handler(_, m: Message):
    """
        name::
            unmute_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        if await app.check_private():
            return

        reply = m.reply_to_message
        user = False

        if not reply and app.long() == 1:
            return await app.send_edit(
                "Reply to a user or give me the username | id of that user.",
                text_type=["mono"],
                delme=4
            )

        if await app.IsAdmin("ban_users") is False:
            return await app.send_edit(
                "You're not an admin or you don't have enough admin rights.",
                text_type=["mono"],
                delme=4
            )

        if reply:
            user = await app.get_chat_member(m.chat.id, reply.from_user.id)
        elif not reply:
            if app.long() > 1:
                user = await app.get_chat_member(m.chat.id, m.command[1])
        else:
            return await app.send_edit("Something went wrong !", text_type=["mono"], delme=4)

        if user:
            if user.user.is_self:
                return await app.send_edit(
                    "You can't unmute yourself !",
                    text_type=["mono"],
                    delme=4
                )
            elif user.status == "administrator":
                return await app.send_edit(
                    "How do i unmute an admin ?",
                    text_type=["mono"],
                    delme=4
                )
            elif user.status == "creator":
                return await app.send_edit(
                    "How do i unmute a creator ?",
                    text_type=["mono"],
                    delme=4
                )
        else:
            return await app.send_edit("Something went wrong !", text_type=["mono"], delme=4)

        await app.restrict_chat_member(
            m.chat.id,
            user.user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False
            )
        )
        await app.send_edit(f"Unmuted {user.user.mention} in this chat.", delme=4)

    except (UsernameInvalid, UsernameNotOccupied):
        await app.send_edit("The provided username | id is invalid !", text_type=["mono"], delme=4)
    except UserNotParticipant:
        await app.send_edit("This user doesn't exist in this group !", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)




@app.on_message(
    gen(
        commands="kick",
        exclude=["sudo", "channel"]
    )
)
async def kick_handler(_, m: Message):
    """
        name::
            kick_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        if await app.check_private():
            return

        reply = m.reply_to_message
        user = False

        if not reply and app.long() == 1:
            return await app.send_edit(
                "Reply to a user or give me username | id of that user.",
                text_type=["mono"],
                delme=4
            )

        if await app.IsAdmin("ban_users") is False:
            return await app.send_edit(
                "You're not admin or you don't have enough admin rights.",
                text_type=["mono"],
                delme=4
            )

        if reply:
            user = await app.get_chat_member(m.chat.id, reply.from_user.id)
        else:
            if app.long() > 1:
                user = await app.get_chat_member(m.chat.id, m.command[1])

        if user:
            if user.user.is_self:
                return await app.send_edit("You can't kick yourself !", text_type=["mono"])
            elif user.status == "administrator":
                return await app.send_edit(
                    "How am i supposed to kick an admin ?",
                    text_type=["mono"]
                )
            elif user.status == "creator":
                return await app.send_edit(
                    "How am i supposed to kick a creator of a group ?",
                    text_type=["mono"]
                )
        else:
            return await app.send_edit("Something went wrong.", text_type=["mono"], delme=4)

        await app.send_edit("Kicking . . .", text_type=["mono"])
        done = await app.kick_user(m.chat.id, user.user.id)
        if done:
            await app.send_edit(f"Kicked {user.user.mention} in this chat.", delme=4)
        else:
            await app.send_edit("Failed to kick to user.", text_type=["mono"], delme=4)

    except (UsernameInvalid, UsernameNotOccupied):
        await app.send_edit("The provided username | id is invalid !", text_type=["mono"], delme=4)
    except UserNotParticipant:
        await app.send_edit("This user doesn't exist in this group !", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)




@app.on_message(
    gen(
        commands="pin",
        exclude=["sudo", "channel"]
    )
)
async def pin_handler(_, m: Message):
    """
        name::
            pin_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        arg = True
        cmd = m.command
        reply = m.reply_to_message

        if app.long() > 1:
            arg = False if cmd[1] == "loud" else True

        if m.chat.type in private:
            if not reply:
                return await app.send_edit(
                    "Reply to some message, so that i can pin that message.",
                    text_type=["mono"],
                    delme=4
                )

            done = await reply.pin(disable_notification=arg)
            if done:
                return await app.send_edit("Pinned message !", text_type=["mono"], delme=4)
            else:
                return await app.send_edit("Failed to pin message.", text_type=["mono"], delme=4)

        if await app.IsAdmin("pin_messages") is False:
            return await app.send_edit(
                "You're not an admin here or you don't have enough admin rights.",
                text_type=["mono"],
                delme=4
            )

        if reply:
            await app.send_edit("⏳ • Hold on . . .", text_type=["mono"])
            done = await reply.pin(disable_notification=arg)
            if done:
                await app.send_edit("Pinned message.", text_type=["mono"], delme=4)
            else:
                await app.send_edit("Failed to pin message.", text_type=["mono"], delme=4)
        else:
            await app.send_edit(
                "Reply to a message so that I can pin that message.",
                text_type=["mono"],
                delme=4
            )

    except Exception as e:
        await app.error(e)




@app.on_message(
    gen(
        commands="unpin",
        exclude=["sudo", "channel"]
    )
)
async def unpin_handler(_, m: Message):
    """
        name::
            unpin_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        cmd = m.command
        reply = m.reply_to_message

        if not reply and app.long() == 1:
            return await app.send_edit(
                "Reply to a message or use `all` as a prefix to unpin all pinned message.",
                text_type=["mono"],
                delme=4
            )

        if reply:
            m = await app.send_edit("⏳ • Hold on . . .", text_type=["mono"])
            done = await reply.unpin()
            if done:
                await app.send_edit("Unpinned message.", text_type=["mono"])
            else:
                await app.send_edit("Failed to unpin message.", text_type=["mono"], delme=4)
        elif not reply and app.long() > 1:
            if cmd[1] == "all":
                done = await app.unpin_all_chat_messages(m.chat.id)
                if done:
                    await app.send_edit("Unpinned all pinned messages . . .", text_type=["mono"])
                else:
                    await app.send_edit(
                        "Failed to unpin all messages.",
                        text_type=["mono"],
                        delme=4
                    )
            elif cmd[1] != "all":
                await app.send_edit(
                    "Reply or use `all` to unpin all pinned messages.",
                    text_type=["mono"],
                    delme=4
                )
            else:
                await app.send_edit("Failed to unpin all messages.", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)




@app.on_message(
    gen(
        commands="promote",
        exclude=["sudo", "channel"]
    )
)
async def promote_handler(_, m: Message):
    """
        name::
            promote_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        if await app.check_private():
            return

        reply = m.reply_to_message
        user = False

        if app.long() == 1 and not reply:
            return await app.send_edit(
                "Reply to user or give me username | id of that user.",
                text_type=["mono"],
                delme=4
            )

        if await app.IsAdmin("add_admins") is False:
            return await app.send_edit(
                "You're not admin or you don't have enough admin rights.",
                text_type=["mono"],
                delme=4
            )

        if reply:
            user = await app.get_chat_member(m.chat.id, reply.from_user.id)
        else:
            if app.long() > 1:
                user = await app.get_chat_member(m.chat.id, m.command[1])

        if user:
            if user.user.is_self:
                return await app.send_edit("You can't promote yourself !", text_type=["mono"])
            elif user.status == "administrator":
                return await app.send_edit(
                    "How am i supposed to promote already promoted user ?",
                    text_type=["mono"]
                    )
            elif user.status == "creator":
                return await app.send_edit(
                    "How am i supposed to promote a creator of a group ? wth ?",
                    text_type=["mono"]
                )
        else:
            return await app.send_edit("Something went wrong !", text_type=["mono"])

        await app.promote_chat_member(
            m.chat.id,
            user.user.id,
            privileges=ChatPrivileges(
            can_change_info=True,
            can_manage_video_chats=True,
            can_manage_chat=True,
            can_delete_messages=True,
            can_edit_messages=True,
            can_invite_users=True,
            can_promote_members=False,
            can_restrict_members=True,
            can_pin_messages=True,
            can_post_messages=True
            )
        )
        app.send_edit("Promoting . . .", text_type=["mono"])
        await app.send_edit(f"Promoted {user.user.mention} in this chat !")

    except (UsernameInvalid, UsernameNotOccupied):
        await app.send_edit("The provided username | id is invalid !", text_type=["mono"], delme=4)
    except UserNotParticipant:
        await app.send_edit("This user doesn't exist in this group !", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)




@app.on_message(
    gen(
        commands="demote",
        exclude=["sudo", "channel"]
    )
)
async def demote_handler(_, m: Message):
    """
        name::
            demote_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        if await app.check_private():
            return

        reply = m.reply_to_message
        user = False

        if await app.IsAdmin("add_admins") is False:
            return await app.send_edit(
                "You're not an admin here or you don't have enough rights.",
                text_type=["mono"],
                delme=4
            )

        if app.long() == 1 and not reply:
            return await app.send_edit(
                "Reply to user or give me username | id of that user.",
                text_type=["mono"],
                delme=4
            )

        if reply:
            user = await app.get_chat_member(m.chat.id, reply.from_user.id)
        else:
            if app.long() > 1:
                user = await app.get_chat_member(m.chat.id, m.command[1])

        if user:
            if user.user.is_self:
                return await app.send_edit("You can't demote yourself !", text_type=["mono"])
            elif user.status == "creator":
                return await app.send_edit(
                    "How am i supposed to demote a creator of a group ?",
                    text_type=["mono"]
                )
        else:
            return await app.send_edit("Something went wrong !", text_type=["mono"])

        await app.promote_chat_member(
                m.chat.id,
                user.user.id,
                privileges=ChatPrivileges(
                can_change_info=False,
                can_manage_video_chats=False,
                can_manage_chat=False,
                can_delete_messages=False,
                can_edit_messages=False,
                can_invite_users=False,
                can_promote_members=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_post_messages=False
                )
        )
        await app.send_edit("Demoting . . .", text_type=["mono"])
        await app.send_edit(f"Demoted {user.user.mention} in this chat !")

    except (UsernameInvalid, UsernameNotOccupied):
        await app.send_edit("The provided username | id is invalid !", text_type=["mono"], delme=4)
    except UserNotParticipant:
        await app.send_edit("This user doesn't exist in this group !", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)
