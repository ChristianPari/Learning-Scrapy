import scrapy
import csv

class LeagueSpider(scrapy.Spider):
  name = 'League'
  start_urls = ['https://www.basketball-reference.com/teams/']

  def parse(self, response, **kwargs):
    team_links = response.css('table[id="teams_active"]').css('tbody').css('tr.full_table').css('th').css('a::attr("href")')
    for link in team_links:
      team_abrv = link.get()[7: 10].lower()
      url = self.start_urls[0][0: -7] + link.get()
      yield scrapy.Request(url, callback=self.parse_teams_roster_links, meta={'team_abrv': team_abrv})

  def parse_teams_roster_links(self, response):
    team_table_rows = response.css('table.sortable').css('tbody').css('tr')
    roster_link = team_table_rows[0].css('td[data-stat="team_name"]').css('a::attr("href")').get()
    team_abrv = response.meta.get('team_abrv')
    yield response.follow(roster_link, callback=self.parse_roster, meta={'team_abrv': team_abrv})

  def parse_roster(self, response):
    team_abrv = response.meta.get('team_abrv')
    players = response.css('div[id="div_roster"]').css('tbody').css('tr')
    players_data = []
    for player in players:
      player_data = {
        'team': team_abrv,
        'number': player.css('th::text').get(),
        'name': player.css('td[data-stat="player"]').css('a::text').get(),
        'position': player.css('td[data-stat="pos"]::text').get()
      }
      if player_data['number'].__eq__(''):
        player_data['number'] = 'n/a'

      players_data.append(player_data)
    write_to_csv('C:/Users/Chris/Documents/csv-files/nba/' + team_abrv + '.csv', players_data)

def write_to_csv(file_name, data):
  with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
    field_names = ['team', 'number', 'name', 'position']
    writer = csv.DictWriter(csv_file, fieldnames=field_names)

    writer.writeheader()
    for info in data:
      writer.writerow(
        {
          'team': info.get('team'),
          'number': info.get('number'),
          'name': info.get('name'),
          'position': info.get('position')
        }
      )
