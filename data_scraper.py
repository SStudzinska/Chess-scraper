import requests
from bs4 import BeautifulSoup
import os
import csv

NAME = "Name"
TITLE = "Title"
TRAINING_TITLE = "Tr_title"
FEDERATION = "Federation"
STANDARD_RATING = "Rating"
BIRTH_YEAR = "Birth"
GENDER = "Gender"
WHITE_TOTAL = "White_total"
WHITE_WINS = "White_wins"
WHITE_DRAWS = "White_draws"
BLACK_TOTAL = "Black_total"
BLACK_WINS = "Black_wins"
BLACK_DRAWS = "Black_draws"
players_with_elo_1000_2100 = "https://ratings.fide.com/incl_search_l.php?search=&search_rating=all&search_country=all&search_title=all_g&search_other_title=all&search_year=undefined&search_low=1000&search_high=2100&search_inactive=on&search_exrated=off&search_radio=rating&search_bday_start=all&search_bday_end=all&search_radio=rating&search_asc=descending&search_gender=All&simple=0"
players_with_elo_2101_2200 ="https://ratings.fide.com/incl_search_l.php?search=&search_rating=all&search_country=all&search_title=all_g&search_other_title=all&search_year=undefined&search_low=2101&search_high=2200&search_inactive=on&search_exrated=off&search_radio=rating&search_bday_start=all&search_bday_end=all&search_radio=rating&search_asc=descending&search_gender=All&simple=0"
players_with_elo_2201_2300 = "https://ratings.fide.com/incl_search_l.php?search=&search_rating=all&search_country=all&search_title=all_g&search_other_title=all&search_year=undefined&search_low=2201&search_high=2300&search_inactive=on&search_exrated=off&search_radio=rating&search_bday_start=all&search_bday_end=all&search_radio=rating&search_asc=descending&search_gender=All&simple=0"
players_with_elo_2301_2500 = "https://ratings.fide.com/incl_search_l.php?search=&search_rating=all&search_country=all&search_title=all_g&search_other_title=all&search_year=undefined&search_low=2301&search_high=2500&search_inactive=on&search_exrated=off&search_radio=rating&search_bday_start=all&search_bday_end=all&search_radio=rating&search_asc=descending&search_gender=All&simple=0"
players_with_elo_2501_2900 = "https://ratings.fide.com/incl_search_l.php?search=&search_rating=all&search_country=all&search_title=all_g&search_other_title=all&search_year=undefined&search_low=2501&search_high=2900&search_inactive=on&search_exrated=off&search_radio=rating&search_bday_start=all&search_bday_end=all&search_radio=rating&search_asc=descending&search_gender=All&simple=0"


def get_fide_data(urls):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Cookie": "__utma=229134367.66436967.1683803511.1683803511.1683803511.1;"
                  " __utmz=229134367.1683803511.1.1.utmccn=(referral)|utmcsr=google.com|utmcct=/|utmcmd=referral;"
                  " __atuvc=1%7C19; __atssc=google%3B1; __utma=166426153.56833175.1683803177.1683803177.1684000624.2;"
                  " __utmc=166426153; __utmz=166426153.1684000624.2.2.utmcsr=google|utmccn=(organic)"
                  "|utmcmd=organic|utmctr=(not%20provided); sc_is_visitor_unique=rx12156504.1684001697."
                  "F958459269AC4F6434884CC56E760D56.2.2.2.2.2.2.2.2.2; sc_is_visitor_unique=rx12156504.1684007139."
                  "F958459269AC4F6434884CC56E760D56.3.2.2.2.2.2.2.2.2",
        "Host": "ratings.fide.com",
        "Referer": "https://ratings.fide.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    filepath="chess_players_data.csv"
    fieldnames = [NAME, TITLE, TRAINING_TITLE, FEDERATION, STANDARD_RATING, BIRTH_YEAR, GENDER, WHITE_TOTAL, WHITE_WINS, WHITE_DRAWS, BLACK_TOTAL, BLACK_WINS, BLACK_DRAWS]
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    i = 0
    for url in urls:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table_rows = soup.tbody.find_all('tr')

            for player in table_rows:
                cells = player.find_all('td')
                profile_href = cells[0].find('a')['href']
                gender, total_white, total_black, white_wins, white_draws, black_wins, black_draws = get_info_from_profile(profile_href, headers)
                name = cells[0].find('a').text
                title = cells[1].text.strip()
                training_title = cells[2].find('span').text
                federation = cells[3].text.strip()
                std = cells[4].text.strip()
                birth_year = cells[7].text.strip()
                data ={
                    NAME: name,
                    TITLE: title,
                    TRAINING_TITLE: training_title,
                    FEDERATION: federation,
                    STANDARD_RATING: std,
                    BIRTH_YEAR: birth_year,
                    GENDER: gender,
                    WHITE_TOTAL: total_white,
                    WHITE_WINS: white_wins,
                    WHITE_DRAWS: white_draws,
                    BLACK_TOTAL: total_black,
                    BLACK_WINS: black_wins,
                    BLACK_DRAWS: black_draws
                }
                i += 1
                with open(filepath, 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow(data)
                    print(data)



def get_info_from_profile(profile, headers):

    response = requests.get("https://ratings.fide.com" + profile, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    gender_div = soup.find('div', class_='profile-top-info__block__row__header', string='Sex:')
    gender = gender_div.find_next_sibling('div', class_='profile-top-info__block__row__data').text
    PLAYER_ID = profile.split("/profile/")[-1]
    headers2 = {
        "POST": f"/a_data_stats.php?id1={PLAYER_ID}&id2=0 HTTP/1.1",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Cookie": "__utma=229134367.66436967.1683803511.1683803511.1683803511.1; __utmz=229134367.1683803511.1.1.utmccn=(referral)|utmcsr=google.com|utmcct=/|utmcmd=referral; __atuvc=1%7C19; __atssc=google%3B1; __utmc=166426153; __utma=166426153.56833175.1683803177.1685174272.1685177586.6; __utmz=166426153.1685177586.6.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; sc_is_visitor_unique=rx12156504.1685177668.F958459269AC4F6434884CC56E760D56.6.5.4.4.4.4.4.4.4; __utmb=166426153.2.10.1685177586; sc_is_visitor_unique=rx12156504.1685177740.F958459269AC4F6434884CC56E760D56.6.5.4.4.4.4.4.4.4",
        "Host": "ratings.fide.com",
        "Origin": "https://ratings.fide.com",
        "Referer": f"https://ratings.fide.com/profile/{PLAYER_ID}/statistics",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    action_postURL = f'https://ratings.fide.com/a_data_stats.php?id1={PLAYER_ID}&id2=0'
    res = requests.get(action_postURL)
    search_cookies = res.cookies
    res_post = requests.post(action_postURL, headers=headers2, cookies=search_cookies)
    data = res_post.json()
    white_total = data[0]["white_total_std"]
    black_total = data[0]["black_total_std"]
    white_wins = data[0]["white_win_num_std"]
    white_draws = data[0]["white_draw_num_std"]
    black_wins = data[0]["black_win_num_std"]
    black_draws = data[0]["black_draw_num_std"]

    return gender, white_total, black_total, white_wins, white_draws, black_wins, black_draws


if __name__ == "__main__":
    urls = [players_with_elo_2501_2900, players_with_elo_2301_2500, players_with_elo_2201_2300, players_with_elo_2101_2200, players_with_elo_1000_2100]
    get_fide_data(urls)
