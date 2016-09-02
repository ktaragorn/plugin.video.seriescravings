import parsedom as common
import urllib2
import string
from xbmcswift2 import Plugin

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
		return series_craving_suffixed_page("show_path")

	def tv_show_episode_path(self, episode_path):
		return series_craving_suffixed_page("episode_path")

	# parsing for sections seems hard, gonna hard code
	def show_sections(self):
		return ["0-9"] + list(string.uppercase)

	def generate_shows_hash(self,names, urls):
		path_names = [self.extract_path_name(url) for url in urls]
		return [{"name": name, "path_name": path_name} for (name, path_name) in zip(names, path_names)]

	def extract_path_name(self, url):
		return url.replace("http://series-cravings.me/", "")


@plugin.cached()
def series_craving_suffixed_page(suffix):
	return str(urllib2.urlopen("http://series-cravings.me/" + suffix).read())