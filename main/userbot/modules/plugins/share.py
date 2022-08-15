""" share plugin """

import os
import time

from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"share" : (
        "share",
        {
        "send [plugin name]" : "Send official plugin files from userbot to telegram chat.",
        "install [reply to plugin]" : "Reply to a .py file to install it in external modules directory.",
        "uninstall [name of local plugin]" : "Uninstall Local installed modules."
        }
        )
    }
)




@app.on_message(gen("send"))
async def sendplugin_handler(_, m: Message):
    """ send plugin handler for share plugin """
    if app.long() > 1:
        await app.send_edit("Checking module . . .", text_type=["mono"])
        filename = m.command[1]
        modulename = f"main/userbot/modules/plugins/{filename}.py"
        if os.path.exists(modulename):
            if app.getdv("THUMB_PIC"):
                thumb_pic = app.getdv("THUMB_PIC")
            elif app.THUMB_PIC:
                thumb_pic = app.THUMB_PIC
            else:
                thumb_pic = None

            start = time.time()
            module_caption = os.path.basename(modulename)
            await app.send_edit(f"Uploading {module_caption} . . .")

            try:
                await app.send_document(
                    m.chat.id,
                    document=modulename,
                    thumb=thumb_pic,
                    caption=(f"File name: `{module_caption}`\n\nUploaded By: {app.UserMention()}")
                    )
                await m.delete()
            except Exception as e:
                await app.error(e)
                await app.send_edit("Try again later, check log chat . . .", delme=3)
        else:
            await app.send_edit("404: plugin not found . . .", delme=2, text_type=["mono"])
    else:
        await app.send_edit(
            f"`{app.Trigger()[0]}send [ plugin name ]`  to upload plugin file.",
            delme=3
        )




@app.on_message(gen("install"))
async def install_handler(_, m: Message):
    """ install handler for share plugin """
    reply = m.reply_to_message
    if not reply:
        return await app.send_edit(
            "Reply to a python file to install . . .",
            text_type=["mono"],
            delme=4
        )

    if reply:
        if not reply.document.file_name.endswith(".py"):
            return await app.send_edit(
                "Only (.py) plugins can be installed !!",
                text_type=["mono"],
                delme=3
            )

        doc_name = reply.document.file_name

        module_loc = (
            f"./main/userbot/modules/plugins/{doc_name}"
        )
        await app.send_edit("Installing module . . .", text_type=["mono"])
        if os.path.exists(module_loc):
            return await app.send_edit(
                f"Module `{doc_name}` already exists ! skipping installation !",
                delme=4
            )

        try:
            download_loc = await app.download_media(
                message=reply,
                file_name=module_loc
            )
            if download_loc:
                await app.send_edit(f"**Installed module:** `{doc_name}`", delme=5)
                data = open(download_loc, "r")
                await app.aexec(data.read())
            else:
                await app.send_edit(
                    f"Failed to install module {doc_name}",
                    text_type=["mono"],
                    delme=4
                )
        except Exception as e:
            await app.error(e)





@app.on_message(gen("uninstall"))
async def uninstall_handler(_, m: Message):
    """ uninstal handler for share plugin """
    cmd = m.command
    try:
        if app.long() > 1:
            if cmd[1].endswith(".py"):
                module_loc = f"./main/userbot/modules/plugins/{cmd[1]}"
            elif not cmd[1].endswith(".py"):
                module_loc = f"./main/userbot/modules/plugins/{cmd[1]}.py"
            if os.path.exists(module_loc):
                os.remove(module_loc)
                await app.send_edit(f"**Uninstalled module:** {cmd[1]}", delme=3)
            else:
                await app.send_edit("Module doesn't exist !", delme=4, text_type=["mono"])
        else:
            await app.send_edit("Give me a module name . . .", text_type=["mono"], delme=3)
    except Exception as e:
        await app.error(e)
