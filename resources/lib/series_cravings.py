import parsedom as common
from xbmcswift2 import Plugin
import urllib2

plugin = Plugin()
class SeriesCravings:
	def top_shows(self):
		section = common.parseDOM(self.tv_shows_page(), "div", attrs={"id" : "secondary"})
		names = common.parseDOM(section, "a")
		urls = common.parseDOM(section, "a", ret="href")
		return self.generate_shows_hash(names, urls)
	def shows(self):
		return {"T": [{"name" : "Test", "path_name": "test"}]}

	# @plugin.cached()
	def tv_shows_page(self):
		return urllib2.urlopen("http://series-cravings.me/tv-show-2").read()

	def generate_shows_hash(self,names, urls):
		path_names = [self.extract_path_name(url) for url in urls]
		return [{"name": name, "path_name": path_name} for (name, path_name) in zip(names, path_names)]

	def extract_path_name(self, url):
		return url.replace("http://series-cravings.me/", "")