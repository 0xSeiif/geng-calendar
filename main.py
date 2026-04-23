import requests
from ics import Calendar, Event
import arrow

def get_geng_matches():
    url = "https://lol.fandom.com/api.php"
    
    # On cherche "Gen.G" avec un joker (%) pour attraper "Gen.G Esports" ou "Gen.G"
    params = {
        "action": "cargoquery",
        "format": "json",
        "tables": "MatchSchedule",
        "fields": "DateTime_UTC, Team1, Team2, BestOf, Tournament",
        # On cherche tous les matchs de 2026 (l'année actuelle)
        "where": "(Team1 LIKE 'Gen.G%' OR Team2 LIKE 'Gen.G%') AND DateTime_UTC > '2026-01-01'",
        "order_by": "DateTime_UTC",
        "limit": "50"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("cargoquery", [])
    except Exception as e:
        print(f"Erreur API : {e}")
        return []

def create_calendar():
    matches = get_geng_matches()
    c = Calendar()
    
    if not matches:
        print("Aucun match trouvé.")
        # On crée un événement de test pour vérifier si l'import marche
        e_test = Event()
        e_test.name = "Bot Gen.G Opérationnel - En attente de matchs"
        e_test.begin = arrow.now().datetime
        c.events.add(e_test)
    else:
        for m in matches:
            data = m["title"]
            e = Event()
            
            t1 = data["Team1"]
            t2 = data["Team2"]
            opp = t2 if "Gen.G" in t1 else t1
            
            e.name = f"Gen.G vs {opp} (Bo{data['BestOf']})"
            e.begin = arrow.get(data["DateTime UTC"]).datetime
            e.duration = {"hours": 3}
            e.description = f"Tournoi: {data['Tournament']}"
            e.location = "Twitch.tv/LCK"
            c.events.add(e)
    
    with open('geng_schedule.ics', 'w', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())

if __name__ == "__main__":
    create_calendar()
