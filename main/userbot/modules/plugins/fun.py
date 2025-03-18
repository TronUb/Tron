""" fun plugin """

import html
import time
import random
import asyncio
import aiohttp

from pyrogram.errors import FloodWait

from main import app
from main.core.enums import UserType


@app.on_cmd(
    commands="slap",
    usage="Fun text of slapping someone."
)
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
            me = app.UserMention

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
            await log_error(e)
    else:
        await app.send_edit(
            "Reply to a friend to use harsh sentences to insult him",
            text_type=["mono"],
            delme=3
        )


@app.on_cmd(
    commands="upcase",
    usage="Convert a text to upper-case."
)
async def uppercase_handler(_, m):
    """ uppercase handler for fun plugin """
    try:
        reply = m.reply_to_message
        if reply:
            text = reply.text.upper()
            await app.send_edit(text)
        elif not reply:
            if app.command() > 1:
                text = m.text.split(None, 1)[1].upper()
                await app.send_edit(text)
            elif app.command() == 1:
                await app.send_edit(
                    "Please give me some text after command or reply to someone.",
                    text_type=["mono"],
                    delme= 3
                )
        else:
            return await app.send_edit("upcase command Error !", text_type=["mono"], delme=4)
    except Exception as e:
        await log_error(e)


@app.on_cmd(
    commands="type",
    usage="Text typing animation, use less."
)
async def type_handler(_, m):
    """ type handler for fu plugin """
    try:
        if app.command() > 1:
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
        await log_error(e)


@app.on_cmd(
    commands="insult",
    usage="Insulting texts for your friends.",
    disable_for=UserType.SUDO
)
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
                return await app.send_edit(
                    "You can't insult youself.", text_type=["mono"], delme=3
                )

            lang = (
                "en"
                if app.command() == 1
                else m.command[1] if app.command() > 1 else "en"
            )
            response = await app.fetch_url(
                f"https://evilinsult.com/generate_insult.php?lang={lang}&type=json"
            )

            if response and response.get("status") == 200 and "data" in response:
                data = response["data"]  # Extract the actual insult JSON
            else:
                data = {"error": "Failed to fetch insult."}  # Handle errors properly

            await app.send_edit("Insulting . . .", text_type=["mono"])
            if data:
                await app.send_edit(f"`{data.get('insult')}`")
            else:
                await app.send_edit("No insults found !", delme=3, text_type=["mono"])
        except Exception as e:
            await log_error(e)


@app.on_cmd(commands="advice", usage="Give someone advice.")
async def advice_handler(_, m):
    """Advice handler for fun plugin"""
    reply = m.reply_to_message

    if not reply:
        await app.send_edit(
            "Please reply to someone, so that I can give them advice . . .",
            delme=3,
            text_type=["mono"],
        )
        return  # Exit function if no reply

    try:
        await app.send_edit("Finding a good piece of advice . . .", text_type=["mono"])

        # Fetch the advice JSON safely
        response = await app.fetch_url("https://api.adviceslip.com/advice")

        if response and response.get("status") == 200 and "data" in response:
            advice_text = response["data"].get("slip", {}).get("advice")
            if advice_text:
                await app.send_edit(f"`{advice_text}`")
            else:
                await app.send_edit("No advice found!", delme=3, text_type=["mono"])
        else:
            await app.send_edit("Failed to fetch advice!", delme=3, text_type=["mono"])

    except Exception as e:
        await log_error(f"Error: {str(e)}")


@app.on_cmd(commands="uadvice", usage="Give someone a useless advice.")
async def useless_advice_handler(_, m):
    """Handler for fetching and sending useless advice."""
    reply = m.reply_to_message

    if not reply:
        await app.send_edit(
            "Please reply to someone, so that I can give them a useless advice . . .",
            delme=3,
            text_type=["mono"],
        )
        return  # Exit function if no reply

    try:
        await app.send_edit("Finding a useless advice . . .", text_type=["mono"])

        # Fetch the advice safely
        response = await app.fetch_url(
            "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
        )

        if response and response.get("status") == 200 and "data" in response:
            useless_advice = response["data"].get("text")
            if useless_advice:
                await app.send_edit(f"`{useless_advice}`")
            else:
                await app.send_edit(
                    "No useless advice found!", delme=3, text_type=["mono"]
                )
        else:
            await app.send_edit(
                "Failed to fetch useless advice!", delme=3, text_type=["mono"]
            )

    except Exception as e:
        await log_error(f"Error: {str(e)}")


@app.on_cmd(
    commands="qs",
    usage="Ask someone a random trivia question, answers in saved message.",
)
async def question_handler(_, m):
    """Question handler for fun plugin"""
    reply = m.reply_to_message
    if not reply:
        return await app.send_edit(
            "Please reply to someone, so that I can ask them a question...",
            delme=3,
            text_type=["mono"],
        )

    try:
        await app.send_edit("Finding a question...", text_type=["mono"])

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://opentdb.com/api.php?amount=1&type=multiple"
            ) as resp:
                data = await resp.json()

        if "results" in data and data["results"]:
            question_data = data["results"][0]
            category = html.unescape(question_data.get("category", "Unknown Category"))
            question = html.unescape(
                question_data.get("question", "No question found!")
            )
            correct_answer = html.unescape(
                question_data.get("correct_answer", "No answer found!")
            )
            incorrect_answers = [
                html.unescape(ans) for ans in question_data.get("incorrect_answers", [])
            ]

            # Combine correct and incorrect answers & shuffle
            options = incorrect_answers + [correct_answer]
            random.shuffle(options)

            options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])

            await app.send_edit(
                f"🎭 **Category:** {category}\n\n"
                f"🧐 **Question:**\n\n`{question}`\n\n"
                f"📌 **Options:**\n{options_text}\n\n"
                "*Answer saved in your messages.*"
            )

            await app.send_message(
                "me", f"✅ **Correct Answer:**\n\n`{correct_answer}`"
            )  # Answer in saved messages
        else:
            await app.send_edit("No question found!", delme=3, text_type=["mono"])

    except Exception as e:
        await app.send_edit(f"Error: {e}", text_type=["mono"], delme=4)

@app.on_cmd(
    commands="wtd",
    usage="Suggest some activities to do."
)
async def whattodo_handler(_, m):
    """Suggests a random activity for fun"""
    try:
        await app.send_edit("🔍 Finding an activity...", text_type=["mono"])

        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.boredapi.com/api/activity/") as resp:
                if resp.status != 200:
                    return await app.send_edit(
                        "⚠️ API is down, try again later.", delme=3, text_type=["mono"]
                    )

                act = await resp.json()

        if act and "activity" in act:
            activity = act.get("activity", "No activity found!")
            _type = act.get("type", "Unknown type")

            await app.send_edit(
                f"🎭 **Activity:** `{activity}`\n\n📌 **Type:** `{_type}`"
            )
        else:
            await app.send_edit("No Activity found!", delme=3, text_type=["mono"])

    except Exception as e:
        await app.send_edit(f"⚠️ Error: {e}", text_type=["mono"], delme=4)

@app.on_cmd(
    commands="mqt",
    usage="Get movie quotes."
)
async def moviequote_handler(_, m):
    """Movie quote handler for fun plugin"""
    try:
        await app.send_edit("Finding a movie quote . . .", text_type=["mono"])

        # Fetch movie quote safely
        response = await app.fetch_url("https://favqs.com/api/qotd")

        if response and response.get("status") == 200 and "data" in response:
            quote_data = response["data"].get("quote", {})
            quote_text = quote_data.get("body")
            author = quote_data.get("author")

            if quote_text and author:
                await app.send_edit(
                    f"**🎬 Movie Quote:**\n\n`{quote_text}`\n\n📽️ Role: `{author}`"
                )
            else:
                await app.send_edit(
                    "No movie quotes found!", delme=3, text_type=["mono"]
                )
        else:
            await app.send_edit(
                "Failed to fetch movie quotes!", delme=3, text_type=["mono"]
            )

    except Exception as e:
        await log_error(f"Error: {str(e)}")


@app.on_cmd(
    commands="joke",
    usage="Get some jokes."
)
async def joke_handler(_, m):
    """Joke handler for fun plugin"""
    try:
        await app.send_edit("Finding a joke . . .", text_type=["mono"])

        # Fetch joke safely
        response = await app.fetch_url(
            "https://icanhazdadjoke.com/slack",
            headers={"User-Agent": "TelegramBot"},
        )

        if response and response.get("status") == 200:
            attachments = response.get("data", {}).get("attachments", [])
            joke_text = attachments[0].get("fallback") if attachments else None

            if joke_text:
                await app.send_edit(f"{joke_text}")
            else:
                await app.send_edit("No jokes found!", delme=3, text_type=["mono"])
        else:
            await app.send_edit(
                "Joke site is down, please try again later.",
                delme=3,
                text_type=["mono"],
            )

    except Exception as e:
        await app.send_edit(
            "Joke site is down, try again later.", delme=3, text_type=["mono"]
        )
        await log_error(f"Error fetching joke: {str(e)}")
