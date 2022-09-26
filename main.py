#!/usr/bin/env python3

from requests import get
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--username', required=True, type=str)
parser.add_argument('--league', required=True, type=str)
args = parser.parse_args()

with open('players.json', 'r') as f:
    players = json.loads(f.read())

BASE_URL = 'https://api.sleeper.app/v1'

response = get(f"{BASE_URL}/state/nfl")
week = response.json()['week']

response = get(f"{BASE_URL}/user/{args.username}")
user_id = response.json()['user_id']

response = get(f"{BASE_URL}/user/{user_id}/leagues/nfl/2022")
league_id = [
    l for l in response.json() if l['name'] == args.league
][0]['league_id']

response = get(f"{BASE_URL}/league/{league_id}/rosters")
rosters = response.json()
my_roster = [r for r in rosters if r['owner_id'] == user_id][0]

response = get(f"{BASE_URL}/league/{league_id}/users")
league_members = response.json()

response = get(f"{BASE_URL}/league/{league_id}/matchups/{week}")
matchups = response.json()

matchup_id = [
    m for m in matchups if m['roster_id'] == my_roster['roster_id']
][0]['matchup_id']
my_matchup = [
    m for m in matchups
    if m['matchup_id'] == matchup_id
    and m['roster_id'] == my_roster['roster_id']
][0]

opponent_matchup = [
    m for m in matchups
    if m['matchup_id'] == matchup_id
    and m['roster_id'] != my_roster['roster_id']
][0]

opponent_roster = [
    r for r in rosters
    if r['roster_id'] == opponent_matchup['roster_id']
][0]

opponent = [
    u for u in league_members
    if u['user_id'] == opponent_roster['owner_id']
][0]

me = [
    u for u in league_members
    if u['user_id'] == my_roster['owner_id']
][0]


def get_roster_point_totals(players_points):
    roster = {
        'QB': [],
        'RB': [],
        'WR': [],
        'TE': [],
    }

    for pid in players_points:
        player = players[pid]
        position = player['position']

        roster[position].append(players_points[pid])

    roster['QB'].sort(reverse=True)
    roster['RB'].sort(reverse=True)
    roster['WR'].sort(reverse=True)
    roster['TE'].sort(reverse=True)

    qb_points = roster['QB'][0]
    rb_points = roster['RB'][0]
    te_points = roster['TE'][0]

    wr_points = roster['WR'][0] + roster['WR'][1]

    flex_pool = roster['RB'][1:] + roster['WR'][2:] + roster['TE'][1:]
    flex_pool.sort(reverse=True)
    flex_points = flex_pool[0]

    return qb_points + rb_points + te_points + wr_points + flex_points


print(f"{me['metadata']['team_name']} points: ",
      get_roster_point_totals(my_matchup['players_points']))
print(f"{opponent['metadata']['team_name']} points: ", get_roster_point_totals(
    opponent_matchup['players_points']))
