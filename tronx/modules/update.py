import asyncio
import sys
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from tronx import (
  	app, 
	CMD_HELP,
	Config,
)

from tronx.helpers import (
	get_arg,
	send_edit,
	gen,
	long,
)




CMD_HELP.update(
	{"update" : (
		"update",
		{
		"update" : "Update your userbot to latest version."
		}
		)
	}
)




UPSTREAM_REPO_URL = "https://github.com/beastzx18/tron"

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)




async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "On %d/%m/%y at %H:%M:%S"
    for c in repo.iter_commits(diff):
        ch_log += f"**#{c.count()}** : {c.committed_datetime.strftime(d_form)} : [{c.summary}]({UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}) by `{c.author}`\n"
    return ch_log




async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)




@app.on_message(gen("update"))
async def upstream(_, m):
	await send_edit(m, "Checking for updates, please wait . . .", mono=True)
	if long(m) > 1:
		cmd = m.command
	else:
		cmd = False
	off_repo = UPSTREAM_REPO_URL
	try:
		txt = "`Oops . . . Updater cannot continue due to "
		txt += "some problems occured`\n\n**LOGTRACE:**\n"
		repo = Repo()
	except NoSuchPathError as error:
		await send_edit(m, f"{txt}\n`directory {error} is not found`")
		repo.__del__()
		return
	except GitCommandError as error:
		await send_edit(m, f"{txt}\n`Early failure! {error}`")
		repo.__del__()
		return
	except InvalidGitRepositoryError as error:
		if cmd and cmd[1] != "now":
			pass
		repo = Repo.init()
		origin = repo.create_remote("upstream", off_repo)
		origin.fetch()
		repo.create_head("master", origin.refs.master)
		repo.heads.master.set_tracking_branch(origin.refs.master)
		repo.heads.master.checkout(True)
	ac_br = repo.active_branch.name
	if ac_br != "master":
		await send_edit(
			m, 
			f"**[UPDATER]:**` You are on ({ac_br})\n Please change to master branch.`"
		)
		repo.__del__()
		return
	try:
		repo.create_remote("upstream", off_repo)
	except BaseException:
		pass
	ups_rem = repo.remote("upstream")
	ups_rem.fetch(ac_br)
	changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
	if cmd is False:
		if changelog:
			changelog_str = f"**New UPDATE available for [[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br}):\n\nCHANGELOG**\n\n{changelog}"
			if len(changelog_str) > 4096:
				await send_edit(m, "`Changelog is too big, view the file to see it.`")
				file = open("output.txt", "w+")
				file.write(changelog_str)
				file.close()
				await app.send_document(
					m.chat.id,
					"output.txt",
					caption="Do `.update now` to update.",
					reply_to_message_id=send_message_id,
				)
				remove("output.txt")
			else:
				return await send_edit(
					m, 
					f"{changelog_str}\n\nDo `.update now` to update.",
					disable_web_page_preview=True,
				)
		else:
			await send_edit(
				m, 
				f"\n`Your BOT is`  **up-to-date**  `with`  **[[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br})**\n",
				disable_web_page_preview=True,
			)
			repo.__del__()
			return
	if Config.HEROKU_API_KEY is not None:
		import heroku3

		heroku = heroku3.from_key(HEROKU_API_KEY)
		heroku_app = None
		heroku_applications = heroku.apps()
		if not Config.HEROKU_APP_NAME:
			await send_edit(
				m, 
                "`Please set up the HEROKU_APP_NAME variable to be able to update userbot.`"
			)
			repo.__del__()
			return
		for app in heroku_applications:
			if app.name == Config.HEROKU_APP_NAME:
				heroku_app = app
				break
		if heroku_app is None:
			await send_edit(
				m, 
				f"{txt}\n`Invalid Heroku credentials for updating userbot dyno.`"
			)
			repo.__del__()
			return
		await send_edit(
			m, 
			"`Userbot dyno build in progress, please wait for it to complete.`"
		)
		ups_rem.fetch(ac_br)
		repo.git.reset("--hard", "FETCH_HEAD")
		heroku_git_url = heroku_app.git_url.replace(
			"https://", "https://api:" + HEROKU_API_KEY + "@"
		)
		if "heroku" in repo.remotes:
			remote = repo.remote("heroku")
			remote.set_url(heroku_git_url)
		else:
			remote = repo.create_remote("heroku", heroku_git_url)
		try:
			remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
		except GitCommandError as error:
			pass
		await send_edit(m, "`Successfully Updated!\nRestarting, please wait...`")
	else:
		try:
			ups_rem.pull(ac_br)
		except GitCommandError:
			repo.git.reset("--hard", "FETCH_HEAD")
		await updateme_requirements()
		await send_edit(
			m,
			"`Successfully Updated!\nBot is restarting... Wait for a second!`",
		)

		args = [sys.executable, "./resources/startup/deploy.sh"]
		execle(sys.executable, *args, environ)
		return
