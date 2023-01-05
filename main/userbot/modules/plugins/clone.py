""" clone plugin """

import json
from pyrogram.types import Message
from telegraph import upload_file
from main import app, gen
from main.core.enums import UserType



@app.on_cmd(
    commands="clone",
    usage="Change your account avatar to someone's else.",
    disable_for=UserType.SUDO
)
async def clone_handler(_, m: Message):
    """ clone handler for clone plugin """
    try:
        reply = m.reply_to_message

        if not reply:
            return await app.send_edit(
                "Reply to someone so that i can clone there .",
                text_type=["mono"],
                delme=3
            )

        await app.send_edit("cloning . . .", text_type=["mono"])

        # save your detials first
        profile_photos = []
        profile_data = {}

        if not app.getdv("PROFILE_DATA"):
            async for x in app.get_chat_photos(app.id):
                url = await app.download_media(x.file_id)
                response = upload_file(url)
                profile_photos.append(f"https://telegra.ph{response[0]}")

            profile_data.update(
                {
                    "first_name": app.first_name,
                    "last_name": app.last_name,
                    "bio": app.bio,
                    "photo": profile_photos[::-1]
                }
            )

            app.setdv("PROFILE_DATA", json.dumps(profile_data))

        # remove your profile photos
        async for x in app.get_chat_photos("me"):
            await app.delete_profile_photos(x.file_id)

        # set your new profile photos
        for file_id in [x.file_id async for x in app.get_chat_photos(reply.from_user.id)][::-1]:
            await app.set_profile_photo(
                photo=await app.download_media(file_id)
            )

        # set your bio, first name, last name
        user = await app.get_chat(reply.from_user.id)
        await app.update_profile(
            first_name=reply.from_user.first_name,
            last_name=reply.from_user.last_name if reply.from_user.last_name else "",
            bio=user.bio if user.bio else ""
        )

        await app.send_edit("Clone Completed !", text_type=["mono"], delme=3)

    except Exception as e:
        await app.error(e)





@app.on_cmd(
    commands="revert",
    usage="Revert back to your original account.",
    disable_for=UserType.SUDO
)
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

        if not (
            first_name or
            last_name or
            bio or
            photo
            ):
            await app.send_edit(
                "Some profile information is missing.",
                text_type=["mono"],
                delme=3
            )

        # remove old profile photos
        async for x in app.get_chat_photos("me"):
            await app.delete_profile_photos(x.file_id)

        # set your original profile pictures
        for url in photo:
            await app.set_profile_photo(
                photo=app.PyDownload(url)
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

        app.deldv("PROFILE_DATA") # delete for another use

    except Exception as e:
        await app.error(e)
