""" fun plugin """

import time
import random
import asyncio

from pyrogram.errors import FloodWait

from main import app, gen




app.CMD_HELP.update(
    {"fun" : (
        "fun",
        {
        "upcase [text]" : "Convert texts into uppercase",
        "slap [reply to user]" : "Slap your friends with amazing items.",
        "type [text]" : "Retype words with animation, just try and understand, Don't Use too much.",
        "insult [reply to message]" : "Use it to insult idiots & fools",
        "advice [reply to message]" : "get a random advice for someone.",
        "wtd" : "what to do when you are bored ?, finds a activity for you.",
        "mqt" : "Finds some movie quotes for you.",
        "joke" : "Get some daddy jokes.",
        }
        )
    }
)




@app.on_message(gen("slap"))
async def slap_handler(_, m):
    """ slap handler for fun plugin """
    reply = m.reply_to_message
    if reply:
        try:
            await app.send_edit(". . .")

            user = reply.from_user
            if user.is_self:
                return await app.send_edit("You cant slap youself.", text_type=["mono"], delme=3)

            user = user.mention
            me = app.UserMention()

            SLAP_TEXT = (
                f"{me} slaps {user} with a bunch of cardboards",
                f"{me} hits {user} in the face with cows",
                f"{me} ties {user} on a chair and rubs him with a sandpaper",
                f"{me} helped {user} swimming in lava",
                f"{me} starts slapping {user} with Titanic ship",
                f"{me} fills a book of physics in {user} mouth",
                f"{me} gives a cup of poison to {user} ",
                f"{me} slaps {user} with bunch of dead mosquito",
                f"{me} hits {user}'s face with rubber chicken",
                f"{me} starts puts {user} in water with phirana",
                f"{me} dumps {user} in a river",
                f"{me} pats {user} on head",
                f"{me} kicks {user} out of the conversation",
            )
            await app.send_edit(random.choice(SLAP_TEXT))

        except Exception as e:
            await app.error(e)
    else:
        await app.send_edit(
            "Reply to a friend to use harsh words to insult him",
            text_type=["mono"],
            delme=3
        )




@app.on_message(gen(["upcase"]))
async def uppercase_handler(_, m):
    """ uppercase handler for fun plugin """
    try:
        reply = m.reply_to_message
        if reply:
            text = reply.text.upper()
            await app.send_edit(text)
        elif not reply:
            if app.long() > 1:
                text = m.text.split(None, 1)[1].upper()
                await app.send_edit(text)
            elif app.long() == 1:
                await app.send_edit(
                    "Please give me some text after command or reply to someone.",
                    text_type=["mono"],
                    delme= 3
                )
        else:
            return await app.send_edit("upcase command Error !", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)




@app.on_message(gen("type"))
async def type_handler(_, m):
    """ type handler for fu plugin """
    try:
        if app.long() > 1:
            text = [x for x in m.text.split(None, 1)[1]]
        else:
            return await app.send_edit("Some text is required to show in typing animation", delme=3)

        tbp = ""
        typing_symbol = "▒"
        for i in range(len(text)):
            try:
                await app.send_edit(tbp + typing_symbol)
                await asyncio.sleep(0.40)
                tbp = tbp + text[i]
                await app.send_edit(tbp)
                await asyncio.sleep(0.70)
            except FloodWait as e:
                time.sleep(e.value) # continue
    except Exception as e:
        await app.error(e)




@app.on_message(gen("insult", exclude =["sudo"]))
async def insult_handler(_, m):
    """ insult handler for fun plugin """
    reply = m.reply_to_message
    if not reply:
        await app.send_edit(
            "Please reply to someone, so that i can insult them.",
            text_type=["mono"],
            delme=3
        )

    elif reply:
        try:
            if reply.from_user.is_self:
                return await app.send_edit("You cant insult youself.", text_type=["mono"], delme=3)

            lang = "en" if app.long() == 1 else m.command[1] if app.long() > 1 else "en"
            data = await app.GetRequest(
                f"https://evilinsult.com/generate_insult.php?lang={lang}&type=json"
            )

            await app.send_edit("Insulting . . .", text_type=["mono"])
            if data:
                await app.send_edit(f"`{data.get('insult')}`")
            else:
                await app.send_edit("No insults found !", delme=3, text_type=["mono"])
        except Exception as e:
            await app.error(e)




@app.on_message(gen("advice"))
async def advice_handler(_, m):
    """ advice handler for fun plugin """
    reply = m.reply_to_message
    if not reply:
        await app.send_edit(
            "Please reply to someone, so that i can give them a advice . . .",
            delme=3,
            text_type=["mono"]
        )

    elif reply:
        try:
            await app.send_edit("Finding a good advice . . .", text_type=["mono"])
            data = await app.GetRequest("https://api.adviceslip.com/advice")
            data = data.get("slip").get("advice")
            if data:
                await app.send_edit(f"`{data}`")
            else:
                await app.send_edit("No advice found !", delme=3, text_type=["mono"])
        except Exception as e:
            await app.error(e)




@app.on_message(gen("qs"))
async def question_handler(_, m):
    """ question handler for fun plugin """
    reply = m.reply_to_message
    if not reply:
        await app.send_edit(
            "Please reply to someone, so that i can ask them a question . . .",
            delme=3,
            text_type=["mono"]
        )

    elif reply:
        try:
            await app.send_edit("Finding a question . . .", text_type=["mono"])
            data = await app.GetRequest("http://jservice.io/api/random")
            question = data[0].get("question")
            answer = data[0].get("answer")
            if question and answer:
                await app.send_edit(f"Question:\n\n`{question}`\n\nAnswer in saved message.")
                await app.send_message("me", f"Answer:\n\n`{answer}`") # answer in saved messages
            else:
                await app.send_edit("No question found !", delme=3, text_type=["mono"])
        except Exception as e:
            await app.error(e)




@app.on_message(gen("wtd"))
async def whattodo_handler(_, m):
    """ what to do handler for fun plugin """
    try:
        await app.send_edit("Finding a activity . . .", text_type=["mono"])
        act = await app.GetRequest("http://www.boredapi.com/api/activity/")
        activity = act.get("activity")
        _type = act.get("type")
        if act:
            await app.send_edit(f"Activity: `{activity}`\n\nType: `{_type}`")
        else:
            await app.send_edit("No Activity found !", delme=3, text_type=["mono"])
    except Exception as e:
        await app.error(e)




@app.on_message(gen("mqt"))
async def moviequote_handler(_, m):
    """ movie quote handler for fun plugin """
    try:
        await app.send_edit("Finding a movie quote . . .", text_type=["mono"])
        data = await app.GetRequest("https://movie-quote-api.herokuapp.com/v1/quote/")
        qt = data.get("quote")
        role = data.get("role")
        show = data.get("show")
        if qt and role and show:
            await app.send_edit(f"**Quote:**\n\n`{qt}`\n\nRole: `{role}`\n\nShow: `{show}`")
        else:
            await app.send_edit("No movie quotes found !", delme=3, text_type=["mono"])
    except Exception as e:
        await app.error(e)




@app.on_message(gen("joke"))
async def joke_handler(_, m):
    """ joke handler for fun plugin """
    try:
        await app.send_edit("Finding a joke . . .", text_type=["mono"])
        data = (await app.GetRequest("https://icanhazdadjoke.com/slack")
            )["attachments"][0]["fallback"]
        if not data:
            return app.send_edit(
                "Site is down, please try again later . . .",
                delme=3,
                text_type=["mono"]
            )
        elif data:
            await app.send_edit(f"{data}")
        else:
            await app.send_edit("No jokes found !", delme=3, text_type=["mono"])
    except Exception as e:
        await app.send_edit("Joke site is down, try again later.", text_type=["mono"], delme=3)
        await app.error(e)
