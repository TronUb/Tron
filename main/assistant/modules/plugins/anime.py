import sys
import traceback
import uuid

from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InputMediaPhoto,
)
from pyrogram import filters
from main.userbot.client import app


@app.bot.on_message(filters.command("anime") & filters.user(app.id), group=-1)
async def bot_anime_handler(_, m: Message):
    """Fetches anime details and displays MAL link with an inline characters button"""
    try:
        if m.from_user.id != app.id:
            return

        text = m.text
        try:
            cmd = text.split(None, 1)[1]
        except IndexError:
            cmd = None

        if not cmd:
            return await app.bot.send_message(
                m.chat.id, "Give me some text (anime name) to search . . ."
            )

        msg = await app.bot.send_message(m.chat.id, "Fetching anime details...")
        anime_data = await app.get_anime_details_jikan(cmd)
        anime_details = anime_data.get("anime_details")
        anime_characters = anime_data.get("characters")

        if "error" in anime_data:
            return await msg.edit(anime_data["error"])

        details_list = [f"**{anime_details.get('title')}**\n"]

        fields = {
            "🎌 **Japanese Title:**": anime_details.get("japanese_title"),
            "📖 **Synonyms:**": (
                ", ".join(anime_details.get("synonyms"))
                if anime_details.get("synonyms")
                else None
            ),
            "📺 **Episodes:**": anime_details.get("episodes"),
            "⭐ **Score:**": anime_details.get("score"),
            "🏆 **Rank:**": anime_details.get("rank"),
            "🔥 **Popularity:**": anime_details.get("popularity"),
            "📜 **Status:**": anime_details.get("status"),
            "🔗 **Source:**": anime_details.get("source"),
            "🎭 **Genres:**": (
                ", ".join(anime_details.get("genres"))
                if anime_details.get("genres")
                else None
            ),
            "🌟 **Themes:**": (
                ", ".join(anime_details.get("themes"))
                if anime_details.get("themes")
                else None
            ),
            "🏛️ **Demographics:**": (
                ", ".join(anime_details.get("demographics"))
                if anime_details.get("demographics")
                else None
            ),
            "📝 **Synopsis:**": (
                (anime_details.get("synopsis")[:300] + "...")
                if anime_details.get("synopsis")
                else None
            ),
            "⏳ **Aired:**": anime_details.get("aired"),
            "⏱️ **Duration:**": anime_details.get("duration"),
            "🔞 **Rating:**": anime_details.get("rating"),
            "❤️ **Favorites:**": anime_details.get("favorites"),
        }

        for key, value in fields.items():
            if value:
                details_list.append(f"{key} {value}\n")

        details_text = "".join(details_list)

        # Inline buttons
        buttons = []
        if anime_details.get("mal_url"):
            buttons.append(
                [
                    InlineKeyboardButton(
                        "📌 View on MyAnimeList", url=anime_details.get("mal_url")
                    )
                ]
            )

        if anime_characters:
            buttons.append(
                [
                    InlineKeyboardButton(
                        "🎭 Characters",
                        callback_data=f"show_chars:{anime_details.get('mal_id')}:0",
                    )
                ]
            )

        keyboard = InlineKeyboardMarkup(buttons) if buttons else None

        await app.bot.send_photo(
            m.chat.id,
            anime_details.get("image", ""),
            caption=details_text,
            reply_markup=keyboard,
        )

        await msg.delete()

    except Exception as e:
        error_text = f"**Error:**\n```{traceback.format_exc()}```"
        await app.bot.send_message(m.chat.id, error_text)


@app.bot.on_callback_query(filters.regex("^show_chars:"))
async def show_characters_callback(_, query: CallbackQuery):
    """Handles the callback query to show paginated characters"""
    try:
        data = query.data.split(":")  # Extract callback data
        mal_id = data[1]
        page = int(data[2])  # Get current page

        # Refetch anime details and characters using mal_id
        anime_data = await app.get_anime_details_jikan(mal_id=mal_id)
        anime_characters = anime_data.get("characters", [])

        if not anime_characters:
            return await query.answer("Character data not found.", show_alert=True)

        per_page = 10  # Number of characters per page
        start_idx = page * per_page
        end_idx = start_idx + per_page
        char_subset = anime_characters[start_idx:end_idx]

        char_text = "**Characters:**\n" + "\n".join(
            [
                f"- [{char['name']}]({char['mal_url']}) ({char['role']})"
                for char in char_subset
            ]
        )

        # Pagination buttons
        buttons = []
        if start_idx > 0:  # Previous button only if not on first page
            buttons.append(
                InlineKeyboardButton(
                    "⬅️ Previous", callback_data=f"show_chars:{mal_id}:{page - 1}"
                )
            )
        if end_idx < len(
            anime_characters
        ):  # Next button only if more characters remain
            buttons.append(
                InlineKeyboardButton(
                    "➡️ Next", callback_data=f"show_chars:{mal_id}:{page + 1}"
                )
            )

        buttons.append(
            InlineKeyboardButton("🔙 Back", callback_data=f"back_to_anime:{mal_id}")
        )

        await query.message.edit_text(
            char_text,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([buttons]),
        )
    except Exception as e:
        print(e)
        await query.answer("Error loading characters.", show_alert=True)


@app.bot.on_callback_query(filters.regex("^back_to_anime:"))
async def back_to_anime_callback(_, query: CallbackQuery):
    """Handles back button to return to full anime details (image + text + buttons)"""
    try:
        mal_id = query.data.split("back_to_anime:", 1)[1]

        # Refetch anime details using mal_id
        anime_data = await app.get_anime_details_jikan(mal_id=mal_id)
        anime_details = anime_data.get("anime_details", {})

        if not anime_details:
            return await query.answer("Anime details not found.", show_alert=True)

        details_list = [f"**{anime_details.get('title')}**\n"]

        fields = {
            "🎌 **Japanese Title:**": anime_details.get("japanese_title"),
            "📖 **Synonyms:**": (
                ", ".join(anime_details.get("synonyms"))
                if anime_details.get("synonyms")
                else None
            ),
            "📺 **Episodes:**": anime_details.get("episodes"),
            "⭐ **Score:**": anime_details.get("score"),
            "🏆 **Rank:**": anime_details.get("rank"),
            "🔥 **Popularity:**": anime_details.get("popularity"),
            "📜 **Status:**": anime_details.get("status"),
            "🔗 **Source:**": anime_details.get("source"),
            "🎭 **Genres:**": (
                ", ".join(anime_details.get("genres"))
                if anime_details.get("genres")
                else None
            ),
            "🌟 **Themes:**": (
                ", ".join(anime_details.get("themes"))
                if anime_details.get("themes")
                else None
            ),
            "🏛️ **Demographics:**": (
                ", ".join(anime_details.get("demographics"))
                if anime_details.get("demographics")
                else None
            ),
            "📝 **Synopsis:**": (
                (anime_details.get("synopsis")[:300] + "...")
                if anime_details.get("synopsis")
                else None
            ),
            "⏳ **Aired:**": anime_details.get("aired"),
            "⏱️ **Duration:**": anime_details.get("duration"),
            "🔞 **Rating:**": anime_details.get("rating"),
            "❤️ **Favorites:**": anime_details.get("favorites"),
        }

        for key, value in fields.items():
            if value:
                details_list.append(f"{key} {value}\n")

        details_text = "".join(details_list)

        # Inline buttons
        buttons = []
        if anime_details.get("mal_url"):
            buttons.append(
                [
                    InlineKeyboardButton(
                        "📌 View on MyAnimeList", url=anime_details.get("mal_url")
                    )
                ]
            )

        if anime_data.get("characters"):
            buttons.append(
                [
                    InlineKeyboardButton(
                        "🎭 Characters", callback_data=f"show_chars:{mal_id}:0"
                    )
                ]
            )

        keyboard = InlineKeyboardMarkup(buttons) if buttons else None

        await query.message.edit_media(
            media=InputMediaPhoto(anime_details.get("image", ""), caption=details_text),
            reply_markup=keyboard,
        )

    except Exception as e:
        await query.answer("Error returning to anime details.", show_alert=True)
