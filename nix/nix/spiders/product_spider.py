from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep



class NixSpider(Spider):
  name = 'nix'
  start_urls = [
    # 'https://quotes.toscrape.com/',
    'https://books.toscrape.com/'
  ]


  def start_requests(self):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    self.driver = webdriver.Chrome(executable_path=r'D:\python\scrape-website\chromedriver_win\chromedriver.exe', chrome_options=options)
    self.driver.get('https://books.toscrape.com')

    sel = Selector(text=self.driver.page_source)
    books = sel.xpath('//h3/a/@href').extract()
    for book in books:
      url = 'https://books.toscrape.com/' + book
      yield Request(url, callback=self.parse_book)

    while True:
      try:
        next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
        sleep(3)
        self.logger.info('Sleeping for 3 seconds.')
        next_page.click()

        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()
        for book in books:
          url = 'https://books.toscrape.com/catalogue/' + book
          yield Request(url, callback=self.parse_book)
      except NoSuchElementException:
        self.logger.info('No more pages to load')
        self.driver.quit()
        break
        

  def parse_book(self, reponse):
    pass