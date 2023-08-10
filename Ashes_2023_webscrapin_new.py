import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

#Sending request to html page

url = "https://www.cricbuzz.com/cricket-series/4777/the-ashes-2023/matches"
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content,'html.parser')

#Finding all match links
matches = soup.find_all('a',{'class' : 'text-hvr-underline'})
match_link = []
for match in matches:
    match = match.get('href')
    if 'scores' in match:
        match_link.append('https://www.cricbuzz.com'+match)

#Finding scorecards links of all matches
scorecards_link = []
for link in match_link:
    response = requests.get(link)
    html_content = response.text

    soup = BeautifulSoup(html_content,'html.parser')
    scorecard = soup.find_all('a',{'class' : 'cb-nav-tab'})
    for s in scorecard:
        if s.text == 'Scorecard':
            scorecards_link.append('https://www.cricbuzz.com'+s.get('href'))

#creating excel workbook for both batsman and bowler
batsman_workbook = Workbook()
batsman_file = batsman_workbook.active
batsman_file.append(['Team', 'Match no', 'Batsman Name', 'Runs', 'Balls', 'Fours', 'Sixes', 'Strike Rate'])

bowler_workbook  = Workbook()
bowler_file = bowler_workbook.active
bowler_file.append(['Team', 'Match no', 'Bowler Name', 'Overs', 'Maiden', 'Runs', 'Wickets', 'Nb', 'Wd', 'Economy'])

#collecting bowler and batsman data in a single for loop

test_no = 1
for scorecard_link in scorecards_link:
    suffix = {1: 'st', 2: 'nd', 3: 'rd'}
    if test_no in suffix:
        # print(f'The Ashes : {test_no}{suffix[test_no]} test')
        match_no = f'{test_no}{suffix[test_no]} test'
    else:
        # print(f'The Ashes : {test_no}th test')
        match_no = f'{test_no}th test'
    test_no += 1
    response = requests.get(scorecard_link)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    innings_list = soup.find('div', {'class': 'cb-col cb-col-100 cb-bg-white'})
    for i in range(1, 5):
        innings = innings_list.find('div', {'id': 'innings_' + f'{i}'})
        if innings is not None:
            bat_bowl_tag = innings.find_all('div', {'class': 'cb-col cb-col-100 cb-ltst-wgt-hdr'})
            bat_tag = bat_bowl_tag[0]
            bowl_tag = bat_bowl_tag[-1]

            bt_team = bat_tag.find('div', {'class': 'cb-col cb-col-100 cb-scrd-hdr-rw'}).text.split()[0].strip()
            div_batsman = bat_tag.find_all('div', {'class': 'cb-col cb-col-100 cb-scrd-itms'})
            for batsman in div_batsman:
                batsman_tag = batsman.find('div', {'class': 'cb-col cb-col-25'})
                if batsman_tag:
                    bt_name_tag = batsman_tag.find('a').get('href')
                    response = requests.get('https://www.cricbuzz.com/' + bt_name_tag)
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    bt_name = soup.find('div', {'class': 'cb-col cb-col-80 cb-player-name-wrap'}).find('h1', {
                        'itemprop': 'name'}).text
                    bt_stat = batsman.find_all('div', {'class': 'cb-col cb-col-8 text-right'})
                    runs = batsman.find('div', {'class': 'cb-col cb-col-8 text-right text-bold'}).text
                    if bt_name:
                        batsman_file.append(
                            [bt_team, match_no, bt_name, runs, bt_stat[0].text, bt_stat[1].text, bt_stat[2].text,
                             bt_stat[3].text])
                        print(bt_team, '', match_no, '', bt_name, '', runs, '', bt_stat[0].text, '', bt_stat[1].text,
                              '', bt_stat[2].text, '', bt_stat[3].text)
            time.sleep(5)
            div_bowler = bowl_tag.find_all('div', {'class': 'cb-col cb-col-100 cb-scrd-itms'})

            for bowler in div_bowler:
                if bt_team == 'Australia':
                    bw_team = 'England'
                else:
                    bw_team = 'Australia'
                bowler_tag = bowler.find('div', {'class': 'cb-col cb-col-38'})
                if bowler_tag:
                    bw_name_tag = bowler_tag.find('a').get('href')
                    response = requests.get('https://www.cricbuzz.com/' + bw_name_tag)
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    bw_name = soup.find('div', {'class': 'cb-col cb-col-80 cb-player-name-wrap'}).find('h1', {
                        'itemprop': 'name'}).text
                    bw_stat = bowler.find_all('div', {'class': 'cb-col cb-col-8 text-right'})
                    wicket = bowler.find('div', {'class': 'cb-col cb-col-8 text-right text-bold'}).text
                    re = bowler.find_all('div', {'class': 'cb-col cb-col-10 text-right'})
                    overs, maiden, nb, wd, runs, economy = float(bw_stat[0].text), int(bw_stat[1].text), int(
                        bw_stat[2].text), int(bw_stat[3].text), int(re[0].text), float(re[1].text)
                    if bw_name:
                        bowler_file.append([bw_team, match_no, bw_name, overs, maiden, runs, wicket, nb, wd, economy])
                        print(bw_team, '', match_no, '', bw_name, '', overs, '', maiden, '', runs, '', wicket, '', nb,
                              '', wd, '', economy)

            time.sleep(5)

batsman_workbook.save('batsman_summary.xlsx')
bowler_workbook.save('bowler_summary.xlsx')