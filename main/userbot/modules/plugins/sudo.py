""" sudo plugin """

import json
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



sudo_types = ("common", "dev")


@app.on_message(gen("addsudo", exclude=["sudo"]))
async def addsudo_handler(_, m: Message):
    """ addsudo handler for sudo plugin """
    reply = m.reply_to_message
    args = app.GetArgs(m)
    text = None
    sudo_set = {
        "dev": set(),
        "common": set()
    }

    if not reply:
        return await app.send_edit(
            "Reply to a user to add him in sudo list",
            text_type=["mono"],
            delme=4
        )

    user_id = reply.from_user.id
    try:
        text = args.text.split(None, 1)[1]
    except IndexError:
        pass

    sudo_type = text if text and text in sudo_types else sudo_types[0]

    sudo_list = app.getdv("SUDO_USERS")
    if sudo_list:
        all_sudos = json.dumps(json.loads(sudo_list).get(sudo_type).update({user_id}))

    else:
        sudo_set.get(sudo_type).update({user_id})
        all_sudos = json.dumps(sudo_set)

    app.setdv("SUDO_USERS", all_sudos)
    await app.send_edit(
        f"{reply.from_user.mention()} `has been added to sudo.`",
        delme=4
    )




@app.on_message(gen("listsudo"))
async def getsudo_handler(_, m: Message):
    """ getsudo hanlder for sudo plugin """
    sudo_list = app.getdv("SUDO_USERS")
    if not sudo_list:
        return await app.send_edit(
            "No sudos are added !",
            text_type=["mono"],
            delme=3
        )

    sudo_list = json.loads(sudo_list)

    common_sudos = [x for x in sudo_list[sudo_types[0]]]
    dev_sudos = [x for x in sudo_list[sudo_types[1]]]

    sudos = "dev sudos:\n\n{}\n\ncommon sudos:{}".format("\n".join(dev_sudos), "\n".join(common_sudos))
    await app.send_edit("**Available Sudo id:**\n" + sudos)




@app.on_message(gen("delsudo", exclude=["sudo"]))
async def delsudo_handler(_, m: Message):
    """ delsudo handler for sudo plugin """
    reply = m.reply_to_message
    user_id = reply.from_user.id
    if not reply:
        return await app.send_edit(
            "Reply to a user to remove him from sudo list.",
            text_type=["mono"],
            delme=4
        )

    sudo_list = app.getdv("SUDO_USERS")

    if not sudo_list:
        return await app.send_edit(
            "No sudos are added !",
            text_type=["mono"],
            delme=3
        )

    sudo_list = json.loads(sudo_list)

    common_sudos = ["common"] + [x for x in sudo_list[sudo_types[0]]]
    dev_sudos = ["dev"] + [x for x in sudo_list[sudo_types[1]]]

    if user_id in common_sudos:
        sudo_list[common_sudos[0]].remove(user_id)
        app.setdv("SUDO_USERS", sudo_list)
    elif user_id in dev_sudos:
        sudo_list[dev_sudos[0]].remove(user_id)
    else:
        return await app.send_edit(
            "This user is not in sudo list",
            text_type=["mono"],
            delme=4
        )

    await app.send_edit(
        f"{reply.from_user.mention()} `has been removed from sudo list`",
        delme=4
    )
