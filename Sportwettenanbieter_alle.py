import cloudscraper
import time

API_TOKEN = "951aadcb3407afb427a18418fec9c8a56c523b2fa3d034b836b472f3e08c"
BASE_URL = "https://widgets.oddspedia.com/api"
SPORT_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]  # Add all sport_ids you want to check

# Function to fetch matches for a specific sport
def fetch_matches(sport_id):
    url = f"{BASE_URL}/matches?api_token={API_TOKEN}&lang=en&sport_id={sport_id}"
    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to calculate implied probability
def calculate_implied_probability(odds):
    return 1 / odds if odds > 0 else 0

# Function to check for surebets across all sports
def check_for_surebets():
    best_surebet = None
    best_surebet_percentage = -float('inf')  # Track the highest surebet win percentage

    for sport_id in SPORT_IDS:
        matches_data = fetch_matches(sport_id)

        if not matches_data or 'match_list' not in matches_data:
            print(f"No valid match data for sport ID {sport_id}.")
            continue

        matches = matches_data['match_list']
        print(f"Checking for surebets across {len(matches)} matches for sport ID {sport_id}...")

        for idx, match in enumerate(matches):
            leagues = match.get('categories', [{}])[0].get('leagues', [{}])[0]
            home_team = leagues.get('matches', [{}])[idx].get('ht', 'Unknown Home Team')
            away_team = leagues.get('matches', [{}])[idx].get('at', 'Unknown Away Team')
            league_name = leagues.get('league_name', 'Unknown League')

            bookmakers_odds = leagues.get('matches', [{}])[idx].get('bookmakers', [])
            best_odds_home = float('inf')
            best_odds_away = float('inf')
            best_home_bookmaker = ""
            best_away_bookmaker = ""

            # Loop through all bookmakers and find the best odds for home and away
            for bookmaker in bookmakers_odds:
                bookmaker_name = bookmaker.get('name', 'Unknown Bookmaker')
                odds_home = bookmaker.get('odds_home', None)
                odds_away = bookmaker.get('odds_away', None)

                if odds_home and odds_home < best_odds_home:
                    best_odds_home = odds_home
                    best_home_bookmaker = bookmaker_name

                if odds_away and odds_away < best_odds_away:
                    best_odds_away = odds_away
                    best_away_bookmaker = bookmaker_name

            if best_odds_home == float('inf') or best_odds_away == float('inf'):
                print(f"No valid odds for match {home_team} vs {away_team}.")
                continue

            total_implied_probability = calculate_implied_probability(best_odds_home) + calculate_implied_probability(best_odds_away)

            # Check how close this match is to being a surebet
            surebet_percentage = (1 - total_implied_probability) * 100

            if surebet_percentage > best_surebet_percentage:
                best_surebet_percentage = surebet_percentage
                best_surebet = (home_team, away_team, league_name, total_implied_probability, best_home_bookmaker, best_away_bookmaker)

            print(f"Total implied probability: {total_implied_probability} ({surebet_percentage:.2f}% chance of surebet)\n")

    if best_surebet:
        print(f"Highest surebet opportunity: {best_surebet[0]} vs {best_surebet[1]} in {best_surebet[2]}")
        print(f"Home Team Best Odds: {best_surebet[4]}")
        print(f"Away Team Best Odds: {best_surebet[5]}")
        print(f"Total implied probability: {best_surebet[3]:.2f}")
        print(f"Surebet percentage: {best_surebet_percentage:.2f}%")
    else:
        print("No surebets found.")

# Main loop to check for surebets
try:
    while True:
        check_for_surebets()
        print("Waiting 2 minutes before the next check...")
        time.sleep(120)
except KeyboardInterrupt:
    print("Program stopped.")
