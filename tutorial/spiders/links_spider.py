import scrapy

class LinkSpider(scrapy.Spider):
	name = "link"
	start_urls = (
		'http://www.onlinekhabar.com/',
	)

	def parse(self, response):
		for link in response.css('a::attr(href)').extract():
			# print(link)
			yield {
				'link': link
			}
		next_page = response.css('a::attr(href)').extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
