import cloudscraper
import time

API_TOKEN = "951aadcb3407afb427a18418fec9c8a56c523b2fa3d034b836b472f3e08c"
BASE_URL = "https://widgets.oddspedia.com/api"

# Function to fetch matches from the API
def fetch_matches():
    url = f"{BASE_URL}/matches?api_token={API_TOKEN}&lang=en&sport_id=1"  # Example for Football
    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Fetched data: {data}")  # Log the entire data to inspect structure
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

# Function to check for surebets
def check_for_surebets():
    matches_data = fetch_matches()

    if not matches_data or 'match_list' not in matches_data:
        print("No valid match data.")
        return

    matches = matches_data['match_list']
    print(f"Checking for surebets across {len(matches)} matches...")

    closest_surebet = None
    closest_prob_diff = float('inf')  # Large value to track closest surebet opportunity

    for idx, match in enumerate(matches):
        leagues = match.get('categories', [{}])[0].get('leagues', [{}])[0]
        home_team = leagues.get('matches', [{}])[idx].get('ht', 'Unknown Home Team')
        away_team = leagues.get('matches', [{}])[idx].get('at', 'Unknown Away Team')
        league_name = leagues.get('league_name', 'Unknown League')

        print(f"Checking match {idx + 1}/{len(matches)}: {home_team} vs {away_team} in {league_name}")

        # Example odds, replace with actual odds fetching logic
        odds_home = 1.5  # Example odds
        odds_away = 2.8  # Example odds

        total_implied_probability = calculate_implied_probability(odds_home) + calculate_implied_probability(odds_away)

        # Check how close this match is to being a surebet
        prob_diff = total_implied_probability - 1
        if prob_diff < closest_prob_diff:
            closest_surebet = (home_team, away_team, league_name, total_implied_probability)
            closest_prob_diff = prob_diff

        print(f"Total implied probability: {total_implied_probability} ({prob_diff * 100:.2f}% away from a surebet)\n")

    if closest_surebet:
        print(f"Closest match to a surebet: {closest_surebet[0]} vs {closest_surebet[1]} in {closest_surebet[2]}")
        print(f"Total implied probability: {closest_surebet[3]:.2f}")
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
