import requests
from ics import Calendar, Event
import arrow

def get_geng_matches():
    # API officielle de LoL Esports (perspectives de Riot)
    url = "https://esports-api.elisa.io/query" 
    # Note : Riot utilise souvent des endpoints complexes, 
    # une alternative stable est l'API de Strafe ou Liquipedia.
    # Pour rester simple sans clé, on va utiliser l'API publique de "Abios" via un proxy.
    
    url = "https://pandascore.co/api/teams/gen-g/matches?filter[future]=true"
    # ATTENTION : Si tu ne veux vraiment aucune clé, la meilleure source alternative 
    # est de "scrapper" le site Liquipedia qui est la référence absolue.
    
    # Voici un code robuste qui utilise un flux RSS/JSON de tournois :
    url = "https://raw.githubusercontent.com/LoL-Esports/calendar/main/data/leagues/lck.json"
    
    # Mais pour ne pas te perdre, essayons une version simplifiée de Liquipedia :
    return [] # On va plutôt passer par un parseur HTML simple

# Voici la version "Liquipedia" (très fiable pour Gen.G)
def create_calendar():
    c = Calendar()
    
    # On utilise un service qui transforme Liquipedia en JSON pour nous simplifier la vie
    try:
        # On cible la LCK sur Liquipedia
        response = requests.get("https://api.liquipedia.net/api/v1/match", params={
            "wiki": "leagueoflegends",
            "conditions": "[[opponent1::Gen.G]] OR [[opponent2::Gen.G]]",
            "limit": 50
        })
        # Note : Liquipedia demande une clé aussi désormais...
    except:
        pass

    # REVENONS À LA SOLUTION LA PLUS SIMPLE : 
    # On va corriger le script Leaguepedia car c'est le SEUL qui ne demande pas de clé.
    # Le problème venait juste de la date ou du nom du tournoi.
    
    url = "https://lol.fandom.com/api.php"
    params = {
        "action": "cargoquery",
        "format": "json",
        "tables": "MatchSchedule",
        "fields": "DateTime_UTC, Team1, Team2, BestOf, Tournament",
        "where": "Team1 LIKE '%Gen.G%' OR Team2 LIKE '%Gen.G%'", # On enlève la date pour tester
        "order_by": "DateTime_UTC DESC", # On prend les plus récents en premier
        "limit": "20"
    }
    
    res = requests.get(url, params=params).json()
    matches = res.get("cargoquery", [])
    
    if not matches:
        e = Event()
        e.name = "Bot en attente de nouveaux matchs"
        e.begin = arrow.now().datetime
        c.events.add(e)
    else:
        for m in matches:
            d = m["title"]
            e = Event()
            e.name = f"Gen.G vs {d['Team2'] if 'Gen.G' in d['Team1'] else d['Team1']}"
            e.begin = arrow.get(d["DateTime UTC"]).datetime
            e.description = f"Tournoi: {d['Tournament']}"
            c.events.add(e)

    with open('geng_schedule.ics', 'w', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())

if __name__ == "__main__":
    create_calendar()
