import os
import argparse
import logging
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

from utils import get_page_teams, get_page_scores, get_page_odds
from utils import read_json

logging.basicConfig(level=logging.INFO)


def main(season):
    # read settings file
    settings = read_json('settings.json')
    exec_path = settings['chrome_driver_path']
    url_pattern = settings['url_pattern']
    data_dir = settings['data_dir']
    filename_pattern = settings['filename_pattern']
    filepath = os.path.join(data_dir, filename_pattern % (season - 1, season))

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    driver = webdriver.Chrome(executable_path=exec_path, options=options)
    url1 = url_pattern % (season - 1, season)

    home_teams_all = []
    away_teams_all = []
    home_teams_score_all = []
    away_teams_score_all = []
    home_teams_odds_all = []
    away_teams_odds_all = []
    page = 0
    while True:
        page += 1
        if page > 1:
            url = url1 + '#/page/%d/' % page
        else:
            url = url1
        logging.info('Sraping page: %s' % url)
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features="lxml")
        home_teams, away_teams = get_page_teams(soup)
        home_teams_score, away_teams_score = get_page_scores(soup)
        home_teams_odds, away_teams_odds = get_page_odds(soup)

        lens = [len(home_teams), len(away_teams),
                len(home_teams_score), len(away_teams_score),
                len(home_teams_odds), len(away_teams_odds)]

        if len(set(lens)) != 1:
            logging.warning('The length of lists is not consistent')
        if lens[0] == 0:
            break

        home_teams_all.extend(home_teams)
        away_teams_all.extend(away_teams)
        home_teams_score_all.extend(home_teams_score)
        away_teams_score_all.extend(away_teams_score)
        home_teams_odds_all.extend(home_teams_odds)
        away_teams_odds_all.extend(away_teams_odds)

    df = pd.DataFrame({
        'home_team': home_teams_all, 'away_team': away_teams_all,
        'home_team_points': home_teams_score_all,
        'away_team_points': away_teams_score_all,
        'home_team_odds': home_teams_odds_all,
        'away_team_odds': away_teams_odds_all
    })

    # reverse the order of the games as the latest games are collected first.
    final_df = df.iloc[::-1, :].reset_index(drop=True)
    logging.info('Write to file')
    final_df.to_csv(filepath, index=False)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--season', type=int,
                        help="the ending year of a season")
    args = parser.parse_args()

    if args.season is None:
        parser.print_help()
    else:
        main(args.season)
