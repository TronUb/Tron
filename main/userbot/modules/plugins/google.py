import os
import random
import shutil
import requests

from bs4 import BeautifulSoup
from bing_image_downloader import downloader as bing_downloader
from pyrogram.types import Message

from main import app, gen

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
}


@app.on_cmd(commands="sauce", usage="Get information of an image.")
async def imagesauce_handler(_, m: Message):
    """Image sauce handler for google plugin"""
    try:
        reply = m.reply_to_message
        if not reply or not (reply.photo or reply.animation):
            return await app.send_edit(
                "Reply to a photo or animation.", text_type=["mono"], delme=4
            )

        await app.send_edit("⏳ • Processing image...")

        # Determine file type and download
        media = reply.photo or reply.animation
        ext = "png" if reply.photo else "gif"
        savename = f"photo_{media.file_unique_id}.{ext}"
        file_path = f"./downloads/{savename}"

        await app.download_media(reply, file_name=file_path)

        # Google reverse image search
        search_url = "http://www.google.co.id/searchbyimage/upload"
        with open(file_path, "rb") as image_file:
            response = requests.post(
                search_url,
                files={"encoded_image": (savename, image_file)},
                headers=headers,
            )

        # Parse search results
        text = requests.get(response.url, headers=headers).text
        soup = BeautifulSoup(text, "html.parser")
        result_div = soup.find("div", class_="r5a77d")

        if result_div:
            text_results = result_div.text
            await app.send_edit(
                f"**Results:** [{text_results}]({response.url})",
                disable_web_page_preview=True,
            )
        else:
            await app.send_edit("No results found.", text_type=["mono"], delme=4)

    except Exception as e:
        await app.error(e)


@app.on_cmd(
    commands="pic",
    usage="Get images from @pic"
)
async def yandeximages_handler(_, m: Message):
    """Yandex image handler for google plugin"""
    if len(m.command) < 2:
        return await app.send_edit("Usage: `.pic <query>`", delme=4)

    try:
        await app.send_edit("Getting image . . .", text_type=["mono"])
        query = m.text.split(None, 1)[1]

        result = await app.get_inline_bot_results("@pic", query)
        if not result.results:
            return await app.send_edit("No images found!", text_type=["mono"], delme=4)

        random_result = random.choice(result.results)
        await m.delete()
        await app.send_inline_bot_result(
            m.chat.id, query_id=result.query_id, result_id=random_result.id
        )

    except Exception as e:
        await app.error(e)


@app.on_cmd(commands="img", usage="Get images from Google.")
async def imagesearch_handler(_, m: Message):
    """Image search handler for Google plugin"""
    if len(m.command) < 2:
        return await app.send_edit(
            "Please provide a search query.", text_type=["mono"], delme=4
        )

    # Handle custom image limits
    try:
        if len(m.command) > 2 and m.command[1].isdigit():
            limit = int(m.command[1])
            query = " ".join(m.command[2:])
        else:
            limit = 3  # Default limit
            query = " ".join(m.command[1:])
    except ValueError:
        return await app.send_edit(
            "Invalid command format.", text_type=["mono"], delme=4
        )

    try:
        await app.send_edit(f"**Getting images for:** `{query}`")

        # Download images using Bing API
        bing_downloader.download(
            query,
            limit=limit,
            output_dir="images",
            adult_filter_off=True,
            force_replace=False,
            timeout=60,
            verbose=False,
        )

        img_dir = f"./images/{query}"
        if os.path.exists(img_dir) and os.listdir(img_dir):
            for img in os.listdir(img_dir):
                await app.send_photo(m.chat.id, f"{img_dir}/{img}")
        else:
            await app.send_edit("No images found!", text_type=["mono"], delme=4)

        # Cleanup
        shutil.rmtree("./images", ignore_errors=True)
        await m.delete()

    except Exception as e:
        await app.error(e)
