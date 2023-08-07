import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

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

#Getting Batsman stats

excel = Workbook()
batsman_file = excel.active
batsman_file.append(['Team', 'Match no', 'Batsman Name', 'Runs', 'Balls', 'Fours', 'Sixes', 'Strike Rate'])

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
    innings_list = soup.find_all('div', {'class': 'cb-col cb-col-100 cb-ltst-wgt-hdr'})
    for i in innings_list:
        div_team = i.find('div', {'class': 'cb-col cb-col-100 cb-scrd-hdr-rw'})
        if div_team:
            team = div_team.text.split()[0]
        div_batsman = i.find_all('div', {'class': 'cb-col cb-col-100 cb-scrd-itms'})
        for batsman in div_batsman:
            batsman_tag = batsman.find('div', {'class': 'cb-col cb-col-25'})
            if batsman_tag:
                bt_name = batsman_tag.find('a', {'class': 'cb-text-link'}).text
                bt_stat = batsman.find_all('div', {'class': 'cb-col cb-col-8 text-right'})
                runs = batsman.find('div', {'class': 'cb-col cb-col-8 text-right text-bold'}).text
                if bt_name:
                    # print(team,'',match_no,'',bt_name,'',runs,'',bt_stat[0].text,'',bt_stat[1].text,'',bt_stat[2].text,'',bt_stat[3].text)
                    batsman_file.append([team, match_no, bt_name, int(runs), int(bt_stat[0].text), int(bt_stat[1].text), int(bt_stat[2].text),
                                         float(bt_stat[3].text)])

excel.save("Batsman_summary.xlsx")
print('completed for Batsman')

excel = Workbook()
bowler_file = excel.active
bowler_file.append(['Team', 'Match no', 'Bowler Name', 'Overs', 'Maiden', 'Runs', 'Wickets', 'Nb', 'Wd', 'Economy'])

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
    innings_list = soup.find_all('div', {'class': 'cb-col cb-col-100 cb-ltst-wgt-hdr'})
    for i in innings_list:
        div_team = i.find('div', {'class': 'cb-col cb-col-100 cb-scrd-hdr-rw'})
        if div_team:
            team = div_team.text.split()[0]
        div_bowler = i.find_all('div', {'class': 'cb-col cb-col-100 cb-scrd-itms'})
        for bowler in div_bowler:
            if team == 'Australia':
                bw_team = 'Englang'
            else:
                bw_team = 'Australia'
            bowler_tag = bowler.find('div', {'class': 'cb-col cb-col-38'})
            if bowler_tag:
                bw_name = bowler_tag.find('a', {'class': 'cb-text-link'}).text
                bw_stat = bowler.find_all('div', {'class': 'cb-col cb-col-8 text-right'})
                wicket = bowler.find('div', {'class': 'cb-col cb-col-8 text-right text-bold'}).text
                re = bowler.find_all('div', {'class': 'cb-col cb-col-10 text-right'})
                overs, maiden, nb, wd, runs, economy = float(bw_stat[0].text), int(bw_stat[1].text), int(bw_stat[2].text), int(bw_stat[3].text), int(re[0].text), float(re[1].text)
                bowler_file.append([bw_team, match_no, bw_name, overs, maiden, runs, int(wicket), nb, wd, economy])

excel.save("Bowler_summary.xlsx")
print("Bowlers completed")








