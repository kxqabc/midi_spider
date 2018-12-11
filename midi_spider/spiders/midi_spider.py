import scrapy

from ..items import MidiItem


class MidiSpider(scrapy.Spider):
    name = "midi_spider"
    allowed_domains = ["freemidi.org"]
    start_urls = ["https://freemidi.org/songtitle-%s" % e for e in ['0', 'a', 'b', 'c']]

    def parse(self, response):
        main_content = response.xpath("//body/div[@id='container']/div[@id='mainContent']")
        page_selector = response.xpath("./div[@class='header-nav-pages-container']")
        current_page = int(page_selector.xpath("./span[@class='current']").extract_first())
        print "current page: %s" % str(current_page)
        last_page = int(page_selector.xpath("./a[last()]").extract_first())
        print "last page: %s" % str(last_page)
        
        i = 0
        while True:
            page_url = response.url + '-%d' % i
            i += 1

        song_selectors = response.xpath("//body/div[@id='container']/div[@id='mainContent']/div[@class='song-list-container']")
        print "len of songs: %d" % len(song_selectors)
        for song_sel in song_selectors:
            song_href = song_sel.xpath("./div[@class='row-title']/a/@href").extract_first()
            song_url = response.urljoin(song_href)
            yield scrapy.Request(song_url, callback=self.parse_song_link)

    def parse_song_link(self, response):
        midi_download_sel = response.xpath("//body/"
                                  "div[@id='container']/"
                                  "div[@id='mainContent']/"
                                  "div[@class='container-fluid']/"
                                  "div[@class='row']/"
                                  "div[@class='col-xs-12']/"
                                  "div[@class='container-fluid']/"
                                  "a[@id='downloadmidi']")
        href = midi_download_sel.xpath("./@href").extract_first()
        url = response.urljoin(href)
        print "download url: %s" % str(url)
        midi_item  = MidiItem()
        midi_item['file_urls'] = [url]
        midi_item['file_name'] = "first"
        return midi_item
