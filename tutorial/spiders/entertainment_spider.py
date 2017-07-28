import scrapy
import re

# Constants
def definition():
	global ONLINE_KHABAR
	ONLINE_KHABAR = 1

	global EKANTIPUR
	EKANTIPUR = 2

	global HAMRO_KURA
	HAMRO_KURA = 3

	global UJYAALO_ONLINE
	UJYAALO_ONLINE = 4

	global TOP_NEPAL_NEWS
	TOP_NEPAL_NEWS = 5

def get_source(link):		

	"""
	Function to return the respective website by matching the url regex
	Regex are supplied in such a way to match the required url
	In some cases the regex also filters data from 2017
	"""
	if re.match("http:\/\/www.onlinekhabar.com\/2017\/.*[0-9]/$", link):
		return ONLINE_KHABAR
	elif re.match("http://.*.ekantipur.com/news/2017.*.html$", link):
		return EKANTIPUR
	elif re.match("http://hamrakura.com/news-details/.*./2017.*$", link):
		return HAMRO_KURA
	elif re.match("http://ujyaaloonline.com/news/.*[0-9]/.*/$", link):
		return UJYAALO_ONLINE
	elif re.match('http://topnepalnews.com/entertainment/.*[0-9]$', link):
		return TOP_NEPAL_NEWS
	else: 
		return None

def get_urls():
	urls = ['http://www.ekantipur.com/nep/entertainment']

	for pages in xrange(1, 70): # total pages 511
		urls = urls + ['http://www.onlinekhabar.com/content/ent-news/page' + str(pages) + '/']

	for pages in xrange(1, 10): # total pages 48
		urls = urls + ['http://hamrakura.com/category.php?_Id=6&p=' + str(pages)]

	for pages in xrange(1, 11): # total pages 56
		urls = urls + ['http://ujyaaloonline.com/news/category/16/art/page/' + str(pages) + '/']

	for pages in range(0, 50, 25): # total pages 175
		urls = urls + ['http://topnepalnews.com/entertainment?per_page=' + str(pages)]	

	return urls

def clean_txt(raw_input):
	# Function to remove html tags and extra special characters
	cleanr = re.compile('<.*?>')
  	cleantext = re.sub(cleanr, '', raw_input)
  	cleantext = re.sub('["\',]', '', cleantext.strip())
  	return cleantext

class EntertainmentSpider(scrapy.Spider):
	definition()
	name = "ent_all"
	start_urls = []

	start_urls = start_urls + get_urls()

	def parse(self, response):
		for link in response.css('a::attr(href)').extract():
			
			self.log("Links__ %s" % link)

			source1 = get_source(link)
			
			# Parse urls according to the origin websites
			if source1 == ONLINE_KHABAR:
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page_onlinekhabar)
			elif source1 == EKANTIPUR:
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page_ekantipur)
			elif source1 == HAMRO_KURA:
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page_hamrakura)
			elif source1 == UJYAALO_ONLINE:
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page_ujyaalo)
			elif source1 == TOP_NEPAL_NEWS:
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page_topnepalnews)

		
	def parse_page_onlinekhabar(self, response):
		for page in response.css('div.ok-single-content'):
			for paragraph in page.css('p::text').extract():
				paragraph = re.sub('["\',]', '', paragraph.strip())
				yield {
					'content': paragraph
				}

	def parse_page_ekantipur(self, response):
		for page in response.css('div.maincontent'):
			for paragraph in page.css('p::text').extract():
				paragraph = re.sub('["\',]', '', paragraph.strip())
				yield {
					'content': paragraph
				}

	def parse_page_hamrakura(self, response):
		for page in response.css('div.content-single'):
			for paragraph in page.css('p::text').extract():
				paragraph = re.sub('["\',]', '', paragraph.strip())
				yield {
					'content': paragraph
				}

	def parse_page_ujyaalo(self, response):
		for content in response.css('div.detailbox').extract():
			yield {
				'content': clean_txt(content)
			}

	def parse_page_topnepalnews(self, response):
		for content in response.css('div.article-single'):
			for paragraph in content.css('p::text').extract():
				yield {
					'content': clean_txt(paragraph)
				}



	