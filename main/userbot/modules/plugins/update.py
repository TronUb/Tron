import asyncio
import heroku3
import requests
import sys
import re
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from main import app, gen





app.CMD_HELP.update(
    {"update" : (
        "update",
        {
        "update" : "To check if new update is available or not.",
        "update [ now ]" : "To update userbot to latest version."
        }
        )
    }
)




TRON_REPO = app.UPSTREAM_REPO


async def gen_chlog():
    changes = []
    last_updated = int(re.sub(r"[- + : \s]", "", str(app.heroku_app().updated_at))[:14])
    recent_updates = app.GetRequest("https://api.github.com/repos/TronUb/Tron/events")

    for x in recent_updates:
        if x.get("payload").get("commits") is not None and int(x.get("created_at").replace("-", "").replace(":", "").replace("T", "").replace("Z", "")) > last_updated:
            changes.append(x.get("payload").get("commits")[0].get("message")+"\n")

    if not changes:
        await app.send_edit("Your app is up-to-date.", text_type=["mono"])
        return -1
    else:
        if len("".join(changes)) > 4096:
            await app.create_file("changelog.txt", "".join(changes), send=True)
            return 0
        else:
            await app.send_edit("".join(changes))
            return 1

        



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




@app.on_message(gen("update", exclude = ["sudo", "channel"]))
async def update_handler(_, m):
    try:
        branch = "master"
        cmd = m.text.split()
        args = m.text.split(None, 1)
        errtext = "Some problem occurred:\n\n"
        await app.send_edit("Checking for updates, please wait . . .", text_type=["mono"])

        if len(cmd)  == 1:
            return await gen_chlog()
        elif len(cmd) > 1:
            if args[1] != "now":
                return app.send_edit("type 'now' after update command to confirm update", text_type=["mono"], delme=3)
        elif len(cmd) > 2:
            if args[1] == "now":
                branch = m.text.split(None, 2)[2]

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
            origin = repo.create_remote("upstream", TRON_REPO)
            origin.fetch()

            try:
                remote_ref = getattr(origin.refs, branch)
                head = getattr(repo.heads, branch)
            except AttributeError:
                return await app.send_edit(f"No branch {branch} found !", text_type=["mono"], delme=3)

            repo.create_head(branch, remote_ref)
            head.set_tracking_branch(remote_ref)
            head.checkout(True)
        ACTIVE_BRANCH = repo.active_branch.name
        await app.send_edit(f"Updating userbot to {ACTIVE_BRANCH} branch . . .", text_type=["mono"])

        try:
            repo.create_remote("upstream", TRON_REPO)
        except BaseException:
            pass

        ups_rem = repo.remote("upstream")
        ups_rem.fetch(ACTIVE_BRANCH)

        if app.heroku_app():
            await app.send_edit("Found update, updating . . .", text_type=["mono"])
            repo.git.reset("--hard", "FETCH_HEAD")
            heroku_git_url = app.heroku_app().git_url.replace("https://", "https://api:" + app.HEROKU_API_KEY + "@")

            if "heroku" in repo.remotes:
                remote = repo.remote("heroku")
                remote.set_url(heroku_git_url)
            else:
                remote = repo.create_remote("heroku", heroku_git_url)

            try:
                remote.push(refspec=f"HEAD:refs/heads/{ACTIVE_BRANCH}", force=True)
            except GitCommandError as e:
                print(e)
                app.log.error(e)
                return await app.send_edit("Failed to updste userbot . . .", text_type=["mono"], delme=3)

            await app.send_edit("Successfully Updated, initialing . . .", text_type=["mono"], delme=5)

        else:
            try:
                ups_rem.pull(ACTIVE_BRANCH)
            except GitCommandError:
                repo.git.reset("--hard", "FETCH_HEAD")

            await install_requirements()
            await app.send_edit("Successfully updated Userbot!\nBot is restarting . . .", text_type=["mono"], delme=8)
    except Exception as e:
        await app.error(e)

