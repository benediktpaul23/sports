import cloudscraper
import time

API_TOKEN = "951aadcb3407afb427a18418fec9c8a56c523b2fa3d034b836b472f3e08c"
BASE_URL = "https://widgets.oddspedia.com/api"
SPORT_IDS = [1, 2, 3, 4, 5, 6]  # Add all sport_ids you want to check

# Function to fetch matches and odds for a specific sport
def fetch_matches_and_odds(sport_id):
    url = f"{BASE_URL}/matches?api_token={API_TOKEN}&lang=en&sport_id={sport_id}&bookmakers=1"  # Requesting bookmakers
    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.get(url)
        if response.status_code == 200:
            if response.text.strip() == "":
                print(f"Empty response for sport ID {sport_id}.")
                return None
            try:
                data = response.json()
                return data
            except ValueError as e:
                print(f"Error parsing JSON for sport ID {sport_id}: {e}")
                return None
        else:
            print(f"Error: {response.status_code} for sport ID {sport_id}")
            return None
    except Exception as e:
        print(f"Error fetching data for sport ID {sport_id}: {e}")
        return None

# Function to check for surebets across all sports
def check_for_surebets():
    for sport_id in SPORT_IDS:
        matches_data = fetch_matches_and_odds(sport_id)

        if matches_data and 'match_list' in matches_data:
            matches = matches_data['match_list']

            for match in matches:
                leagues = match.get('categories', [{}])[0].get('leagues', [{}])[0]
                home_team = leagues.get('matches', [{}])[0].get('ht', 'Unknown Home Team')
                away_team = leagues.get('matches', [{}])[0].get('at', 'Unknown Away Team')
                league_name = leagues.get('league_name', 'Unknown League')

                print(f"Checking match: {home_team} vs {away_team} in {league_name}")

                # Fetching odds from bookmakers
                bookmakers_odds = leagues.get('matches', [{}])[0].get('bookmakers', [])

                if bookmakers_odds:
                    bookmaker_count = len(bookmakers_odds)  # Count the number of bookmakers
                    print(f"Total bookmakers found: {bookmaker_count}")

                    # Print each bookmaker and their odds
                    for bookmaker in bookmakers_odds:
                        bookmaker_name = bookmaker.get('name', 'Unknown Bookmaker')
                        odds_home = bookmaker.get('odds_home', 'N/A')
                        odds_draw = bookmaker.get('odds_draw', 'N/A')
                        odds_away = bookmaker.get('odds_away', 'N/A')

                        print(f"Bookmaker: {bookmaker_name}")
                        print(f"Odds - Home: {odds_home}, Draw: {odds_draw}, Away: {odds_away}\n")
                else:
                    print(f"No bookmakers available for {home_team} vs {away_team}.")
        else:
            print(f"No valid match data for sport ID {sport_id}.")

# Main loop to check for surebets
try:
    while True:
        check_for_surebets()
        print("Waiting 2 minutes before the next check...")
        time.sleep(120)
except KeyboardInterrupt:
    print("Program stopped.")
