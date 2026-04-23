import requests
from ics import Calendar, Event
import arrow
from datetime import datetime

def get_geng_matches():
    # URL de l'API de Leaguepedia (Cargo)
    url = "https://lol.fandom.com/api.php"
    
    # On demande les matchs futurs de Gen.G
    params = {
        "action": "cargoquery",
        "format": "json",
        "tables": "MatchSchedule",
        "fields": "DateTime_UTC, Team1, Team2, BestOf, MatchId, Tournament",
        "where": "(Team1 = 'Gen.G' OR Team2 = 'Gen.G') AND DateTime_UTC > '2024-01-01'",
        "order_by": "DateTime_UTC",
        "limit": "50"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("cargoquery", [])
    return []

def create_calendar():
    matches = get_geng_matches()
    c = Calendar()
    
    for m in matches:
        match_data = m.get("title", {})
        
        # On crée l'événement
        e = Event()
        team1 = match_data.get("Team1")
        team2 = match_data.get("Team2")
        tournament = match_data.get("Tournament")
        bo = match_data.get("BestOf")
        
        e.name = f"Gen.G vs {team2 if team1 == 'Gen.G' else team1} (Bo{bo})"
        
        # Gestion de l'heure
        date_str = match_data.get("DateTime UTC")
        if date_str:
            e.begin = arrow.get(date_str).datetime
            e.duration = {"hours": 2} # Durée estimée
            e.description = f"Tournoi : {tournament}\nFormat : Best of {bo}"
            e.location = "Twitch.tv/LCK"
            c.events.add(e)
    
    # On sauvegarde le fichier
    with open('geng_schedule.ics', 'w', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())
    print("Fichier .ics généré avec succès !")

if __name__ == "__main__":
    create_calendar()
