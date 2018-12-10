import scrapy


class MidiSpider(scrapy.Spider):
    name = "midi_spider"
    allowed_domains = ["freemidi.org"]
    start_urls = [
        "https://freemidi.org/download2-16514-a-powerful-friend--pet-shop-boys",
    ]

    def parse(self, response):
        selector = response.xpath("//body/"
                                  "div[@id='container']/"
                                  "div[@id='mainContent']/"
                                  "div[@class='container-fluid']/"
                                  "div[@class='row']/"
                                  "div[@class='col-xs-12']/"
                                  "div[@class='container-fluid']/"
                                  "a[@id='downloadmidi']")
        text = selector.extract()
        print "first test: %s" % text
        yield text
