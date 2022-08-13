""" clone plugin """

import json
from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"clone" : (
        "clone",
        {
        "clone [reply]" : "clone your friends account for fun.",
        "revert" : "unclone your account to normal."
        }
        )
    }
)





@app.on_message(gen(["clone"]))
async def clone_handler(_, m: Message):
    """ clone handler for clone plugin """
    try:
        reply = m.reply_to_message

        if not reply:
            return await app.send_edit(
                "Reply to someone so i can clone them.",
                text_type=["mono"],
                delme=3
            )

        reply = reply.from_user

        await app.send_edit("cloning . . .", text_type=["mono"], delme=3)

        # save your detials first
        profile_photos = {}
        profile_data = {}

        if not app.getdv("PROFILE_DATA"):
            async for x in [x.file_id async for x in app.get_chat_photos("me")][::-1]:
                profile_photos.update(x.file_id)

            profile_data.update(
                {
                    "first_name": app.first_name,
                    "last_name": app.last_name,
                    "bio": app.bio,
                    "photo": profile_photos
                }
            )

            app.setdv("PROFILE_DATA", json.dumps(profile_data))

        # remove your profile photos
        async for x in app.get_chat_photos("me"):
            await app.delete_profile_photos(x.file_id)

        # set your new profile photos
        for file_id in [x.file_id async for x in app.get_chat_photos(reply.id)][::-1]:
            await app.set_profile_photo(
                photo=await app.download_media(file_id)
            )

        # set your bio, first name, last name
        user = await app.get_chat(reply.from_user.id)
        await app.update_profile(
            first_name=reply.first_name,
            last_name=reply.last_name if reply.last_name else "",
            bio=user.bio if user.bio else ""
        )

        await app.send_edit("Clone Completed !", text_type=["mono"], delme=3)

    except Exception as e:
        await app.error(e)





@app.on_message(gen("revert"))
async def revert_handler(_, m: Message):
    """ revert handler for clone plugin """
    try:
        await app.send_edit(
            "Reverting account to normal . . .",
            text_type=["mono"],
            delme=3
        )

        info = app.getdv("PROFILE_DATA")

        if not info:
            await app.send_edit(
                "Your old profile data doesn't exist, set it manually.",
                text_type=["mono"],
                delme=3
            )

        data = json.loads(info)

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        bio = data.get("bio")
        photo = data.get("photo")

        # set your profile pictures
        for file_id in photo:
            await app.set_profile_photo(
                photo=await app.download_media(file_id)
            )

        # set your bio, first name, last name
        await app.update_profile(
            first_name=first_name,
            last_name=last_name if last_name else "",
            bio=bio if bio else ""
        )

        await app.send_edit("Revert successful !",
            text_type=["mono"],
            delme=3
        )

    except Exception as e:
        await app.error(e)
