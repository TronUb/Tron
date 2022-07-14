from pyrogram.types import Message
from main import app, gen




app.CMD_HELP.update(
    {"sudo" : (
        "sudo",
        {
        "addsudo [reply to user]" : "Add a user into your sudo list.", 
        "listsudo " : "Get list of available sudo ids.",
        "delsudo [reply to user]" : "Delete a user from your sudo list."
        }
        )
    }
)




@app.on_message(gen("addsudo"))
async def addsudo_handler(_, m: Message):
    reply = m.reply_to_message

    if not reply:
        return await app.send_edit(m, "Reply to a user to add him in sudo list", text_type=["mono"], delme=4)  

    sudo_list = app.getdv("SUDO_USERS")
    if sudo_list:
        all_sudo = [x for x in sudo_list.split()] + [str(reply.from_user.id)]
    else:
        all_sudo = [str(reply.from_user.id)]

    app.setdv("SUDO_USERS", " ".join(list(set(all_sudo)))) # rem duplicates
    await app.send_edit(f"{reply.from_user.mention()} `has been added to sudo.`", delme=4)




@app.on_message(gen("listsudo", allow = ["sudo"]))
async def getsudo_handler(_, m: Message):
    sudo_list = [x for x in app.getdv("SUDO_USERS").split()]
    sudo_list = "No sudos added." if not sudo_list else sudo_list
    await app.send_edit("**Available Sudo id:**\n\n" + "\n".join(sudo_list))




@app.on_message(gen("delsudo"))
async def delsudo_handler(_, m: Message):
    reply = m.reply_to_message
    user_id = str(reply.from_user.id)
    if not reply:
        return await app.send_edit("Reply to a user to remove him from sudo list.", text_type=["mono"], delme=4)  

    sudo_list = [x for x in app.getdv("SUDO_USERS").split()]
    if user_id in sudo_list:
        sudo_list.remove(user_id)
        app.setdv("SUDO_USERS", " ".join(sudo_list))
    else:
        return await app.send_edit("This user is not in sudo list", text_type=["mono"], delme=4)

    await app.send_edit(f"{reply.from_user.mention()} `has been removed from sudo list`", delme=4)


