import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = "fe73752800e88b68a8f31ebeeba89604"
BASE_URL = "https://v3.football.api-sports.io"

def get_upcoming_matches(days_ahead=3):
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "v3.football.api-sports.io"
    }

    european_leagues = [39, 78, 135, 61, 140, 94, 88, 262, 203, 195]  # Premier League, Bundesliga, Serie A, etc.
    matches = []

    for day_offset in range(days_ahead):
        date = (datetime.now() + timedelta(days=day_offset)).strftime('%Y-%m-%d')
        for league_id in european_leagues:
            url = f"{BASE_URL}/fixtures"
            response = requests.get(url, headers=headers, params={
                "league": league_id,
                "season": 2024,
                "date": date,
                "timezone": "Europe/Amsterdam"
            })
            data = response.json()

            for match in data.get("response", []):
                fixture = match["fixture"]
                teams = match["teams"]
                logger.info(f"{teams['home']['name']} vs {teams['away']['name']} on {fixture['date']}")
                matches.append({
                    "home": teams['home']['name'],
                    "away": teams['away']['name'],
                    "date": fixture['date'],
                    "league": match["league"]["name"]
                })

    return matches
