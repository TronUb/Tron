import asyncio
import heroku3
import requests
import sys
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from tronx import app, gen





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


async def gen_chlog(m):
	changes = []
	heroku_conn = heroku3.from_key(app.HEROKU_API_KEY)
	heroku_app = heroku_conn.apps()[app.HEROKU_APP_NAME]
	last_updated = int(str((heroku_app.updated_at).date()).replace("-", "")) 
	recent_updates = requests.get("https://api.github.com/repos/TronUb/Tron/events").json()

	for x in recent_updates:
		if x.get("payload").get("commits") is not None and int((x.get("created_at"))[:10].replace("-", "")) > last_updated:
			changes.append(x.get("payload").get("commits")[0].get("message")+"\n")

	if not changes:
		await app.send_edit(m, "Your app is up to date.", text_type=["mono"])
		return -1
	else:
		await app.send_edit(m, "".join(changes))
		return 0

        



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




@app.on_message(gen("update", allow = ["sudo", "channel"]))
async def update_handler(_, m):
	cmd = False
	errtext = "Some problem occurred:\n\n"

	await app.send_edit(m, "Checking for updates, please wait . . .", text_type=["mono"])

	if app.long(m) > 1:
		cmd = m.command

	if await gen_chlog(m) == -1:
		return 

	try:
		repo = Repo()
	except NoSuchPathError as e:
		await app.send_edit(m, f"{errtext}`{e}`")
		return repo.__del__()

	except GitCommandError as e:
		await app.send_edit(m, f"{errtext}`{e}`")
		return repo.__del__()

	except InvalidGitRepositoryError as e:
		repo = Repo.init()
		origin = repo.create_remote("upstream", TRON_REPO)
		origin.fetch()
		repo.create_head("master", origin.refs.master)
		repo.heads.master.set_tracking_branch(origin.refs.master)
		repo.heads.master.checkout(True)
	ACTIVE_BRANCH = repo.active_branch.name
	if ACTIVE_BRANCH != "master":
		await app.send_edit(m, f"**[ UPDATER ]:** You are on [ {ACTIVE_BRANCH} ]\n\nPlease change to `master` branch.`")
		return repo.__del__()

	try:
		repo.create_remote("upstream", TRON_REPO)
	except BaseException:
		pass
	ups_rem = repo.remote("upstream")
	ups_rem.fetch(ACTIVE_BRANCH)
	changelog = False
	if cmd is False:
		if changelog:
			changelog_str = f"**New update is available for [{ACTIVE_BRANCH}]({TRON_REPO}/tree/{ACTIVE_BRANCH}):\n\n[CHANGE LOG]:**\n\n{changelog}"
			if len(changelog_str) > 4096:
				await app.send_edit(m, "Changelog is too big, view the file below to see it.", text_type=["mono"], delme=6)
				file = open("up_output.txt", "w+")
				file.write(changelog_str)
				file.close()
				await app.send_document(
					m.chat.id,
					"up_output.txt",
					caption="**[ STATUS ]:** Do `.update now` to update.",
				)
				remove("up_output.txt")
			else:
				return await app.send_edit(
					m, 
					f"{changelog_str}\n\n[ UPDATE ]: Do `.update now` to update.",
					disable_web_page_preview=True,
				)
		else:
			await app.send_edit(
				m, 
				f"**[ STATUS ]:** Your bot is upto date !\n**[ VERSION ]:** `{app.userbot_version}`\n**[ BRANCH ]:** [{ACTIVE_BRANCH}]({TRON_REPO}/tree/{ACTIVE_BRANCH})",
				disable_web_page_preview=True,
			)
			return repo.__del__()

	if app.HEROKU_API_KEY:
		import heroku3

		heroku = heroku3.from_key(app.HEROKU_API_KEY)
		heroku_app = None
		heroku_applications = heroku.apps()
		if not app.HEROKU_APP_NAME:
			await app.send_edit(m, "Please set up the [ HEROKU_APP_NAME ] variable to be able to update userbot.", text_type=["mono"], delme=4)
			return repo.__del__()

		for apps in heroku_applications:
			if apps.name == app.HEROKU_APP_NAME:
				heroku_app = apps
				break

		if heroku_app is None:
			await app.send_edit(m, "Invalid Heroku credentials for updating userbot.", text_type=["mono"], delme=4)
			return repo.__del__()

		m = await app.send_edit(m, "Userbot update in progress, please wait for few minutes . . .", text_type=["mono"])
		ups_rem.fetch(ACTIVE_BRANCH)
		repo.git.reset("--hard", "FETCH_HEAD")
		heroku_git_url = heroku_app.git_url.replace("https://", "https://api:" + app.HEROKU_API_KEY + "@")

		if "heroku" in repo.remotes:
			remote = repo.remote("heroku")
			remote.set_url(heroku_git_url)
		else:
			remote = repo.create_remote("heroku", heroku_git_url)

		try:
			remote.push(refspec=f"HEAD:refs/heads/{ACTIVE_BRANCH}", force=True)
		except GitCommandError as e:
			app.log.error(e)

		await app.send_edit(m, "Successfully Updated, initialing . . .", text_type=["mono"], delme=8)

	else:
		try:
			ups_rem.pull(ACTIVE_BRANCH)
		except GitCommandError:
			repo.git.reset("--hard", "FETCH_HEAD")
		await install_requirements()
		await app.send_edit(m,"Successfully updated Userbot!\nBot is restarting . . .", text_type=["mono"], delme=8)


