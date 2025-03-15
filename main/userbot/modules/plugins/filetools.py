""" filetools plugin """

import os
import shutil
import zipfile

from pyrogram.types import Message
from main import app


async def unzipfiles(zippath):
    """Unzips a file and extracts it into the ./downloads directory"""
    if not os.path.exists(zippath):
        return None

    folder_name = os.path.splitext(os.path.basename(zippath))[0]
    extract_path = os.path.join("./downloads", folder_name)

    try:
        shutil.unpack_archive(zippath, extract_path)
        os.remove(zippath)  # Remove the zip file after extraction
        return extract_path
    except Exception as e:
        return str(e)


@app.on_cmd(commands="zip", usage="Zip a file or folder.")
async def zip_handler(_, m: Message):
    """Zip handler for filetools plugin"""
    reply = m.reply_to_message
    if not reply or not reply.media:
        return await app.send_edit(
            "Reply to a file or folder to compress.", text_type=["mono"], delme=4
        )

    await app.send_edit("Zipping file...", text_type=["mono"])

    try:
        file_path = await app.download_media(message=reply)

        if not file_path:
            return await app.send_edit(
                "Failed to download file.", text_type=["mono"], delme=4
            )

        zip_path = f"{file_path}.zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isdir(file_path):
                for root, _, files in os.walk(file_path):
                    for file in files:
                        zipf.write(
                            os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file), file_path),
                        )
            else:
                zipf.write(file_path, os.path.basename(file_path))

        await app.send_document(
            m.chat.id,
            zip_path,
            caption=f"Compressed file: `{os.path.basename(zip_path)}`",
        )
        os.remove(zip_path)  # Remove zip after sending

    except Exception as e:
        await app.send_edit(f"Error: {e}", text_type=["mono"], delme=4)


@app.on_cmd(commands="unzip", usage="Unzip a file.")
async def unzip_handler(_, m: Message):
    """Unzip handler for filetools plugin"""
    reply = m.reply_to_message
    if not reply or not reply.media:
        return await app.send_edit(
            "Reply to a file to unzip it.", text_type=["mono"], delme=4
        )

    zip_path = await app.download_media(message=reply)

    if not zip_path.endswith(".zip") or not os.path.exists(zip_path):
        return await app.send_edit("Invalid ZIP file.", text_type=["mono"], delme=4)

    await app.send_edit("Unzipping file...", text_type=["mono"])

    extract_path = await unzipfiles(zip_path)

    if extract_path:
        await app.send_edit(
            f"File unzipped successfully at: `{extract_path}`", text_type=["mono"]
        )
    else:
        await app.send_edit("Failed to unzip file.", text_type=["mono"], delme=4)


@app.on_cmd(commands="new", usage="Create a new file.")
async def createfile_handler(_, m: Message):
    """Create a new file"""
    reply = m.reply_to_message
    command_parts = m.text.split(None, 2)

    if len(command_parts) < 2:
        return await app.send_edit(
            "Provide a filename and optional content.", text_type=["mono"], delme=4
        )

    filename = command_parts[1]
    content = command_parts[2] if len(command_parts) > 2 else ""

    if reply:
        content = reply.text or reply.caption or "None"

    file_path = os.path.join("./downloads", filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        await app.send_document(
            m.chat.id, file_path, caption=f"File created: `{filename}`"
        )
    except Exception as e:
        await app.send_edit(f"Error: {e}", text_type=["mono"], delme=4)
