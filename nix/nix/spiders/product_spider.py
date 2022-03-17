import scrapy

class NixSpider(scrapy.Spider):
  name = 'nix'
  start_urls = [
    # 'https://quotes.toscrape.com/',
    'https://httpbin.org/ip'
  ]

  def parse(self, response):
    title = response.text
    yield {'titletext': title}