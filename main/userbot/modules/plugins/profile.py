""" profile plugin """

import time
import asyncio

from functools import partial

from pyrogram.types import (
    Message,
    User
    )

from pyrogram.errors import PeerIdInvalid

from main import app, gen
from main.core.enums import UserType


date_dict = []


men = partial("<a href='tg://user?id={}'>{}</a>".format)


infotext = """
**NAME:** `{}`
**USER ID:** `{}`
**Mention:** [{}](tg://user?id={})
**USERNAME:** {}
**DC ID:** `{}`
"""


def FullName(user: User):
    """ fullname function for profile plugin """
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@app.on_cmd(
    commands="whois",
    usage="Get user information."
)
async def whois_handler(_, m: Message):
    """ whois handler for profile plugin """
    reply = m.reply_to_message
    cmd = m.command
    await app.send_edit("Finding details . . .", text_type=["mono"])

    if reply:
        get_user = reply.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
    else:
        get_user = None

    if not get_user:
        return await app.send_edit(
            "Please reply to a user or provide a user ID.", text_type=["mono"], delme=3
        )

    try:
        user = await app.get_users(get_user)
    except PeerIdInvalid:
        return await app.send_edit("I don't know that User.", text_type=["mono"], delme=3)

    pfp = None
    async for x in app.get_chat_photos(user.id, limit=1):
        pfp = x.file_id
        break

    info_text = (
        f"**Full Name:** {user.first_name} {user.last_name or ''}\n"
        f"**User ID:** `{user.id}`\n"
        f"**Username:** @{user.username if user.username else 'N/A'}\n"
        f"**DC ID:** `{user.dc_id}`\n"
    )

    if pfp:
        await app.send_cached_media(m.chat.id, file_id=pfp, caption=info_text)
    else:
        await app.send_edit(info_text, disable_web_page_preview=True)

    await m.delete()


@app.on_cmd(
    commands="id",
    usage="Get user id of user."
)
async def id_handler(_, m: Message):
    """ id handler for profile plugin """
    await app.send_edit("Getting id . . .", text_type=["mono"])
    cmd = m.command
    reply = m.reply_to_message
    get_user = None

    if not reply and len(cmd) == 1:
        get_user = m.from_user.id
    elif reply and len(cmd) == 1:
        get_user = reply.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]

    try:
        user = await app.get_users(get_user)
        chat = await app.get_chat(m.chat.id)
    except PeerIdInvalid:
        return await app.send_edit("I don't know that User.", text_type=["mono"])

    u_name = user.first_name if user.first_name else None
    c_name = chat.first_name if chat.first_name else chat.title

    await app.send_edit(f"**{u_name}:** `{user.id}`\n**{c_name}:** `{chat.id}`")


@app.on_cmd(
    commands=["men", "mention"],
    usage="Mention a user.",
    disable_for=UserType.SUDO
)
async def mentionuser_handler(_, m: Message):
    """ mentionuser handler for profile plugin """
    if app.command() < 3:
        return await app.send_edit(
            "Incorrect command use.\n\n**Example** : `.men @beastzx Tronuserbot`"
        )

    try:
        user = await app.get_users(m.command[1])
    except Exception as e:
        await app.send_edit("User not found !", text_type=["mono"])
        return await app.error(e)

    mention = men(user.id, " ".join(m.command[2:]))
    await app.send_edit(mention)


@app.on_cmd(
    commands="uinfo",
    usage="Get full user information."
)
async def get_full_user_info(_, m: Message):
    """Get full user info function for profile plugin"""
    await app.send_edit("🔍 Scraping user info . . .", text_type=["mono"])

    user = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    p_id = None

    try:
        async for x in app.get_chat_photos(user.id, limit=1):
            p_id = x.file_id
            break

        user_info = (
            f"🆔 **ID:** `{user.id}`\n"
            f"👤 **Name:** `{user.first_name}`\n"
            f"🌍 **DC ID:** `{getattr(user, 'dc_id', 'N/A')}`\n"
            f"🤖 **Bot:** `{user.is_bot}`\n"
            f"🎭 **Fake:** `{user.is_fake}`\n"
            f"🚨 **Scam:** `{user.is_scam}`\n"
            f"📌 **Status:** `{user.status}`\n"
            f"👀 **Is it me?** `{user.is_self}`\n"
            f"🗑 **Deleted:** `{user.is_deleted}`\n"
            f"📞 **Contact:** `{user.is_contact}`\n"
            f"✅ **Verified:** `{user.is_verified}`\n"
            f"⛔ **Restricted:** `{user.is_restricted}`\n"
        )

        if p_id:
            await app.send_cached_media(m.chat.id, file_id=p_id, caption=user_info)
            await m.delete()
        else:
            await app.send_edit(user_info)

    except Exception as e:
        await app.send_edit(
            "⚠️ An error occurred while fetching user info!", text_type=["mono"]
        )
        await app.error(e)


@app.on_cmd(
    commands=["sc", "scan"],
    usage="Scan a user from @tgscanrobot"
)
async def tgscan_handler(_, m: Message):
    """ tgscan handler for profile plugin """
    if m.reply_to_message:
        await app.send_edit("Checking database . . .")
        await app.forward_messages(
            "@tgscanrobot",
            m.chat.id,
            m.reply_to_message.id
            )
        time.sleep(0.5)
        msg = await app.get_chat_history(
            "@tgscanrobot",
            limit=1
            )
        if msg:
            user = "**INFO: **" + msg[0].text.split("\n\n1. ")[0]
            await app.send_edit(user)
        else:
            await app.send_edit("No information found !", text_type=["mono"])

    else:
        await app.send_edit("reply to someone's message . . .", delme=3, text_type=["mono"])


@app.on_cmd(
    commands="block",
    usage="Block a user.",
    disable_for=UserType.SUDO
)
async def block_handler(_, m: Message):
    """ block handler for profile plugin """
    reply = m.reply_to_message

    if app.command() >= 2 and not reply:
        user = m.command[1]
        try:
            await app.block_user(user)
            await app.send_edit("Blocked User 🚫", text_type=["mono"], delme=3)
        except Exception as e:
            await app.error(e)
    elif reply:
        user = reply.from_user.id
        try:
            await app.block_user(user)
            await app.send_edit("Blocked User 🚫", text_type=["mono"], delme=3)
        except Exception as e:
            await app.error(e)


@app.on_cmd(
    commands="unblock",
    usage="Unblock a user.",
    disable_for=UserType.SUDO
)
async def unblock_handler(_, m: Message):
    """ unblock handler for profile plugin """
    reply = m.reply_to_message

    if app.command() >= 2 and not reply:
        user = m.command[1]
        try:
            await app.unblock_user(user)
            await app.send_edit("Unblocked User 🎉", text_type=["mono"], delme=3)
        except Exception as e:
            await app.error(e)
    elif reply:
        user = reply.from_user.id
        try:
            await app.unblock_user(user)
            await app.send_edit("Unblocked User 🎉", text_type=["mono"], delme=3)
        except Exception as e:
            await app.error(e)

@app.on_cmd(
    commands="sg",
    usage="Get user name/username history."
)
async def usernamehistory_handler(_, m: Message):
    """Username history handler for profile plugin"""
    reply = m.reply_to_message

    if not reply:
        await app.send_edit(
            "⚠️ Reply to a user to get their name/username history.",
            text_type=["mono"],
            delme=2,
        )
        return

    await app.send_edit("🔍 Checking history . . .", text_type=["mono"])

    await app.forward_messages("@SangMataInfo_bot", m.chat.id, reply.id)

    is_no_record = False

    for attempt in range(8):
        await asyncio.sleep(1)  # Use async sleep

        # Fetch history properly
        history = []
        async for msg in app.get_chat_history("@SangMataInfo_bot", limit=3):
            history.append(msg)

        if not history or len(history) < 3:
            continue  # Avoid index errors if history is empty

        if history[0].text == "No records found":
            await app.send_edit("🚫 No records found!")
            is_no_record = True
            await app.read_chat_history("@SangMataInfo_bot")
            break

        if all(msg.from_user.id == 461843263 for msg in history[:3]):
            await app.read_chat_history("@SangMataInfo_bot")
            break
        else:
            print(f"🔁 Retry attempt {attempt + 1} . . .")
            continue

    if is_no_record:
        return

    # Extracting name and username history safely
    try:
        history_name = "1. " + history[2].text.split("\n\n1. ")[1]
    except IndexError:
        history_name = "❌ No name history available."

    try:
        username_history = "1. " + history[1].text.split("\n\n1. ")[1]
    except IndexError:
        username_history = "❌ No username history available."

    user_info = (
        f"📝 **Name History for** [{reply.from_user.first_name}](tg://user?id={reply.from_user.id}) (`{reply.from_user.id}`)\n\n"
        + history_name
    )

    if (
        app.textlen() <= 4096
        and len(user_info)
        + len("\n\n**🔄 Username History**\n\n")
        + len(username_history)
        <= 4906
    ):
        user_info += "\n\n**🔄 Username History**\n\n" + username_history
        await app.send_edit(user_info)
    else:
        await app.send_edit(user_info)
        await app.send_edit("\n\n**🔄 Username History**\n\n" + username_history)


@app.on_cmd(
    commands="set",
    usage="Set your profile details.",
    disable_for=UserType.SUDO
)
async def setprofile_handler(_, m: Message):
    """ setprofile handler for profile plugin """
    cmd = m.command

    if app.command() < 3:
        return await app.send_edit(
            "Please use text and suffix after command suffix: `fname`, `lname`, `bio`, `uname`"
        )

    # set -> fname, lname, bio & uname
    if app.command() > 2:
        text = m.text.split(None, 2)[2]

        if cmd[1] in ["fname", "lname", "bio"]:
            await setprofile(m, cmd[1], text)
        elif cmd[1] in ["uname"]:
            await app.update_username(text)

    else:
        return await app.send_edit("Please specify a correct suffix.", text_type=["mono"], delme=3)


@app.on_cmd(
    commands="rem",
    usage="Remove removable attributes from your profile.",
    disable_for=UserType.SUDO
)
async def remprofile_handler(_, m: Message):
    """ rmprofile handler for profile plugin """
    cmd = []
    if app.command() > 1:
        cmd = m.command

    elif app.command(m) == 1:
        return await app.send_edit(
            "what do you want to remove ? suffix: `lname`, `bio`, `pfp`, `uname`",
            delme=3
        )

    try:
        if cmd[1] in ["lname", "bio", "pfp", "uname"]:
            await rmprofile(m, cmd[1])
        else:
            await app.send_edit(
                "please use from the list:\n\n`lname`\n`bio`\n`pfp`\n`uname`",
                delme=3
            )
    except Exception as e:
        await app.error(e)


# set your profile stuffs
async def setprofile(m: Message, mode, kwargs):
    """ setprofile handler for profile plugin """
    # set first name
    if mode == "fname":
        try:
            await app.update_profile(
                first_name = f"{kwargs}"
                )
            await app.send_edit(
                f"✅ Updated first name to [ {kwargs} ]"
                )
        except Exception as e:
            await app.error(e)
    # set last name
    elif mode == "lname":
        try:
            await app.update_profile(
                last_name = f"{kwargs}"
            )
            await app.send_edit(
                f"✅ Updated last name to [ {kwargs} ]"
                )
        except Exception as e:
            await app.error(e)
    # set bio
    elif mode == "bio":
        try:
            await app.update_profile(
                bio = f"{kwargs}"
                )
            await app.send_edit(
                f"✅ Updated bio to [ {kwargs}]"
                )
        except Exception as e:
            await app.error(e)
    else:
        await app.send_edit("Please give correct format.", delme=2)


# remove everything
async def rmprofile(m: Message, args):
    """ rmprofile function for profile plugin """
    # delete last name
    if args == "lname":
        await app.update_profile(
            last_name = ""
            )
        await app.send_edit(
            "✅ Removed last name from profile."
            )
    # delete bio
    elif args == "bio":
        await app.update_profile(
            bio = "")
        await app.send_edit(
            "✅ Removed bio from profile."
            )
    # delete profile picture
    elif args == "pfp":
        photos = await app.get_profile_photos("me")
        if photos:
            await app.delete_profile_photos([p.file_id for p in photos[1:]])
            await app.send_edit(
                "✅ Deleted all photos from profile."
                )
        else:
            await app.send_edit("❌ There are no photos in your profile.")
    # delete username
    elif args == "uname":
        await app.update_username("")
        await app.send_edit(
            "✅ Removed username from profile."
            )
    else:
        await app.send_edit("Give correct format.", delme=3)


@app.on_cmd(
    commands="repo",
    usage="Get repo link.",
)
async def repolink_handler(_, m: Message):
    """ repolink handler for profile plugin """
    await app.send_edit(
        "TronUB Repo: [press here](https://github.com/TronUb/Tron)",
        disable_web_page_preview=True
    )
