import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        # explore response object
        print(f'Response: {response}')
        print(f'Response Status: {response.status}')
        print(f'Response Headers: {response.headers}')

        # View page content
        print(f'Response Content: {response.text[:500]}')

        # page title
        page_title = response.css('title::text').get()
        print(f"Page Title: {page_title}")

        # extract quotes, authors and tags from the page
        quotes = response.css('div.quote')
        for quote in quotes:
            quote_text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()
            yield {
                'text': quote_text,
                'author': author,
                'tags': tags
            }
        
        # navigate to next link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback = self.parse)

