from bs4 import BeautifulSoup as _soup
from urllib.parse import quote
import requests, json

from . import errors

SEARCH_URL = "http://nhentai.net/search?q={}&page={}"
IMAGE_URL = "https://i.nhentai.net/galleries/{}/{}"
DOUJIN_URL = "https://nhentai.net/g/{}"

session = requests.Session()

class Doujinshi():
	"""
	.name = primary/english name
	.jname = secondary/non english name
	.tags = a list of numerical tags
	.magic = magic number/id
	.cover = cover(thumbnail)
	.gid = /galleries/ id for page lookup
	.pages = number of pages
	"""
	def __init__(self, arg):
		self._images = []
		self.fetched = False
		if type(arg) is int:
			self.init_from_id(arg)
		else:
			self.init_from_div(arg)

	def init_from_div(self, res):
		self.name = res.div.text
		self.magic = int(res.a['href'][3:-1:])
		self._set_cover(res)
			
	def init_from_id(self, magic):
		res = _get(DOUJIN_URL.format(magic))
		if res(class_='container error'):
			raise errors.DoujinshiNotFound()
		self.magic = magic
		self._set_cover(res.find(id='cover'))
		self.fetch(res) # since res was already requested
		self.name = res.find(id='info').h1.text
		
	def _set_cover(self, res):
		try:
			self.cover = res.img['data-src']
		except:
			self.cover = 'https:' + res.img['src']
		self.gid = int(self.cover.rsplit('/', 2)[-2])
	
	def fetch(self, res=None):
		if not res:
			res = _get(DOUJIN_URL.format(self.magic))
		# add pages
		for url in res(class_='gallerythumb'):
			url = url.noscript.img['src'].rsplit('/', 1)[-1]
			self._images.append(IMAGE_URL.format(self.gid, url.replace('t', '')))
		# set info (jname, pages, tags)
		res = res.find(id='info')
		self.jname = res.h2.text if res.h2 else None
		self.pages = len(self._images)
		self.tags = []
		for tag in res('a', class_='tag'):
			tag = tag.text.rsplit(' ', 1)[:-1:]
			self.tags.append(' '.join(tag))
		self.fetched = True
		
	def __getitem__(self, key):
		if not self.fetched:
			self.fetch()
		return self._images[key]
		
	def __getattr__(self, key):
		if key == 'jname' or key == 'pages' or key == 'tags':
			self.fetch()
			return getattr(self, key)
		raise AttributeError
		
	def __repr__(self):
		return 'doujin:' + str(self.magic)
		
def _get(endpoint:str):
	return _soup(session.get(endpoint).text, 'lxml')
	
def search(query:str, page:int=1):
	res = _get(SEARCH_URL.format(quote(query), page))
	for div in res(class_='gallery'):
		yield Doujinshi(div)