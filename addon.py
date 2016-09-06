from xbmcswift2 import Plugin
from resources.lib.series_cravings import SeriesCravings

try:
    import urlresolver
except ImportError:
    import dummy_urlresolver as urlresolver

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


def generate_items(elements, route, is_playable=False):
	return [{"label" : element["name"], "path": plugin.url_for(route, path=element["path"]), "is_playable" : is_playable} for element in elements]

@plugin.route("/top_shows")
def top_shows():
    shows = SeriesCravings().top_shows()
    plugin.set_content("tvshows")
    return generate_items(shows, route="show")

@plugin.route("/by_sections")
def by_sections():
	sections = SeriesCravings().show_sections()
	return [{"label" : section, "path": plugin.url_for("by_section", section=section)} for section in sections]

@plugin.cached()
def all_shows():
	return SeriesCravings().shows()

@plugin.route("/by_section/<section>")
def by_section(section):
    shows = all_shows()[section]
    plugin.set_content("tvshows")
    return generate_items(shows, route="show")

@plugin.route("/show/<path>")
def show(path):
	seasons = SeriesCravings().show_episodes(path).keys()
	seasons.reverse()
	return [{"label" : season, "path": plugin.url_for("show_episodes", season=season, show_path=path)} for season in seasons]

@plugin.route("/show/<show_path>/season/<season>")
def show_episodes(show_path, season):
    plugin.set_content("episodes")
    episodes = SeriesCravings().show_episodes(show_path)[season]
    return generate_items(episodes, route="episode", is_playable=True)

@plugin.route("/episode/<path>")
def episode(path):
    streams = SeriesCravings().episode_streams(path)
    stream = urlresolver.choose_source([urlresolver.HostedMediaFile(url=value, title=key) for (key, value) in streams.iteritems()])
    plugin.log.error(stream)
    plugin.set_resolved_url(stream.get_url())

if __name__ == '__main__':
    plugin.run()
