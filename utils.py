import json


def get_page_teams(soup):
    # teams
    teams = soup.find_all(attrs={'class': 'name table-participant'})
    home_teams_page = []
    away_teams_page = []
    for team in teams:
        u = team.find_all('a')[0]
        home_team = u.contents[0].string.strip(' - ')
        away_team = u.contents[1].string.strip(' - ')
        home_teams_page.append(home_team)
        away_teams_page.append(away_team)
    return home_teams_page, away_teams_page


def get_page_scores(soup):
    # scores
    scores = soup.find_all(
        'td', attrs={'class': 'center bold table-odds table-score'})
    home_points_page = []
    away_points_page = []
    for score in scores:
        home_pnts, away_pnts = score.string.split(':')
        home_pnts = int(home_pnts.strip('\xa0OT'))
        away_pnts = int(away_pnts.strip('\xa0OT'))
        home_points_page.append(home_pnts)
        away_points_page.append(away_pnts)
    return home_points_page, away_points_page


def get_page_odds(soup):
    # odds
    odds = soup.find_all(attrs={'xparam': 'odds_text'})
    home_odds_page = []
    away_odds_page = []
    for i, odd in enumerate(odds):
        if i % 2 == 0:
            # convert odds to decimal
            home_odds_page.append(eval(odd.contents[0]) + 1)
            # home_odds_all.append(odd.contents[0])
        else:
            # convert odds to decimal
            away_odds_page.append(eval(odd.contents[0]) + 1)
            # away_odds_all.append(odd.contents[0])
    return home_odds_page, away_odds_page


def read_json(file):
    '''
    Reads data from json file
    '''
    with open(file, 'r', encoding='utf8') as outfile:
        data = json.load(outfile)
    return data
