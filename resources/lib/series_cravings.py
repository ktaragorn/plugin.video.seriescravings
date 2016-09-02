import parsedom as common
import urllib2
import string
from xbmcswift2 import Plugin

try:
	import urlresolver
except ImportError:
	import dummy_urlresolver as urlresolver

plugin = Plugin()

class SeriesCravings:
	def top_shows(self):
		section = common.parseDOM(self.tv_shows_page(), "div", attrs={"id" : "secondary"})
		names = common.parseDOM(section, "a")
		urls = common.parseDOM(section, "a", ret="href")
		return self.generate_shows_hash(names, urls)
	def shows(self):
		section_headers = self.show_sections()
		section = common.parseDOM(self.tv_shows_page(), "div", attrs={"id" : "primary"})
		shows_by_sections = common.parseDOM(section, "ul")
		# TODO show the annotations too?
		shows_by_sections = [self.generate_shows_hash(common.parseDOM(shows_in_section, "a"), common.parseDOM(shows_in_section, "a", ret="href")) for shows_in_section in shows_by_sections]
		return dict(zip(section_headers, shows_by_sections))

	def tv_shows_page(self):
		return series_craving_suffixed_page("tv-show-2")

	def tv_show_page(self, show_path):
		return series_craving_suffixed_page(show_path)

	def tv_show_episode_path(self, episode_path):
		return series_craving_suffixed_page("test/" + episode_path)

	# parsing for sections seems hard, gonna hard code
	def show_sections(self):
		return ["0-9"] + list(string.uppercase)

	def generate_shows_hash(self, names, urls):
		return self.generate_hash(names, urls, path_extractor=self.extract_show_path)

	def generate_hash(self,names, urls, path_extractor):
		paths = [path_extractor(url) for url in urls]
		return [{"name": name, "path": path} for (name, path) in zip(names, paths)]

	def extract_show_path(self, url):
		return url.replace("http://series-cravings.me/", "")

	def extract_episode_path(self, url):
		return url.replace("http://series-cravings.me/test/", "")

	def show_episodes(self, path):
		seasons = common.parseDOM(self.tv_show_page(path),"div", attrs={"class" : "omsc-toggle-title"})
		seasons_episodes = common.parseDOM(self.tv_show_page(path), "ul", attrs={"class": "b"})
		seasons_episodes = [self.generate_hash(common.parseDOM(episodes_in_season, "a"), common.parseDOM(episodes_in_season, "a", ret="href"), path_extractor=self.extract_episode_path) for episodes_in_season in seasons_episodes]
		return dict(zip(seasons, seasons_episodes))

	def episode_streams(self, path):		# names=/
		page = self.tv_show_episode_path(path)
		names = common.parseDOM(page, "b") # seems hacky but works perfectly
		# urls = common.parseDOM(page, "iframe", ret="src")

		#hacky but works better
		urls = [common.parseDOM(iframe.lower() + "</iframe>", "iframe", ret="src")[0] for iframe in common.parseDOM(page, "b",attrs={"id": "ko"}, ret="data-iframe")]
		urls = [urlresolver.resolve(url) for url in urls]
		return dict(zip(names, urls))


@plugin.cached()
def series_craving_suffixed_page(suffix):
	return str(urllib2.urlopen("http://series-cravings.me/" + suffix).read())