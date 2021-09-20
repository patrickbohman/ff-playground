import requests

# Auth stored in cookies. ESPN user must have access to the league (obvi!)
# Settings >> Privacy and Security >> Site Settings >> Cookies >>
# >> See All Cookies and Site Data >> Search 'ESPN' (not espn fantasy) >> copy content SWID & espn_2
swid = #Your SWID
espn_s2 = #Your ESPN

# URL to private fantasy league
url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/2021/segments/0/leagues/1039705048?scoringPeriodId=1&view=kona_player_info'


# in filterSlotIds:  QB=0  RB=2  WR=4  TE=6
headers = {'x-fantasy-filter': '{\"players\":{\"filterStatus\":{\"value\":[\"FREEAGENT\",\"WAIVERS\"]},'
                               '\"filterSlotIds\":{\"value\":[2,4,6]},'
                               '\"filterRanksForScoringPeriodIds\":{\"value\":[1]},\"limit\":500,\"offset\":0,'
                               '\"sortPercOwned\":{\"sortAsc\":false,\"sortPriority\":1},\"sortDraftRanks\":{'
                               '\"sortPriority\":100,\"sortAsc\":true,\"value\":\"STANDARD\"},'
                               '\"filterRanksForRankTypes\":{\"value\":[\"PPR\"]},\"filterRanksForSlotIds\":{'
                               '\"value\":[0,2,4,6,17,16]},\"filterStatsForTopScoringPeriodIds\":{\"value\":2,'
                               '\"additionalValue\":[\"002021\",\"102021\",\"002020\",\"1120211\",\"022021\"]}}}'}

res = requests.get(url, cookies={'SWID': swid, 'espn_s2': espn_s2}, headers=headers)

import json as json

all_players_json = json.loads(res.text)

allPlayers = all_players_json['players']

with open('teams.json') as t:
    team_dict = json.load(t)
t.close()

with open('position.json') as p:
    pos_dict = json.load(p)
p.close()

playerDict = {}

for p in allPlayers:
    if not p['player']['injured']:
        playerDict[p['id']] = {
        'Player Name': p['player']['fullName'],
        'Position': pos_dict[str(p['player']['defaultPositionId'])],
        'TeamName': team_dict[str(p['player']['proTeamId'])],
        'Status': p['status'],
        'Injured': p['player']['injured']
        }

f = open('output/availablePlayers.csv', "w+")
f.close()

import csv

csv_columns = ['Rank', 'Player', 'Position', 'Team', 'Injured']

try:
    with open('output/availablePlayers.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        rank = 1
        for player, value in playerDict.items():
            writer.writerow({'Rank': rank,
                             'Player': value['Player Name'],
                             'Position': value['Position'],
                             'Team': value['TeamName'],
                             'Injured': value['Injured']})
            rank += 1
except IOError:
    print("I/O error")

import pandas as pd

csv = pd.read_csv('output/availablePlayers.csv')

from pyexcel.cookbook import merge_all_to_a_book
import glob

merge_all_to_a_book(glob.glob('output/availablePlayers.csv'), "output/availablePlayers.xlsx")