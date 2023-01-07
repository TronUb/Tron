""" sudo plugin """

from pyrogram.types import Message
from main import app
from main.core.enums import UserType




@app.on_cmd(
    commands="addsudo",
    usage="Give your userbot access to someone else.",
    disable_for=UserType.SUDO,
    reply=True
)
async def addsudo_handler(_, m: Message):
    """ addsudo handler for sudo plugin """
    try:
        sudos = app.SudoUsers
        user = m.reply_to_message.from_user
        default_cmds = {
            "ping", "help", "alive", "ialive",
            "img", "cat", "dog", "q", "joke"
        }

        try:
            sudo_cmds = m.text.split(None, 1)[1]
        except IndexError:
            sudo_cmds = default_cmds

        if user.id in sudos:
            return await app.send_edit(
                "The user is already in sudo list.",
                text_type=["mono"],
                delme=3
            )

        else:
            app.set_sudo(
                user.id,
                user.first_name,
                sudo_cmds
            )

            await app.send_edit(
                f"Added {user.mention} as sudo."
                delme=3
            )
    except Exception as e:
        await app.error(e)




@app.on_cmd(
    commands="listsudo",
    usage="Get available sudo's user ids.",
    disable_for=UserType.SUDO
)
async def getsudo_handler(_, m: Message):
    """ getsudo hanlder for sudo plugin """
    try:
        sudos = app.all_sudo().items()
        text = "Available sudos:\n\n"

        r = [
            f"{x[1].get('sudo_name')} ({x[0]})\n" 
            for x in sudos
        ]

        if r:
            await app.send_edit(
                text + "".join(r),
                delme=3
            )
        else:
            await app.send_edit(
                text + "\nNo Sudo Added !",
                delme=3
            )
    except Exception as e:
        await app.error(e)




@app.on_cmd(
    commands="delsudo",
    usage="Remove a user from your sudo users list.",
    disable_for=UserType.SUDO,
    reply=True
)
async def delsudo_handler(_, m: Message):
    """ delsudo handler for sudo plugin """
    try:
        user = m.reply_to_message.from_user
        sudos = app.SudoUsers

        try:
            sudo_id = m.text.split(None, 1)[1]
        except IndexError:
            sudo_id = None

        if not sudo_id:
            return await app.send_edit(
                "Give me sudo user id so that i can delete them.",
                delme=3
            )

        if not sudo_id in sudos:
            await app.send_edit(
                "This user is not a sudo !",
                text_type=["mono"],
                delme=3
            )
        else:
            app.del_sudo(sudo_id)
            await app.send_edit(
                f"Deleted {user.mention} from sudo.",
                delme=3
            )
    except Exception as e:
        await app.error(e)
