import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

matchsummary_workbook = Workbook()
matchsummary_file = matchsummary_workbook.active
matchsummary_file.append(['Match no','Team1','Team2','Stadium','Winner','Margin'])

url = "https://www.cricbuzz.com/cricket-series/4777/the-ashes-2023/matches"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')
matches = soup.find_all('div', {'class': "cb-col-60 cb-col cb-srs-mtchs-tm"})
for match in matches:
    # match tag has team1 , team2
    match_tag = match.find('a', {'class': "text-hvr-underline"}).text.split(',')
    team_tag = match_tag[0].split(' ')
    team1, team2 = team_tag[0].strip(), team_tag[2][0:-1].strip()
    match_no = match_tag[1].strip()
    stadium = match.find('div', {'class': "text-gray"}).text.split(',')[0].strip()
    # margin and winner tag
    mw_tag = match.find('a', {'class': "cb-text-complete"}).text
    if "Australia" in mw_tag:
        winner = "Australia"
        margin = mw_tag.split('by')[1].strip()
    elif "England" in mw_tag:
        winner = "England"
        margin = mw_tag.split('by')[1].strip()
    else:
        winner = 'Draw'
        margin = 'Draw'
    margin = margin.replace('wkts', 'Wickets')
    margin = margin.replace('runs', 'Runs')
    matchsummary_file.append([match_no,team1, team2, stadium, winner, margin])

matchsummary_workbook.save("match_summary.xlsx")





