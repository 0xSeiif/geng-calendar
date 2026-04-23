import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
import arrow
import re

def get_liquipedia_matches():
    # On se fait passer pour un navigateur web pour ne pas être bloqué
    url = "https://liquipedia.net/leagueoflegends/Gen.G_Esports/Played_Matches"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Encoding': 'gzip, deflate'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    matches = []
    
    # On cherche les lignes de matchs dans les tableaux Liquipedia
    rows = soup.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 4:
            try:
                # Extraction des équipes
                team1 = cells[0].get_text(strip=True)
                team2 = cells[3].get_text(strip=True)
                
                # Extraction de la date
                date_span = cells[2].find('span', class_='timer-object')
                if date_span:
                    timestamp = date_span.get('data-timestamp')
                    if timestamp:
                        match_time = arrow.get(int(timestamp))
                        
                        # On ne prend que les matchs futurs ou très récents
                        if match_time > arrow.now().shift(days=-1):
                            opponent = team2 if "Gen.G" in team1 else team1
                            matches.append({
                                'opponent': opponent,
                                'time': match_time.datetime,
                                'tournament': cells[4].get_text(strip=True) if len(cells) > 4 else "LCK"
                            })
            except:
                continue
    return matches

def create_calendar():
    matches = get_liquipedia_matches()
    c = Calendar()
    
    if not matches:
        # Événement de test pour confirmer que le bot a tourné
        e = Event()
        e.name = "Bot Liquipedia Connecté - Aucun match futur"
        e.begin = arrow.now().datetime
        c.events.add(e)
    else:
        for m in matches:
            e = Event()
            e.name = f"Gen.G vs {m['opponent']}"
            e.begin = m['time']
            e.duration = {"hours": 3}
            e.description = f"Source: Liquipedia\nTournoi: {m['tournament']}"
            c.events.add(e)
            
    with open('geng_schedule.ics', 'w', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())

if __name__ == "__main__":
    create_calendar()
