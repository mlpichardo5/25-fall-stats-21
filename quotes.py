import scrapy
class QuotesSpider(scrapy.Spider):
    # Defines a new class QuotesSpider that inherits from scrapy.Spider. This class will contain the logic for our spider.
    name = "quotes"
    # Sets the name of the spider to "quotes". This is how you will refer to this spider when running it from the command line.
    allowed_domains = ["quotes.toscrape.com"]
    # attribute is used to restrict the spider to only crawl URLs from specified domains.
    # prevents the spider from accidentally crawling other websites
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]
    # A list of URLs where the spider will begin its crawling.
    # In this case, it starts at the first page of the quotes website.
    def parse(self, response):
        # Defines the parse method, which will be called with the response object of each request made.
        # This is where the main parsing logic of the spider resides.
        for quote in response.css('div.quote'):
            # Iterates over each div element with the class quote found in the response. 
            # This is where individual quotes are located on the page.
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            # yield : Generates a dictionary containing the extracted data for each quote. 
            # The yield statement is used to return the data without stopping the spider.
                # 'text': quote.css(...): Extracts the text of the quote by selecting the span element with the class text
                # and retrieves its text content.
                # 'author': quote.css(...): Extracts the author's name by selecting the small element
                # with the class author and retrieves its text content.
                # 'tags': quote.css(...),: Extracts all tags associated with the quote by selecting all a 
                # elements with the class tag within the div element with the class tags, and retrieves their text content as a list.

        next_page = response.css('li.next a::attr(href)').get()
        # next_page = response.css('li.next a::attr(href)').get(): 
                # Finds the URL of the next page by selecting the a element within the li element with the class next and retrieving its href attribute.
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        # if next_page is not None:: Checks if there is a next page.
        # yield response.follow(next_page, self.parse): If there is a next page, 
                # the spider follows the link and calls the parse method on the response of the next page.
                # This allows the spider to continue scraping subsequent pages.