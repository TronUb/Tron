from deep_translator import GoogleTranslator

from pyrogram.types import Message

from main import app, gen



gtl = GoogleTranslator()


@app.on_cmd(
    commands=["tr", "tl", "translate"],
    usage="Translate your texts to any language."
)
async def translate_handler(_, m: Message):
    reply = m.reply_to_message
    cmd = m.command
    oldmsg = m

    try:
        lang = cmd[1] if app.long() > 1 else "en"

        await app.send_edit(f"**Translating in** `{lang}` . . .")

        languages = list((gtl.get_supported_languages(as_dict=True)).values())

        if not lang in languages:
            return await app.send_edit("Bot doesn't support this language code, please try different one.", text_type=["mono"], delme=4)

        if (reply and reply.text):
            tdata = await translate(lang=lang, text=reply.text)
            await app.send_edit(f"**Translated to:** `{lang}`\n\n**Text: **`{tdata}`")

        elif not reply and app.textlen(oldmsg) <= 4096:
            if app.long() <= 2:
                return await app.send_edit("Give me the language code with text to translate.", text_type=["mono"], delme=4)

            text = m.text.split(None, 2)[2]
            tdata = await translate(lang=lang, text=text)
            await app.send_edit(f"**Translated to:** `{lang}`\n\n**Text:** `{tdata}`")
        else:
            await app.send_edit("Something went wrong, please try again later !", text_type=["mono"], delme=4)

    except Exception as e:
        await app.error(e)




async def translate(lang, text):
    tr = GoogleTranslator(source="auto", target=lang)
    return tr.translate(text)




@app.on_cmd(
    commands=["trlist", "tllist", "translatelist"],
    usage="Get list of supported language codes."
)
async def translatelang_handler(_, m):
    data = []
    data.clear()

    langs_list = gtl.get_supported_languages(as_dict=True)  # output: {arabic: ar, french: fr, english: en etc.}
    for keys, values in zip(langs_list.values(), langs_list.keys()):
        data.append(f"`{keys}` : `{values}`")

    await app.send_edit("**SUPPORTED LANGUAGES:**\n\n" + "\n".join(data))
        
