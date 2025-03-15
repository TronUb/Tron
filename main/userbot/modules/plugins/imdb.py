import imdb
from pyrogram.types import Message
from main import app, gen


@app.on_cmd(commands="imdb", usage="Get IMDb details of a movie.")
async def imdb_handler(_, m: Message):
    """IMDb handler for IMDb plugin"""
    try:
        args = app.GetArgs(m)
        if not args:
            return await app.send_edit(
                "🎬 **Give me a movie name!**", text_type=["mono"], delme=3
            )

        if not args.text:
            return await app.send_edit(
                "❌ **There is no text in the message.**", text_type=["mono"], delme=3
            )

        msg = await app.send_edit("🔎 **Searching...**", text_type=["mono"])
        movie_name = args.text.split(None, 1)[1]

        i = imdb.Cinemagoer()
        results = i.search_movie(movie_name)
        if not results:
            return await app.send_edit(
                "❌ **No results found.**", text_type=["mono"], delme=3
            )

        print("results::", results)
        movie = i.get_movie(results[0].movieID)
        nodata = "N/A"

        box_office = movie.get("box office", {})
        cover_url = app.PyDownload(movie.get("full-size cover url", ""))

        title = movie.get("long imdb title", nodata)
        year = movie.get("year", nodata)
        duration = f"{movie.get('runtimes', [nodata])[0]} min | {year}"
        genres = ", ".join(f"`{x}`" for x in movie.get("genres", [])) or nodata
        votes = movie.get("votes", nodata)
        rating = f"{movie.get('rating', nodata)} ⭐ (by {votes})"
        country = ", ".join(f"`{x}`" for x in movie.get("countries", [])) or nodata
        language = ", ".join(f"`{x}`" for x in movie.get("languages", [])) or nodata
        director = (
            ", ".join(f"`{x.get('name')}`" for x in movie.get("director", [])) or nodata
        )
        music_director = (
            ", ".join(f"`{x.get('name')}`" for x in movie.get("composer", [])) or nodata
        )
        writer = (
            ", ".join(f"`{x.get('name')}`" for x in movie.get("writer", [])) or nodata
        )
        budget = box_office.get("Budget", nodata)
        owus = box_office.get("Opening Weekend United States", nodata)
        cwg = box_office.get("Cumulative Worldwide Gross", nodata)

        caption = f"""
🎬 **Title:** `{title}`
⏳ **Duration:** `{duration}`
🎭 **Genres:** {genres}
⭐ **Rating:** `{rating}`
🌍 **Country:** {country}
🗣 **Language:** {language}
🎬 **Director:** {director}
🎼 **Music Director:** {music_director}
✍️ **Writer:** {writer}

💰 **Box Office:**
🏆 **Budget:** `{budget}`
🎟 **Opening Weekend US:** `{owus}`
🌎 **Worldwide Gross:** `{cwg}`
        """

        complete = await app.send_photo(m.chat.id, photo=cover_url, caption=caption)
        if complete:
            await msg.delete()
        else:
            await app.send_edit(
                "❌ **Failed to get movie metadata. Try again later!**",
                text_type=["mono"],
            )
    except Exception as e:
        await app.error(e)
