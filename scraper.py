import requests
from bs4 import BeautifulSoup
import json
import re

from utils import get_schedule

def get_player(match_id):

    url=f"https://embed.bananacreamcafe.com/dooball66v2/ajax_player.php?match_id={match_id}&api_key=hmcb4rf66f"

    r=requests.get(url)

    soup=BeautifulSoup(r.text,"html.parser")

    iframe=soup.select_one("iframe")

    if iframe:
        return iframe["src"]

    return None


def get_stream(url):

    headers={
     "User-Agent":"Mozilla/5.0",
     "Referer":"https://embed.bananacreamcafe.com/"
    }

    r=requests.get(url,headers=headers)

    m=re.search(r'https://.*?\.m3u8',r.text)

    if m:
        return m.group(0)

    return None


matches=get_schedule()

channels=[]

for m in matches:

    player=get_player(m["match_id"])

    if not player:
        continue

    stream=get_stream(player)

    if not stream:
        continue

    channels.append({
     "name":f'{m["home"]} vs {m["away"]}',
     "stream":stream
    })


with open("playlist.json","w") as f:
    json.dump(channels,f,indent=2)


m3u="#EXTM3U\n"

for c in channels:

    m3u+=f'#EXTINF:-1,{c["name"]}\n'
    m3u+=c["stream"]+"\n"

open("playlist.m3u","w").write(m3u)

print("playlist generated")