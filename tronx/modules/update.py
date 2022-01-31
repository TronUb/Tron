import asyncio
import sys
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from tronx import app

from tronx.helpers import (
	gen,
)




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


async def gen_chlog(repo, diff):
	ch_log = ""
	dateform = "On %d/%m/%y at %H:%M:%S"
	for data in repo.iter_commits(diff):
		ch_log += f"**#{data.count()}** : {data.committed_datetime.strftime(dateform)} : [{data.summary}]({TRON_REPO.rstrip('/')}/commit/{c}) by `{data.author}`\n"
	return ch_log




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




@app.on_message(gen("update"))
async def update_ub(_, m):
	cmd = False
	errtext = "Some problem occurred:\n\n"

	await app.send_edit(m, "Checking for updates, please wait . . .", mono=True)

	if app.long(m) > 1:
		cmd = m.command

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
	changelog = await gen_chlog(repo, f"{ACTIVE_BRANCH}")
	if cmd is False:
		if changelog:
			changelog_str = f"**New update is available for [{ACTIVE_BRANCH}]({TRON_REPO}/tree/{ac_br}):\n\n[CHANGE LOG]:**\n\n{changelog}"
			if len(changelog_str) > 4096:
				await app.send_edit(m, "Changelog is too big, view the file below to see it.", mono=True, delme=6)
				file = open("output.txt", "w+")
				file.write(changelog_str)
				file.close()
				await app.send_document(
					m.chat.id,
					"up_output.txt",
					caption="[ STATUS ]: Do `.update now` to update.",
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

	if app.HEROKU_API_KEY is not None:
		import heroku3

		heroku = heroku3.from_key(app.HEROKU_API_KEY)
		heroku_app = None
		heroku_applications = heroku.apps()
		if not app.HEROKU_APP_NAME:
			await app.send_edit(
				m, 
				"`Please set up the [ HEROKU_APP_NAME ] variable to be able to update userbot.`"
			)
			return repo.__del__()

		for bars in heroku_applications:
			if bars.name == app.HEROKU_APP_NAME:
				heroku_app = bars
				break
		if heroku_app is None:
			await app.send_edit(
				m, 
				f"Invalid Heroku credentials for updating userbot."
			)
			return repo.__del__()

		msg = await app.send_edit(
			m, 
			"`Userbot update in progress, please wait for few minutes . . .`"
		)
		ups_rem.fetch(ACTIVE_BRANCH)
		repo.git.reset("--hard", "FETCH_HEAD")
		heroku_git_url = heroku_app.git_url.replace(
			"https://", "https://api:" + app.HEROKU_API_KEY + "@"
		)
		if "heroku" in repo.remotes:
			remote = repo.remote("heroku")
			remote.set_url(heroku_git_url)
		else:
			remote = repo.create_remote("heroku", heroku_git_url)
		try:
			remote.push(refspec=f"HEAD:refs/heads/{ACTIVE_BRANCH}", force=True)
		except GitCommandError as error:
			pass
		try:
			await msg.edit("Successfully Updated!\nRestarting, Please wait . . .", mono=True)
		except Exception:
			await app.send_edit(m, "Successfully Updated!\nRestarting, please wait . . .", mono=True, delme=5)
	else:
		try:
			ups_rem.pull(ACTIVE_BRANCH)
		except GitCommandError:
			repo.git.reset("--hard", "FETCH_HEAD")
		await updateme_requirements()
		await app.send_edit(
			m,
			"Successfully updated Userbot!\nBot is restarting . . .", 
			mono=True, 
			delme=8
		)
		await install_requirements()
