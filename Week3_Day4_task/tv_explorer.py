import urllib.request
import urllib.parse
import urllib.error
import json
import html
from datetime import date


BASE_URL = "https://api.tvmaze.com"


# API Helper

def make_request(endpoint, params=None):

    try:
        url = BASE_URL + endpoint

        if params:
            query_string = urllib.parse.urlencode(params)
            url = url + "?" + query_string

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "TV-Show-Explorer/1.0"
            }
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = response.read().decode("utf-8")

        return json.loads(data)

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("\nResource not found.")
        elif e.code == 429:
            print("\nToo many requests. Please wait and try again.")
        else:
            print(f"\nHTTP Error: {e.code}")

    except urllib.error.URLError as e:
        print(f"\nNetwork error: {e.reason}")

    except json.JSONDecodeError:
        print("\nInvalid response received from API.")

    except Exception as e:
        print(f"\nUnexpected error: {e}")

    return None


# Utility functions

def clean_text(text):
    if not text:
        return "N/A"

    text = html.unescape(text)

    result = []
    inside_tag = False

    for char in text:
        if char == "<":
            inside_tag = True
        elif char == ">":
            inside_tag = False
        elif not inside_tag:
            result.append(char)

    return "".join(result).strip()


def print_line():
    print("-" * 70)


def pause():
    input("\nPress Enter to continue...")


def format_runtime(runtime):
    if runtime:
        return f"{runtime} minutes"
    return "N/A"


# 1. Search TV Show

def search_show():
    query = input("\nEnter TV show name: ").strip()

    if not query:
        print("Please enter a show name.")
        return None

    params = {
        "q": query
    }

    results = make_request("/search/shows", params)

    if not results:
        print("\nNo shows found.")
        return None

    print("\n" + "=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)

    for index, item in enumerate(results, start=1):
        show = item.get("show", {})

        print(f"\n{index}. {show.get('name', 'N/A')}")
        print(f"   ID       : {show.get('id', 'N/A')}")
        print(f"   Type     : {show.get('type', 'N/A')}")
        print(f"   Language : {show.get('language', 'N/A')}")
        print(f"   Status   : {show.get('status', 'N/A')}")
        print(f"   Premiered: {show.get('premiered', 'N/A')}")
        print(f"   Rating   : {show.get('rating', {}).get('average', 'N/A')}")

    print_line()

    try:
        choice = int(input("Select a show number (0 to cancel): "))

        if choice == 0:
            return None

        if 1 <= choice <= len(results):
            selected_show = results[choice - 1]["show"]

            print(f"\nSelected: {selected_show['name']}")
            return selected_show

        print("Invalid selection.")

    except ValueError:
        print("Please enter a valid number.")

    return None


# 2. Display Show Details

def display_show_details(show):
    if not show:
        print("\nNo show selected.")
        return

    print("\n" + "=" * 70)
    print("SHOW DETAILS")
    print("=" * 70)

    print(f"Name : {show.get('name', 'N/A')}")
    print(f"ID : {show.get('id', 'N/A')}")
    print(f"Type : {show.get('type', 'N/A')}")
    print(f"Language : {show.get('language', 'N/A')}")
    print(f"Genres : {', '.join(show.get('genres', [])) or 'N/A'}")
    print(f"Status : {show.get('status', 'N/A')}")
    print(f"Premiered : {show.get('premiered', 'N/A')}")
    print(f"Ended : {show.get('ended', 'N/A')}")
    print(f"Runtime : {format_runtime(show.get('runtime'))}")
    print(f"Average Runtime: {format_runtime(show.get('averageRuntime'))}")

    rating = show.get("rating", {})
    print(f"Rating     : {rating.get('average', 'N/A')}")

    network = show.get("network")

    if network:
        print(f"Network : {network.get('name', 'N/A')}")
    else:
        web_channel = show.get("webChannel")

        if web_channel:
            print(f"Web Channel: {web_channel.get('name', 'N/A')}")

    print(f"\nSummary:")
    print(clean_text(show.get("summary")))

    official_site = show.get("officialSite")

    if official_site:
        print(f"\nOfficial Site: {official_site}")

    print_line()


# 3. Display Episodes

def display_episodes(show):
    if not show:
        print("\nNo show selected.")
        return

    show_id = show["id"]

    episodes = make_request(
        f"/shows/{show_id}/episodes"
    )

    if not episodes:
        print("\nNo episodes found.")
        return

    print("\n" + "=" * 70)
    print(f"EPISODES - {show['name']}")
    print("=" * 70)

    current_season = None

    for episode in episodes:

        season = episode.get("season", "N/A")

        if season != current_season:
            current_season = season
            print(f"\nSeason {season}")

        print(f"S{season:02}E{episode.get('number', 0):02} | {episode.get('name', 'N/A')}")

        print(f"Airdate: {episode.get('airdate', 'N/A')} | Runtime: {episode.get('runtime', 'N/A')} min")

    print_line()


# 4. Display Cast

def display_cast(show):
    if not show:
        print("\nNo show selected.")
        return

    show_id = show["id"]

    cast = make_request(
        f"/shows/{show_id}/cast"
    )

    if not cast:
        print("\nNo cast information found.")
        return

    print("\n" + "=" * 70)
    print(f"CAST - {show['name']}")
    print("=" * 70)

    for index, item in enumerate(cast, start=1):

        person = item.get("person", {})
        character = item.get("character", {})

        print(f"{index}. {person.get('name', 'N/A')}")

        print(f"Character: {character.get('name', 'N/A')}")

    print_line()


# 5. Find Episode by Season / Number

def find_episode(show):
    if not show:
        print("\nNo show selected.")
        return

    try:
        season = int(input("Enter season number: "))
        number = int(input("Enter episode number: "))

        episode = make_request(
            f"/shows/{show['id']}/episodebynumber",{"season": season,"number": number})

        if not episode:
            return

        print("\n" + "=" * 70)
        print("EPISODE DETAILS")
        print("=" * 70)

        print(f"Show : {show['name']}")
        print(f"Season : {episode.get('season', 'N/A')}")
        print(f"Episode : {episode.get('number', 'N/A')}")
        print(f"Title : {episode.get('name', 'N/A')}")
        print(f"Air Date : {episode.get('airdate', 'N/A')}")
        print(f"Air Time : {episode.get('airtime', 'N/A')}")
        print(f"Runtime : {episode.get('runtime', 'N/A')} minutes")

        print("\nSummary:")
        print(clean_text(episode.get("summary")))

        print_line()

    except ValueError:
        print("Season and episode must be numbers.")


# 6. Search Person

def search_person():
    query = input("\nEnter person's name: ").strip()

    if not query:
        print("Please enter a name.")
        return

    results = make_request(
        "/search/people",
        {"q": query}
    )

    if not results:
        print("\nNo people found.")
        return

    print("\n" + "=" * 70)
    print("PEOPLE SEARCH RESULTS")
    print("=" * 70)

    for index, item in enumerate(results, start=1):

        person = item.get("person", {})

        print(f"\n{index}. {person.get('name', 'N/A')}")
        print(f"ID : {person.get('id', 'N/A')}")
        print(f"Country   : {person.get('country').get('name') if person.get('country') else 'N/A'}")
        print(f"Birthday : {person.get('birthday', 'N/A')}")
        print(f"Gender : {person.get('gender', 'N/A')}")

        print(
            f"Department: {person.get('department', 'N/A')}"
        )

    print_line()


# 7. Similar Shows

def similar_shows(show):
    """
    TVmaze does not provide a dedicated /similar endpoint.

    We use the show's genres and search the TVmaze show database
    to find approximate matches.
    """

    if not show:
        print("\nNo show selected.")
        return

    genres = show.get("genres", [])

    if not genres:
        print("\nThis show has no genres to compare.")
        return

    print("\nSearching for similar shows...")

    # Use the first genre as a search keyword.
    results = make_request(
        "/shows",
        {"page": 0}
    )

    if not results:
        print("\nUnable to retrieve shows.")
        return

    matching_shows = []

    for candidate in results:

        if candidate.get("id") == show.get("id"):
            continue

        candidate_genres = candidate.get("genres", [])

        common_genres = set(genres).intersection(set(candidate_genres))

        if common_genres:
            matching_shows.append((candidate, len(common_genres)))

    matching_shows.sort(key=lambda x: x[1],reverse=True)

    print("\n" + "=" * 70)
    print(f"SIMILAR SHOWS TO: {show['name']}")
    print("=" * 70)

    if not matching_shows:
        print("No similar shows found.")
        return

    for index, (candidate, common_count) in enumerate(matching_shows[:10],start=1):

        print(f"{index}. {candidate.get('name', 'N/A')}")

        print(
            f"Genres : {', '.join(candidate.get('genres', [])) or 'N/A'}")

        print(f"Rating : {candidate.get('rating', {}).get('average', 'N/A')}")

    print_line()


# 8. Schedule

def display_schedule():
    print("\nSCHEDULE")

    country = input(
        "Enter country code (default US): "
    ).strip().upper()

    if not country:
        country = "US"

    schedule_date = input(
        "Enter date YYYY-MM-DD "
        "(press Enter for today): "
    ).strip()

    if not schedule_date:
        schedule_date = date.today().isoformat()

    schedule = make_request(
        "/schedule",
        {
            "country": country,
            "date": schedule_date
        }
    )

    if not schedule:
        print("\nNo schedule found.")
        return

    print("\n" + "=" * 70)
    print(
        f"SCHEDULE - {country} - {schedule_date}"
    )
    print("=" * 70)

    for episode in schedule:

        show = episode.get("show", {})

        print(
            f"\n{episode.get('airtime', 'N/A')} - "
            f"{show.get('name', 'N/A')}"
        )

        print(
            f"S{episode.get('season', 'N/A'):02}"
            f"E{episode.get('number', 'N/A'):02} - "
            f"{episode.get('name', 'N/A')}"
        )

        print(
            f"   Channel: "
            f"{show.get('network', {}).get('name', 'N/A')}"
        )

    print_line()


# Main Menu

def show_menu():
    print("\n")
    print("=" * 70)
    print("TV SHOW EXPLORER")
    print("=" * 70)

    print("1. Search TV Show")
    print("2. Display Show Details")
    print("3. Display Episodes")
    print("4. Display Cast")
    print("5. Find Episode by Season/Number")
    print("6. Search Person")
    print("7. Similar Shows")
    print("8. Schedule")
    print("9. Exit")

    print("=" * 70)


def main():

    selected_show = None

    print("\nWelcome to TV Show Explorer!")

    while True:

        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            selected_show = search_show()

            if selected_show:
                pause()

        elif choice == "2":

            display_show_details(selected_show)
            pause()

        elif choice == "3":

            display_episodes(selected_show)
            pause()

        elif choice == "4":

            display_cast(selected_show)
            pause()

        elif choice == "5":

            find_episode(selected_show)
            pause()

        elif choice == "6":

            search_person()
            pause()

        elif choice == "7":

            similar_shows(selected_show)
            pause()

        elif choice == "8":

            display_schedule()
            pause()

        elif choice == "9":

            print("\nThank you for using TV Show Explorer!")
            print("Goodbye!")
            break

        else:

            print("\nInvalid choice. Please select 1-9.")


# Program starts here

if __name__ == "__main__":
    main()