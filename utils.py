import requests
from bs4 import BeautifulSoup

BASE = "https://embed.bananacreamcafe.com/dooball66v2/"

headers = {
 "User-Agent":"Mozilla/5.0"
}

def get_schedule():

    url = BASE + "schedule.html"

    r = requests.get(url,headers=headers)

    soup = BeautifulSoup(r.text,"html.parser")

    matches = []

    for m in soup.select(".match-live"):

        a = m.select_one("a")

        if not a:
            continue

        href = a.get("href","")

        if "match_id" not in href:
            continue

        match_id = href.split("match_id=")[1]

        teams = m.select("span")

        if len(teams) < 2:
            continue

        home = teams[0].text.strip()
        away = teams[1].text.strip()

        matches.append({
         "match_id":match_id,
         "home":home,
         "away":away
        })

    return matches