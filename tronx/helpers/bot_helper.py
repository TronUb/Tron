def shorten(description, info="anilist.co"):
	ms_g = ""
	if len(description) > 700:
		description = description[0:500] + "..."
		ms_g += (
			f"\n<b>Description</b>: <i>{description}</i> <a href='{info}'>Read More</a>"
		)
	else:
		ms_g += f"\n<b>Description</b>: <i>{description}</i>"
	return (
		ms_g.replace("<br>", "")
		.replace("</br>", "")
		.replace("<i>", "")
		.replace("</i>", "")
	)




def sec(milliseconds: int) -> str:
	"""Inputs time in milliseconds, to get beautified time,
	as string"""
	seconds, milliseconds = divmod(int(milliseconds), 1000)
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	tmp = (
		((str(days) + " Days, ") if days else "")
		+ ((str(hours) + " Hours, ") if hours else "")
		+ ((str(minutes) + " Minutes, ") if minutes else "")
		+ ((str(seconds) + " Seconds, ") if seconds else "")
		+ ((str(milliseconds) + " ms, ") if milliseconds else "")
	)
	return tmp[:-2]




airing_query = """
	query ($id: Int,$search: String) {
		Media (id: $id, type: ANIME,search: $search) {
			id
			episodes
			title {
				romaji
				english
				native
			}
			siteUrl
			nextAiringEpisode {
				airingAt
				timeUntilAiring
				episode
			}
		}
	}
	"""




fav_query = """
query ($id: Int) {
	Media (id: $id, type: ANIME) {
		id
		title {
			romaji
			english
			native
		}
	}
}
"""




anime_query = """
	query ($id: Int,$search: String) {
		Media (id: $id, type: ANIME,search: $search) {
			id
			idMal
			title {
				romaji
				english
				native
			}
			description (asHtml: false)
			startDate{
				year
			}
			episodes
			season
			type
			format
			status
			duration
			siteUrl
			studios{
				nodes{
					name
				}
			}
			trailer{
				id
				site 
				thumbnail
			}
			averageScore
			genres
			bannerImage
		}
	}
"""




character_query = """
	query ($query: String) {
		Character (search: $query) {
			id
			name {
				first
				last
				full
			}
			siteUrl
			favourites
			image {
				large
			}
			description
		}
	}
"""




manga_query = """
query ($id: Int,$search: String) {
	Media (id: $id, type: MANGA,search: $search) {
		id
		title {
			romaji
			english
			native
		}
		description (asHtml: false)
		startDate{
			year
		}
		type
		format
		status
		siteUrl
		averageScore
		genres
		bannerImage
	}
}
"""