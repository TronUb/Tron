""" dv plugin """

from pyrogram.types import Message

from main import app, gen
from main.core.enums import UserType


@app.on_cmd(
    commands="setdv",
    usage="Set database variable.",
    disable_for=UserType.SUDO
)
async def setdv_handler(_, m: Message):
    """ setdv handler for dv plugin """
    if app.command() == 1:
        await app.send_edit("Give me a key & a value to set dv vars.", text_type=["mono"], delme=4)

    elif app.textlen() > 4096:
        await app.send_edit(
            "Text is too long. only 4096 characters are excludeed.",
            text_type=["mono"],
            delme=4
        )

    elif app.command() == 2:
        await app.send_edit("Please give me key with a value.", text_type=["mono"], delme=4)

    elif app.command() > 2:
        key = m.command[1]
        value = m.text.split(None, 2)[2]
        done = app.setdv(key, value)

        if done:
            await app.send_edit(
                f"Added database var with [ **key** = `{key}` ] and [ **value** = `{value}` ]"
            )

        elif not done:
            await app.send_edit(
                "Failed to a add key & value to database var.",
                text_type=["mono"],
                delme=2
            )


@app.on_cmd(
    commands="deldv",
    usage="Delete a database variable.",
    disable_for=UserType.SUDO
)
async def deldv_handler(_, m: Message):
    """ deldv handler for dv plugin """
    if app.command() == 1:
        await app.send_edit(
            "Give me some key to delete that a var from database . . . ",
            text_type=["mono"],
            delme=2
        )

    elif app.textlen() > 4096:
        await app.send_edit(
            "text is too long. only 4096 characters are excluded.",
            text_type=["mono"],
            delme=4
        )

    elif app.command() > 1:
        keys = "**Deleted vars:**\n\n"
        cmd = m.command
        for key in cmd[1:]:
            done = app.deldv(key)
            keys += f"`{key}`"

        if done:
            await app.send_edit(f"Successfully deleted keys.\n\n{keys}", delme=4)
        else:
            await app.send_edit(f"Unable delete keys.\n\n{keys}", delme=4)
    else:
        await app.send_edit("Something went wrong, try again later !", text_type=["mono"], delme=4)


@app.on_cmd(
    commands="getdv",
    usage="Get value of databae variable.",
    disable_for=UserType.SUDO
)
async def getdv_handler(_, m: Message):
    """ getdv handler for dv plugin """
    if app.command() == 1:
        await app.send_edit(
            "Give me some key to get value that a var from database . . . ",
            text_type=["mono"],
            delme=2
        )

    elif app.command() > 1:
        key = m.command[1]
        done = app.getdv(key)

        if done:
            await app.send_edit(f"**Here:**\n\n**key** = `{key}`\n\n**value** = `{done}`", delme=4)
        else:
            await app.send_edit(
                "This var doesn't exist in my database.",
                text_type=["mono"],
                delme=4
            )
    else:
        await app.send_edit(
            "Maximum 4096 characters in one message . . .",
            text_type=["mono"],
            delme=4
        )


@app.on_cmd(
    commands=["pmgaurd", "pm"],
    usage="Activate/Deactivate pm gaurd for unwanted spammer block",
)
async def pm_handler(_, m: Message):
    """ pm handler for dv plugin """
    arg = m.command
    if app.command() == 1:
        await app.send_edit("Provide me a suffix to do some work.\n\nSuffix: `on` & `off`", delme=4)

    elif app.command() > 1 and arg[1] == "on":
        if app.Pmpermit is True:
            return await app.send_edit("Pmguard is already active !", text_type=["mono"], delme=4)

        done = app.setdv("PMPERMIT", "True")
        if done:
            await app.send_edit("Pmguard is now turned on.", text_type=["mono"], delme=4)
        else:
            await app.send_edit("Failed to turn on pmguard.", text_type=["mono"], delme=4)

    elif app.command() > 1 and arg[1] == "off":
        if app.Pmpermit is False:
            return await app.send_edit("Pmguard is already off !", text_type=["mono"], delme=4)

        done = app.deldv("PMPERMIT")
        if done:
            await app.send_edit("Pmguard is now turned off.", text_type=["mono"], delme=4)
        else:
            await app.send_edit("Failed to turn off pmguard.", text_type=["mono"], delme=4)

    elif app.command() > 1 and arg[1] not in ("on", "off"):
        await app.send_edit("Use `on` or `off` after command to turn on & off pmguard.", delme=4)
    else:
        await app.send_edit(
            "Something went wrong, please try again later !",
            text_type=["mono"],
            delme=4
        )


@app.on_cmd(
    commands=["listdv", "ldv"],
    usage="Get all database variables & values.",
    disable_for=UserType.SUDO,
)
async def listdv_handler(_, m: Message):
    """ listdv handler for dv plugin """
    if bool(app.getalldv()) is True:
        await app.send_edit("Getting all database vars . . .", text_type=["mono"])
        my_dict = app.getalldv()
        dict_data = []
        dict_data.clear()

        for key, value in zip(my_dict.keys(), my_dict.values()):
            dict_data.append(f"`{key}` = `{value}`\n\n")

        await app.send_edit("**All DB VARS:**\n\n" + "".join(dict_data))
    else:
        await app.send_edit("There are no database vars (empty) !", text_type=["mono"], delme=4)


@app.on_cmd(
    commands="alldv",
    usage="Get all available database variable names."
)
async def alldv_handler(_, m: Message):
    """ alldv handler for dv plugin """
    allvars = [f"`{x}`" for x in app.DVLIST]
    await app.send_edit("**AVAILABLE DB VARS:**\n\n" + "\n".join(allvars))
