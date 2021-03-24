import scrapy

class NbaSpider(scrapy.Spider):
  name = 'nba'
  start_urls = ['https://www.basketball-reference.com/teams/ATL/2021.html']

  def parse(self, response, **kwargs):
    players = response.css('div[id="div_roster"]').css('tbody').css('tr')
    for player in players:
      yield {
        'name': player.css('td[data-stat="player"]').css('a::text').get(),
        'number': player.css('th::text').get(),
        'position': player.css('td[data-stat="pos"]::text').get()
      }