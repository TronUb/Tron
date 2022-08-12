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

        # default values
        nodata = "No Data"

        title = movie.get("long imdb title")
        year = movie.get("year") if movie.get("year") else nodata
        duration = movie.get('runtimes')[0] + "min" + f" | {year}" if movie.get('runtimes') else nodata
        genres = " ".join(f"`{x}`" for x in movie.get("genres")) if movie.get("genres") else nodata
        votes = movie.get("votes") if movie.get("votes") else nodata
        rating = movie.get("rating") + " " + f"(by {votes})"
        country = " ".join(f"`{x}`" for x in movie.get("countries")) if movie.get("countries") else nodata
        language = " ".join(f"`{x}`" for x in movie.get("languages")) if movie.get("languages") else nodata
        director = " ".join(f"`{x['name']}`" for x in movie.get("director")) if movie.get("director") else nodata
        music_director = " ".join(f"`{x['name']}`" for x in movie.get("composer")) if movie.get("composer") else nodata
        writer = " ".join(f"`{x['name']}`" for x in movie.get('writer')) if movie.get('writer') else nodata
        stars = " ".join(f"`{x['name']}`" for x in movie.get("cast")) if movie.get("cast") else nodata
        budget = box_office.get("Budget") if box_office.get("Budget") else nodata
        owus = box_office["Opening Weekend United States"] if box_office["Opening Weekend United States"] else nodata
        cwg = box_office["Cumulative Worldwide Gross"] if box_office["Cumulative Worldwide Gross"] else nodata
        plot = "".join(movie.get("plot")) if movie.get("plot") else nodata

        caption = f"**Title:** `{title}`\n"
        caption += f"**Duration:** `{duration}`\n"
        caption += f"**Genres:** {genres}\n"
        caption += f"**Rating:** `{rating}`\n"
        caption += f"**Country:** {country}\n"
        caption += f"**Language:** {language}\n"
        caption += f"**Director:** {director}\n"
        caption += f"**Music Director:** {music_director}\n"
        caption += f"**Writer:** {writer}\n"
        caption += f"**Stars:** {stars}\n"
        caption += "**Box Office:** \n"
        caption += f"> **Budget:** `{budget}`\n"
        caption += f"> **Opening Weekend United States:** `{owus}`\n"
        caption += f"> **Cumulative Worldwide Gross:** `{cwg}`\n"

        complete = await app.send_photo(
            m.chat.id,
            photo=cover_url,
            caption=caption
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
