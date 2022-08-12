""" imdb plugin """

import imdb
from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"imdb" : (
        "imdb",
        {
        "imdb" : "search a movie and get its metadata on imdb."
        }
        )
    }
)




@app.on_message(gen("imdb"))
async def imdb_handler(_, m: Message):
    """ imdb handler for imdb plugin """
    try:
        args = app.GetArgs(m)
        if not args:
            return await app.send_edit("give me a movie name.", text_type=["mono"], delme=3)

        if not args.text:
            return await app.send_edit("There is no text in message.", text_type=["mono"], delme=3)

        msg = await app.send_edit("Searching . . .", text_type=["mono"])
        movie_name = args.text.split(None, 1)[1]

        i = imdb.Cinemagoer()
        results = i.search_movie(movie_name)[0]
        movie = i.get_movie(results.movieID)

        box_office = movie["box office"]
        cover_url = app.PyDownload(movie["full-size cover url"])

        caption = f"**Title:** `{movie['long imdb title']}`\n"
        caption += f"**Duration:** `{movie['runtimes'][0]} min | {movie['year']}`\n"
        caption += f"**Genres:** {' '.join(f'''`{x}`''' for x in movie['genres'])}\n"
        caption += f"**Rating:** `{movie['rating']} (by {movie['votes']})`\n"
        caption += f"**Country:** {' '.join(f'`{x}`' for x in movie['countries'])}\n"
        caption += f"**Language:** {' '.join(f'`{x}`' for x in movie['languages'])}\n"
        caption += f"**Director:** {' '.join(f'''`{x['name']}`''' for x in movie['director'])}\n"
        caption += f"**Music Director:** {' '.join(f'''`{x['name']}`''' for x in movie['composer'])}\n"
        caption += f"**Writer:** {' '.join(f'''`{x['name']}`''' for x in movie['writer'])}\n"
        caption += f"**Stars:** {' '.join(f'''`{x['name']}`''' for x in movie['cast'])}\n"
        caption += "**Box Office:** \n"
        caption += f"> **Budget:** `{box_office['Budget']}`\n"
        caption += f"> **Opening Weekend United States:** `{box_office['Opening Weekend United States']}`\n"
        caption += f"> **Cumulative Worldwide Gross:** `{box_office['Cumulative Worldwide Gross']}`\n"
        caption += f"**Story Outline:** `{movie['plot'][0][:100]+'...'}`\n"
        
        link = app.telegraph.create_page(
            app.name,
            html_content=caption
        )
        
        url = f"https://telegra.ph/{link.get('path')}"

        complete = await app.send_photo(
            m.chat.id,
            photo=cover_url,
            caption=f"[Results]({url})"
        )

        if complete:
            await msg.delete()
        else:
            await app.send_edit(
                "failed to get movie metadata, try again later.",
                text_type=["mono"]
            )
    except Exception as e:
        await app.error(e)
