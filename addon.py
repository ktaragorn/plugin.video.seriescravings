from xbmcswift2 import Plugin
from resources.lib.series_cravings import SeriesCravings

plugin = Plugin()
@plugin.route('/')
def index():
    items = [
    {
        'label': "Favorites (Not Implemented)",
        'path': 'http://s3.amazonaws.com/KA-youtube-converted/JwO_25S_eWE.mp4/JwO_25S_eWE.mp4',
    },
    {
        'label': "A-Z",
        'path': plugin.url_for("by_sections"),
    },
    {
        'label': "Search (Not Implemented)",
        'path': 'http://s3.amazonaws.com/KA-youtube-converted/JwO_25S_eWE.mp4/JwO_25S_eWE.mp4',
    },
    {
        'label': "Weekly Top 10 Shows",
        'path': plugin.url_for("top_shows")
    },
    {
        'label': "Schedule",
        'path': 'http://s3.amazonaws.com/KA-youtube-converted/JwO_25S_eWE.mp4/JwO_25S_eWE.mp4',
    }
    ]
    return items


def items_for_shows(shows):
	return [{"label" : show["name"], "path": plugin.url_for("show", name=show["path_name"])} for show in shows]

@plugin.route("/top_shows")
def top_shows():
	shows = SeriesCravings().top_shows()
	return items_for_shows(shows)

@plugin.route("/by_sections")
def by_sections():
	sections = SeriesCravings().show_sections()
	return [{"label" : section, "path": plugin.url_for("by_section", section=section)} for section in sections]

@plugin.route("/by_section/<section>")
def by_section(section):
	shows = SeriesCravings().shows()[section]
	return items_for_shows(shows)

@plugin.route("/show/<name>")
def show(name):
	return [{"label": name}]

if __name__ == '__main__':
    plugin.run()
