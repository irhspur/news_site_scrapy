import scrapy
import re
# Constants
def definition () :
    global RATOPATI
    RATOPATI = 1
    global EKANTIPUR
    EKANTIPUR = 2
    global SETOPATI
    SETOPATI = 3
    global UJYAALO_ONLINE
    UJYAALO_ONLINE = 4
    global TOP_NEPAL_NEWS
    TOP_NEPAL_NEWS = 5

def get_source (link) :

    if re.match( "https://setopati.com/sports/.*[0-9]$" , link):
        return RATOPATI
    elif re.match( "http://.*.ekantipur.com/news/2017.*.html$" , link):
        return EKANTIPUR
    elif re.match( "http://www.ratopati.com/story/.*[0-9]$" , link):
        return SETOPATI
    elif re.match( "http://ujyaaloonline.com/news/.*[0-9]/.*/$" , link):
        return UJYAALO_ONLINE
    elif re.match( 'http://topnepalnews.com/entertainment/.*[0-9]$' , link):
        return TOP_NEPAL_NEWS
    else :
        return None

def get_urls () :
    urls = [ 'http://www.ekantipur.com/nep/sports' ]
    for pages in range( 1 , 70 ): # total pages 511
        urls = urls + [ 'http://www.setopati.com/sports']
    for pages in range( 1 , 10 ): # total pages 48
        urls = urls + [ 'http://www.ratopati.com/category/sports']
    for pages in range( 1 , 11 ): # total pages 56
        urls = urls + [ 'http://ujyaaloonline.com/news/category/18/sport/page' + str(pages) + '/' ]
    for pages in range( 0 , 50 , 25 ): # total pages 175
        urls = urls + [ 'http://topnepalnews.com/Sports?per_page=' + str(pages)]
    return urls

def clean_txt (raw_input) :
    # Function to remove html tags and extra special characters
    cleanr = re.compile( '<.*?>' )
    cleantext = re.sub(cleanr, '' , raw_input)
    cleantext = re.sub( '["\',]' , '' , cleantext.strip())
    return cleantext

class EconomySpider(scrapy.Spider) :
    definition()
    name = "sports"
    start_urls = []
    start_urls = start_urls + get_urls()

    def parse (self, response) :
        
        for link in response.css( 'a::attr(href)' ).extract():
            self.log( "Links__ %s" % link)
        
            source1 = get_source(link)

            if source1 == RATOPATI:
                link = response.urljoin(link)
                self.log( 'Link_input %s' % link)
                yield scrapy.Request(link, callback=self.parse_page_ratopati)
            elif source1 == EKANTIPUR:
                link = response.urljoin(link)
                self.log( 'Link_input %s' % link)
                yield scrapy.Request(link, callback=self.parse_page_ekantipur)
            elif source1 == SETOPATI:
                link = response.urljoin(link)
                self.log( 'Link_input %s' % link)
                yield scrapy.Request(link, callback=self.parse_page_setopati)
            elif source1 == UJYAALO_ONLINE:
                link = response.urljoin(link)
                self.log( 'Link_input %s' % link)
                yield scrapy.Request(link, callback=self.parse_page_ujyaalo)
            elif source1 == TOP_NEPAL_NEWS:
                link = response.urljoin(link)
                self.log( 'Link_input %s' % link)
                yield scrapy.Request(link, callback=self.parse_page_topnepalnews)

    def parse_page_setopati (self, response) :
        for content in response.css( 'div.entry-content' ).extract():
            yield {
                'content' : clean_txt(content)
            }
    def parse_page_ekantipur (self, response) :
        for page in response.css( 'div.maincontent' ):
            for paragraph in page.css( 'p::text' ).extract():
                paragraph = re.sub( '["\',]' , '' , paragraph.strip())
                yield {
                    'content' : paragraph
                }
    def parse_page_ratopati (self, response) :
        for content in response.css( 'div.mainEntityOfPage').extract():
            yield {
                'content' : clean_txt(content)
            }
    def parse_page_ujyaalo (self, response) :
        for content in response.css( 'div.detailbox' ).extract():
            yield {
                'content' : clean_txt(content)
            }
    def parse_page_topnepalnews (self, response) :
        for content in response.css( 'div.article-single' ):
            for paragraph in content.css( 'p::text' ).extract():
                yield {
                    'content' : clean_txt(paragraph)
                }
