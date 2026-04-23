import os
import requests
from ics import Calendar, Event
import arrow

# On récupère la clé API que tu as cachée dans les paramètres GitHub
API_KEY = os.getenv("PANDASCORE_API_KEY")
TEAM_SLUG = "gen-g" 

def get_matches():
    url = f"https://api.pandascore.co/teams/{TEAM_SLUG}/matches?filter[future]=true"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

def create_calendar():
    matches = get_matches()
    c = Calendar()
    
    for m in matches:
        e = Event()
        e.name = f"Gen.G vs {m['opponents'][0]['opponent']['name'] if m['opponents'] else 'TBD'}"
        e.begin = arrow.get(m['scheduled_at']).datetime
        e.description = f"Tournoi: {m['league']['name']}"
        c.events.add(e)
    
    # On crée le fichier final
    with open('geng_schedule.ics', 'w') as f:
        f.writelines(c.serialize_iter())

if __name__ == "__main__":
    create_calendar()