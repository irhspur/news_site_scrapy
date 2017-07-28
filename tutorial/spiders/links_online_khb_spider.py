import scrapy
import re

class LinkSpider(scrapy.Spider):
	name = "link_olkb"
	start_urls = (
		'http://www.onlinekhabar.com/content/ent-news/page/%s' % page for page in xrange(1, 2)
	)

	def parse(self, response):
		for link in response.css('a::attr(href)').extract():
			self.log('Link_input %s' % link)
			match_pattern=re.match("http:\/\/www.onlinekhabar.com\/2017\/\d", link)
			if match_pattern is not None:
				yield {
					'link': link
				}
			#yield {
			#	'link': link
			#}
		next_page = response.css('a::attr(href)').extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
