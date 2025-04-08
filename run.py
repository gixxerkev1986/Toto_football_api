
from scraper_api import get_upcoming_matches

if __name__ == "__main__":
    matches = get_upcoming_matches()
    print(f"Found {len(matches)} matches:")
    for m in matches:
        print(f"{m['date']}: {m['home']} vs {m['away']} ({m['league']})")
