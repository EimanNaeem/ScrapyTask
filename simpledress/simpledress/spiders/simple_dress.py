import scrapy


class DressSpider(scrapy.Spider):
    name = 'simple-dress'
    allowed_domains = ['simple-dress.com']
    start_urls = ['http://simple-dress.com/']

    def parse(self, response):
        for link in response.css('div.topimgtwo a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_categories)

    def parse_categories(self, response):
        for link in response.css('div.preview a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_products)

            next_page = response.css('div.pagination a.icon.flaticon-play45.pagination-next::attr(href)').get()
            if next_page is not None:
                link = response.urljoin(next_page)
                yield scrapy.Request(link, callback=self.parse_categories)

    def parse_products(self, response):
            products = response.css('div.product-view.row')
            for product in products:
                try:
                    yield{
                        'title' : product.css('h1.producttitle::text').get(),
                        'Image_URL' : product.css('div.MagicToolboxContainer a::attr(href)').get(),
                        'Current_price': product.css('p.special-price span.price::text').get().strip().replace('$',''),
                        'old_price': product.css('p.old-price span.price::text').get().strip().replace('$',''),
                        'size_options': product.css('div.size-custom-option option::text').getall(),
                        'Color':  product.css('div.color-custom-option option::text').getall(),
                    }
                except:
                    yield{
                        'title' : product.css('h1.producttitle::text').get(),
                        'Image_URL' : product.css('div.MagicToolboxContainer a::attr(href)').get(),
                        'price' : product.css('span.regular-price span.price::text').get().replace('$',''),
                        'size_options': product.css('div.size-custom-option option::text').getall(),
                        'Color' : product.css('div.color-custom-option option::text').getall(),
                    }
