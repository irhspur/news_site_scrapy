import scrapy
import re

def definition():
	global SOURYA_DAILY
	SOURYA_DAILY = 1

	global EKANTIPUR
	EKANTIPUR = 2

	global NEWS_OF_NEPAL
	NEWS_OF_NEPAL = 3

	global WEEKLY_NEPAL
	WEEKLY_NEPAL = 4

	global ENAYA_PATRIKA
	ENAYA_PATRIKA = 5

def get_source(link):		
	if re.match("http://http://www.souryadaily.com/2017.*.html$", link):
		return SOURYA_DAILY
	elif re.match("http://kantipur.ekantipur.com/news/2017.*.html$", link):
		return EKANTIPUR
	elif re.match("http://www.newsofnepal.com/news-details/.*./2017.*$", link):
		return NEWS_OF_NEPAL
	elif re.match("http://weeklynepal.com.np/.*./$", link):
		return WEEKLY_NEPAL
	elif re.match('http://www.enayapatrika.com/2017/.*[0-9]/$', link):
		return ENAYA_PATRIKA
	else: 
		return None

def get_urls():
	urls = ['http://kantipur.ekantipur.com/category/World']
	urls = urls + ['http://www.enayapatrika.com/category/world/']

	for pages in range(1, 10): 
		urls = urls + ['http://www.souryadaily.com/category/international/page/' + str(pages)]

	for pages in xrange(1, 30): 
		urls = urls + ['http://www.newsofnepal.com/category/world/page/' + str(pages) + '/']

	for pages in xrange(1, 30): 
		urls = urls + ['http://weeklynepal.com.np/news/%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B5%E0%A4%BE%E0%A4%B8/page/' + str(pages) + '/']

	return urls

def clean_txt(raw_input):
	cleanr = re.compile('<.*?>')
  	cleantext = re.sub(cleanr, '', raw_input)
  	cleantext = re.sub('["\',]', '', cleantext.strip())
  	return cleantext

class WorldSpider(scrapy.Spider):
	definition()
	name = "world"
	start_urls = []

	start_urls = start_urls + get_urls()

	def parse(self, response):
		for link in response.css('a::attr(href)').extract():
			

			source1 = get_source(link)
			
			if source1 == SOURYA_DAILY:
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page_souryadaily)
			elif source1 == EKANTIPUR:
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page_ekantipur)
			elif source1 == NEWS_OF_NEPAL:
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page_newsofnepal)
			elif source1 == WEEKLY_NEPAL:
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page_weeklynepal)
			elif source1 == ENAYA_PATRIKA:
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page_enayapatrika)

		
	def parse_page_souryadaily(self, response):
		for page in response.css('div.news_left'):
			for paragraph in page.css('p::text').extract():
				yield {
					'content': clean_txt(paragraph)
				}

	def parse_page_ekantipur(self, response):
		for page in response.css('div.content-wrapper'):
			for paragraph in page.css('p::text').extract():
				yield {
					'content': clean_txt(paragraph)
				}

	def parse_page_newsofnepal(self, response):
		for page in response.css('div.td-post-content'):
			for paragraph in page.css('p::text').extract():
				yield {
					'content': clean_txt(paragraph)
				}

	def parse_page_weeklynepal(self, response):
		for page in response.css('div.single-archive'):
			for paragraph in page.css('p::text').extract():
				yield {
					'content': clean_txt(content)
				}

	def parse_page_enayapatrika(self, response):
		for content in response.css('div.news-title-cont'):
			for paragraph in content.css('p::text').extract():
				yield {
					'content': clean_txt(paragraph)
				}