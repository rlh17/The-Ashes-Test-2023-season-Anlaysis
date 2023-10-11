import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

url = 'https://www.espncricinfo.com/series/the-ashes-2023-1336037/squads'
response = requests.get(url)
html_content = response.text

match_link_list = []
soup = BeautifulSoup(html_content,'html.parser')
main_link_tag1 = soup.find('div',{'class' : 'ds-mb-4'})
main_link_tag2 = main_link_tag1.find_all('div',{'class' : 'ds-flex ds-flex-row ds-space-x-2'})
for link in main_link_tag2:
    match_link = link.find('a').get('href')
    team_name = link.find('span').text.split(' ')[0].strip()
    match_link_list.append(["https://www.espncricinfo.com"+match_link,team_name])

players_workbook  = Workbook()
players_file = players_workbook.active
players_file.append(['Team','Player Name','Player Image','Player Role'])

i = 0
for match in match_link_list:
    response = requests.get(match[0])
    html_content = response.text

    players_summary = [['Team','Player Name','Player Image','Player Role']]
    soup = BeautifulSoup(html_content,'html.parser')
    player_tag = soup.find_all('div',{'class' : 'ds-border-line odd:ds-border-r ds-border-b'})
    for player in player_tag:
        player_team = match[1]
        player_name = player.find('div',{'class' : 'ds-flex ds-space-x-2'}).find('span').text
        player_image = player.find('img').get('src')
        player_role = player.find('p').text
        players_file.append([player_team,player_name,player_image,player_role])
    time.sleep(7)
    i += 1
    print("added players to list")

players_workbook.save('players_summary.xlsx')
