import requests
import logging
from datetime import datetime, timedelta

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

def get_active_season(league_id):
    """Zoekt het seizoen waar vandaag binnen valt."""
    url = f"{BASE_URL}/leagues?id={league_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    today = datetime.now().date()

    try:
        for season in data["response"][0]["seasons"]:
            start = datetime.strptime(season["start"], "%Y-%m-%d").date()
            end = datetime.strptime(season["end"], "%Y-%m-%d").date()
            if start <= today <= end:
                return season["year"]
        logger.warning(f"Geen actief seizoen gevonden voor league ID {league_id}, fallback naar laatste.")
        return data["response"][0]["seasons"][-1]["year"]
    except Exception as e:
        logger.error(f"Fout bij ophalen seizoen voor league {league_id}: {e}")
        return 2023  # fallback

def get_upcoming_matches(days_ahead=3):
    matches = []

    for league_name, league_id in EUROPEAN_LEAGUES.items():
        season = get_active_season(league_id)
        logger.info(f"{league_name} (ID: {league_id}) - Actief seizoen: {season}")

        for day_offset in range(days_ahead):
            date = (datetime.now() + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            url = f"{BASE_URL}/fixtures"
            response = requests.get(url, headers=HEADERS, params={
                "league": league_id,
                "season": season,
                "date": date,
                "timezone": "Europe/Amsterdam"
            })
            data = response.json()
            count = len(data.get("response", []))
            logger.info(f"  {date}: {count} wedstrijden gevonden")

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
