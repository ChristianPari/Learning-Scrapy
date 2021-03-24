import scrapy

class LeagueSpider(scrapy.Spider):
  name = 'League'
  start_urls = ['https://www.basketball-reference.com/teams/']

  def parse(self, response, **kwargs):
    team_rows = response.css('table[id="teams_active"]').css('tbody').css('tr.full_table').extract()

    team_links = []
    for team_row in team_rows:
      team_link = team_row.css('th').css('a').attrib('href')