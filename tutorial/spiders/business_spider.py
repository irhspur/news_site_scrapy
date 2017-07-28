import scrapy
import re

# Constants
def definition():
	global ANNAPURNA_POST
	ANNAPURNA_POST = 1

	global EKANTIPUR
	EKANTIPUR = 2

	global ONLINE_KHABAR
	ONLINE_KHABAR = 3

	global IMAGE_KHABAR
	IMAGE_KHABAR = 4

	global RAJDHANI_DAILY
	RAJDHANI_DAILY = 5

def get_source(link):		

	if re.match("http://annapurnapost.com/news/.*[0-9]$", link):
		return ANNAPURNA_POST
	elif re.match("http://.*.ekantipur.com/news/2017.*.html$", link):
		return EKANTIPUR
	elif re.match("http:\/\/www.onlinekhabar.com\/2017\/.*[0-9]/$", link):
		return ONLINE_KHABAR
	elif re.match("http://www.imagekhabar.com/news/latest/nepse/.*[0-9]$", link):
		return IMAGE_KHABAR
	elif re.match('http://rajdhanidaily.com/2017.*[0-9]/$', link):
		return RAJDHANI_DAILY
	else: 
		return None

def get_urls():
	urls = ['http://www.ekantipur.com/nep/economy']

	for pages in xrange(0, 150, 30): # total pages 73
		urls = urls + ['http://annapurnapost.com/newslist/16/' + str(pages)]

	for pages in xrange(1, 70): # total pages 48
		urls = urls + ['http://www.onlinekhabar.com/content/bank/page' + str(pages) + '/']

	for pages in xrange(1, 20): # total pages 56
		urls = urls + ['http://www.imagekhabar.com/category/news/topics/economy/?page=' + str(pages)]

	for pages in range(0, 50, 25): # total pages 175
		urls = urls + ['http://rajdhanidaily.com/category/economics/page/' + str(pages) + '/']	

	return urls

def clean_txt(raw_input):
	cleanr = re.compile('<.*?>')
  	cleantext = re.sub(cleanr, '', raw_input)
  	cleantext = re.sub('["\',]', '', cleantext.strip())
  	return cleantext

class BusinessSpider(scrapy.Spider):
	definition()
	name = "business"
	start_urls = []

	start_urls = start_urls + get_urls()

	def parse(self, response):
		for link in response.css('a::attr(href)').extract():
			
			source1 = get_source(link)
			
			if source1 == ANNAPURNA_POST:
				link = response.urljoin(link)
				yield scrapy.Request(link, callback=self.parse_page_annapurna)
			elif source1 == EKANTIPUR:
				link = response.urljoin(link)
				yield scrapy.Request(link, callback=self.parse_page_ekantipur)
			elif source1 == ONLINE_KHABAR:
				link = response.urljoin(link)
				yield scrapy.Request(link, callback=self.parse_page_online_khabar)
			elif source1 == IMAGE_KHABAR:
				link = response.urljoin(link)
				yield scrapy.Request(link, callback=self.parse_page_image_khabar)
			elif source1 == RAJDHANI_DAILY:
				link = response.urljoin(link)
				yield scrapy.Request(link, callback=self.parse_page_rajdhani_daily)

		
	def parse_page_annapurna(self, response):
		for page in response.css('div.detail_content'):
			for paragraph in page.css('p::text').extract():
				paragraph = re.sub('["\',]', '', paragraph.strip())
				yield {
					'content': clean_txt(paragraph)
				}

	def parse_page_ekantipur(self, response):
		for page in response.css('div.maincontent'):
			for paragraph in page.css('p::text').extract():
				paragraph = re.sub('["\',]', '', paragraph.strip())
				yield {
					'content':  clean_txt(paragraph)
				}

	def parse_page_online_khabar(self, response):
		for page in response.css('div.ok-single-content'):
			for paragraph in page.css('p::text').extract():
				paragraph = re.sub('["\',]', '', paragraph.strip())
				yield {
					'content':  clean_txt(paragraph)
				}

	def parse_page_image_khabar(self, response):
		for page in response.css('div.full-article'):
			for paragraph in page.css('p::text').extract():
				paragraph = re.sub('["\',]', '', paragraph.strip())
				yield {
					'content':  clean_txt(paragraph)
				}

	def parse_page_rajdhani_daily(self, response):
		for content in response.css('div.the-content'):
			for paragraph in content.css('p::text').extract():
				yield {
					'content': clean_txt(paragraph)
				}



	