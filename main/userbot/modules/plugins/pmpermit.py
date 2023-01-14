""" A security system which keeps spammers away """

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from pyrogram.errors import (
    PeerIdInvalid,
    UsernameNotOccupied,
    UsernameInvalid
)

from main import app, gen
from main.core.enums import UserType



async def old_msg(m: Message, user_id):
    """ Delete warn messages """
    if bool(app.get_msgid(user_id)) is True:
        old_msgs = app.get_msgid(user_id)
        await app.delete_messages(
            chat_id=m.chat.id,
            message_ids=old_msgs
        )
        return True
    return False




async def send_warn(m: Message, user):
    """ Send warning messages """
    pic = app.PmpermitPic
    text = app.PmpermitText

    if pic:
        msg = await app.send_photo(
            m.chat.id,
            pic,
            caption=text
        )
        app.set_msgid(user, msg.id)
        return True
    elif not pic:
        msg = await app.send_message(
            m.chat.id,
            text,
            disable_web_page_preview=True
            )
        app.set_msgid(user, msg.id)
        return True
    else:
        return print("The bot didn't send pmpermit warning message.")






# incoming autoblock
@app.on_message(filters.private & filters.incoming & (~filters.bot & ~filters.me), group=-1)
async def pmpermit_handler(_, m: Message):
    """ pmpermit handler for pmpermit plugin """
    try:
        users = []
        is_user = False
        pmlimit = app.PmpermitLimit

        if bool(app.Pmpermit) is False or m.chat.is_verified: # exclude verified accounts
            return

        if bool(app.get_whitelist(m.chat.id)) is True:
            return
        else:
            # this will reduce the use of pyrogram's get_users method
            if bool(users):
                for x in users:
                    if x.get(m.chat.id):
                        is_user = True
                        break

            if is_user:
                user = users.get(m.chat.id)
            else:
                user = await app.get_users(m.chat.id)
                users.append({m.chat.id : user}) # whole object


        # log user info to log chat

        msg = "#pmpermit\n\n"
        msg += f"Name: `{user.first_name}`\n"
        msg += f"Id: `{user.id}`\n"
        msg += f"Username: `@{user.username}`\n" if user.username else "Username: `None`\n"
        msg += f"Message: `{m.text or m.caption}`\n"

        warns = bool(app.get_warn(user.id))

        if warns is False:
            app.set_warn(user.id, 1)
            await send_warn(m, user.id)

        elif warns is True:
            warn = int(app.get_warn(user.id))
            if warn < pmlimit:
                new_warn = warn + 1
                app.set_warn(user.id, new_warn)
                await old_msg(m, user.id) # delete old warns
                await send_warn(m, user.id) # send new warns
            elif warn >= pmlimit:
                done = await app.block_user(user.id)
                if done:
                    try:
                        await app.send_message(
                            app.LOG_CHAT,
                            f"{user.mention} is now blocked for spamming !"
                        )
                    except PeerIdInvalid:
                        print(f"{user.first_name} was blocked in your pm for some reason.")
                else:
                    await app.send_edit(
                        f"Failed to block {user.mention} because through pmpermit.",
                        text_type=["mono"],
                        delme=4
                    )
            else:
                print("Something went wrong in pmpermit")
    except Exception as e:
        await app.error(e)




@app.on_cmd(
    commands=["a", "approve"],
    usage="Approve a user to dm you.",
    disable_for=UserType.SUDO
)
async def approve_handler(_, m: Message):
    """ approve handler for pmpermit plugin """
    if m.chat.type == ChatType.BOT:
        return await app.send_edit(
            "No need to approve innocent bots !",
            text_type=["mono"],
            delme=4
        )

    reply = m.reply_to_message
    cmd = m.command
    user_data = False

    if m.chat.type == ChatType.PRIVATE:
        user_id = m.chat.id

    elif m.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        if reply:
            user_id = reply.from_user.id

        elif not reply and app.long() == 1:
            return await app.send_edit("Whom should i approve, piro ?", text_type=["mono"], delme=4)

        elif not reply and app.long() > 1:
            try:
                user_data = await app.get_users(cmd[1])
                user_id = user_data.id
            except PeerIdInvalid:
                return await app.send_edit(
                    "You have to pass username instead of user id.",
                    text_type=["mono"],
                    delme=4
                )
            except UsernameNotOccupied:
                return await app.send_edit(
                    "This user doesn't exists in telegram.",
                    text_type=["mono"],
                    delme=4
                )
            except UsernameInvalid:
                return await app.send_edit(
                    "The username | user id is invalid.",
                    text_type=["mono"],
                    delme=4
                )

        else:
            return await app.send_edit("Something went wrong.", text_type=["mono"], delme=4)
    if user_data:
        info = user_data
    else:
        info = await app.get_users(user_id)

    try:
        m = await app.send_edit(f"`Approving` {info.mention} `. . .`")
        app.set_whitelist(user_id, True)
        await app.send_edit(f"{info.mention} `is now approved.`", delme=4)
        app.del_warn(user_id)

        if app.get_msgid(user_id):
            await old_msg(m, user_id)

    except Exception as e:
        await app.send_edit("Something went wrong.", text_type=["mono"], delme=4)
        await app.error(e)




@app.on_cmd(
    commands=["da", "disapprove"],
    usage="Disapprove a user from sending message to you.",
    disable_for=UserType.SUDO
)
async def diapprove_handler(_, m:Message):
    """ disapprove handler for pmpermit plugin """
    if m.chat.type == ChatType.BOT:
        return await app.send_edit(
            "No need to approve innocent bots !",
            text_type=["mono"],
            delme=4
        )

    reply = m.reply_to_message
    cmd = m.command
    user_data = False

    if m.chat.type == ChatType.PRIVATE:
        user_id = m.chat.id

    elif m.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        if reply:
            user_id = reply.from_user.id

        elif not reply and app.long() == 1:
            return await app.send_edit(
                "Whom should i disapprove, piro ?",
                text_type=["mono"],
                delme=4
            )

        elif not reply and app.long() > 1:
            try:
                user_data = await app.get_users(cmd[1])
                user_id = user_data.id
            except PeerIdInvalid:
                return await app.send_edit(
                    "Pass username instead of user id.",
                    text_type=["mono"],
                    delme=4
                )
            except UsernameNotOccupied:
                return await app.send_edit(
                    "This user doesn't exists in telegram.",
                    text_type=["mono"],
                    delme=4
                )
            except UsernameInvalid:
                return await app.send_edit(
                    "The username | user id is invalid.",
                    text_type=["mono"],
                    delme=4
                )
        else:
            return await app.send_edit("Failed to disapprove user !", text_type=["mono"], delme=4)
    if user_data:
        info = user_data
    else:
        info = await app.get_users(user_id)

    if info:
        await app.send_edit(f"`Disapproving` {info.mention} `. . .`")
        app.del_whitelist(user_id)
        await app.send_edit(f"{info.mention} `has been disapproved for pm.`", delme=4)
        try:
            await app.send_message(
                app.LOG_CHAT,
                f"#disapprove\n\n{info.mention} `has been disapproved.`"
            )
        except PeerIdInvalid:
            print(f"{info.first_name} has been disapproved.")
    else:
        return await app.send_edit(
            "Sorry there is no user id to disapprove.",
            text_type=["mono"],
            delme=4
        )
