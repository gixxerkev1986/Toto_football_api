import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = "fe73752800e88b68a8f31ebeeba89604"
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "v3.football.api-sports.io"
}

# Europese competities met naam + ID
EUROPEAN_LEAGUES = {
    "Premier League": 39,
    "Bundesliga": 78,
    "Serie A": 135,
    "Ligue 1": 61,
    "La Liga": 140,
    "Eredivisie": 88,
    "Belgian Pro League": 94,
    "Swiss Super League": 203,
    "Austrian Bundesliga": 195,
    "Scottish Premiership": 179
}

def get_upcoming_matches():
    matches = []

    for league_name, league_id in EUROPEAN_LEAGUES.items():
        logger.info(f"{league_name} (ID: {league_id}) - ophalen volgende 10 wedstrijden")

        url = f"{BASE_URL}/fixtures"
        response = requests.get(url, headers=HEADERS, params={
            "league": league_id,
            "next": 10,
            "timezone": "Europe/Amsterdam"
        })
        data = response.json()
        count = len(data.get("response", []))
        logger.info(f"  {count} wedstrijden gevonden")

        for match in data.get("response", []):
            fixture = match["fixture"]
            teams = match["teams"]
            matches.append({
                "home": teams['home']['name'],
                "away": teams['away']['name'],
                "date": fixture['date'],
                "league": match["league"]["name"]
            })

    return matches
