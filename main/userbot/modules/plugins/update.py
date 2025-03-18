import re
import asyncio

import datetime
from typing import List, Optional

from git import Repo
from git.exc import (
    GitCommandError,
    InvalidGitRepositoryError,
    NoSuchPathError
)

from main import app, gen
from main.core.enums import UserType


TRON_REPO = app.UPSTREAM_REPO

async def gen_chlog():
    """Generate and send changelog from GitHub repository updates."""
    try:
        # Ensure herokuApp.updated_at is valid
        if not hasattr(app, "herokuApp") or not app.herokuApp.updated_at:
            return await app.send_edit(
                "Heroku app update timestamp not found.", text_type=["mono"]
            )

        # Convert `updated_at` timestamp to integer
        try:
            last_updated = int(
                datetime.datetime.strptime(
                    str(app.herokuApp.updated_at), "%Y-%m-%d %H:%M:%S"
                ).strftime("%Y%m%d%H%M%S")
            )
        except ValueError:
            return await app.send_edit(
                "Error parsing last update timestamp.", text_type=["mono"]
            )

        # Fetch GitHub events
        response = await app.fetch_url(
            "https://api.github.com/repos/TronUb/Tron/events"
        )

        if not response or response.get("status") != 200:
            return await app.send_edit(
                "Failed to fetch GitHub updates.", text_type=["mono"]
            )

        updates = response.get("data", [])

        changes: List[str] = []
        for event in updates:
            if event.get("payload", {}).get("commits"):
                created_at = event.get("created_at", "")
                try:
                    event_timestamp = int(
                        datetime.datetime.strptime(
                            created_at, "%Y-%m-%dT%H:%M:%SZ"
                        ).strftime("%Y%m%d%H%M%S")
                    )
                    if event_timestamp > last_updated:
                        commit_message = event["payload"]["commits"][0].get(
                            "message", "No message"
                        )
                        changes.append(f"- {commit_message}\n")
                except ValueError:
                    continue  # Ignore if timestamp conversion fails

        # No updates found
        if not changes:
            await app.send_edit("Your app is up-to-date.", text_type=["mono"])
            return -1

        changelog = "".join(changes)

        # Handle Telegram's message limit
        if len(changelog) > 4096:
            await app.create_file("changelog.txt", changelog, send=True)
            return 0
        else:
            await app.send_edit(changelog)
            return 1

    except Exception as e:
        await log_error(f"Changelog Error: {str(e)}")
        return -1


async def install_requirements():
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@app.on_cmd(
    commands="update",
    usage="Update your userbot to the latest version.",
    disable_for=UserType.SUDO
)
async def update_handler(_, m):
    try:
        branch = "master"
        remote = "upstream"

        cmd = m.text.split()

        errtext = "Some problem occurred:\n\n"
        await app.send_edit("Checking for updates, please wait . . .", text_type=["mono"])

        if len(cmd) == 1:
            return await gen_chlog()
        elif len(cmd) > 1:
            if cmd[1] != "now":
                return await app.send_edit("type 'now' after update command to confirm update", text_type=["mono"], delme=3)

        try:
            repo = Repo()
        except NoSuchPathError as e:
            await app.send_edit(f"{errtext}:\n\n`{e}`")
            return repo.__del__()

        except GitCommandError as e:
            await app.send_edit(f"{errtext}:\n\n`{e}`")
            return repo.__del__()

        except InvalidGitRepositoryError as e:
            repo = Repo.init()
            # create remote
            try:
                # check if remote exists
                origin = getattr(repo.remotes, remote)
            except AttributeError:
                # else create one
                origin = repo.create_remote(remote, TRON_REPO)

            origin.fetch()

            try:
                remote_ref = getattr(origin.refs, branch)
            except AttributeError:
                return await app.send_edit(f"No branch {branch} found !", text_type=["mono"], delme=3)

            repo.create_head(branch, remote_ref)
            head = getattr(repo.heads, branch)
            head.set_tracking_branch(remote_ref)
            head.checkout(True)

        ACTIVE_BRANCH = repo.active_branch.name
        await app.send_edit(f"Updating userbot to {ACTIVE_BRANCH} branch . . .", text_type=["mono"])

        upstream = repo.remote(remote)
        upstream.fetch(ACTIVE_BRANCH)

        if app.herokuApp:
            await app.send_edit("Found update, updating . . .", text_type=["mono"])
            repo.git.reset("--hard", "FETCH_HEAD")
            heroku_git_url = app.herokuApp.git_url.replace("https://", "https://api:" + app.HEROKU_API_KEY + "@")

            if "heroku" in repo.remotes:
                remote = repo.remote("heroku")
                remote.set_url(heroku_git_url)
            else:
                remote = repo.create_remote("heroku", heroku_git_url)

            try:
                remote.push(refspec=f"HEAD:refs/heads/{ACTIVE_BRANCH}", force=True)
            except GitCommandError as e:
                print(e)
                return await app.send_edit("Couldn't update userbot . . .", text_type=["mono"], delme=3)

            await app.send_edit("Successfully Updated, initialing . . .", text_type=["mono"], delme=5)

        else:
            try:
                upstream.pull(ACTIVE_BRANCH)
            except GitCommandError:
                repo.git.reset("--hard", "FETCH_HEAD")

            await install_requirements()
            await app.send_edit("Successfully updated Userbot!\nBot is restarting . . .", text_type=["mono"], delme=5)
    except Exception as e:
        await log_error(e)
