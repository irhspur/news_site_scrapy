import scrapy
import re

class EntertainmentSpider(scrapy.Spider):
	name = "ent"
	start_urls = (
		'http://www.onlinekhabar.com/content/ent-news/page/%s' % page for page in xrange(1, 2)
	)

	def parse(self, response):
		for link in response.css('a::attr(href)').extract():
			self.log('Link_input %s' % link)
			# match_pattern=re.match("http:\/\/www.onlinekhabar.com\/2017\/\d", link)
			match_pattern=re.match("http:\/\/www.onlinekhabar.com\/2017\/.*[0-9]/$", link)

			if match_pattern is not None:
				# content_div = link.css('div.ok_single_content')
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page)
		
	def parse_page(self, response):
		# self.log('Herere %s' % response)
		for page in response.css('div.ok-single-content'):
			for paragraph in page.css('p::text').extract():
				yield {
					'content': paragraph
				}
