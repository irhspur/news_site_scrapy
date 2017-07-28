import scrapy
import re

class EntertainmentEkanSpider(scrapy.Spider):
	name = "ent_ekan"
	start_urls = [
		'http://www.ekantipur.com/nep/entertainment'
	]

	def parse(self, response):
		for link in response.css('a::attr(href)').extract():
			self.log('Link_input %s' % link)
			match_pattern=re.match("http://.*.ekantipur.com/news/2017.*.html$", link)
			# match_pattern=re.match("http:\/\/www.onlinekhabar.com\/2017\/.*[0-9]/$", link)

			if match_pattern is not None:
				# content_div = link.css('div.ok_single_content')
				link = response.urljoin(link)
				self.log('Link_input %s' % link)
				yield scrapy.Request(link, callback=self.parse_page)
		
	def parse_page(self, response):
		# self.log('Herere %s' % response)
		for page in response.css('div.maincontent'):
			for paragraph in page.css('p::text').extract():
				yield {
					'content': paragraph
				}
