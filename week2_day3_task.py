# 1:
def sorting_hat(name, signals):
    signals = signals.lower()

    houses = {
        "g": "Gryffindor",
        "h": "Hufflepuff",
        "r": "Ravenclaw",
        "s": "Slytherin"
    }

    counts = {}
    for key in houses:
        counts[key] = signals.count(key)

    max_count = max(counts.values())

    winners = []
    for k in counts:
        if counts[k] == max_count:
            winners.append(k)
    house = min(winners)

    print(f"{name}, you belong in {houses[house]}! ({max_count} signals)")


sorting_hat("Neville", "gGhrGsgH")


# 2:
def rush_hour_report(logs):
    totalCups = sum(logs)
    avg_per_hour = totalCups / len(logs)

    rush_hours = []

    for i in range(len(logs)):
        if logs[i] > avg_per_hour:
            rush_hours.append(i)

    print(f"Total: {totalCups} cups | Average: {avg_per_hour:.1f}/hr")
    print("Rush hours (above average):", end=" ")

    for i in rush_hours:
        print(f"{i+8}AM", end=", ")

rush_hour_report([12, 5, 8, 20, 3, 15, 22])

# 3:
def villains_report(goblin, octopus, vulture):
    g = set(goblin)
    o = set(octopus)
    v = set(vulture)

    # (a) In all three sets
    contested = g & o & v

    # (b) In exactly one set
    exactly_one = (g - o - v) | (o - g - v) | (v - g - o)

    # (c) Total distinct neighborhoods
    distinct = len(g | o | v)

    print(f"\n\nContested by all three: {contested}")
    print(f"Controlled by exactly one:{exactly_one}")
    print(f"Distinct neighborhoods: {distinct}\n")

villains_report(goblin = ["Queens", "Manhattan",
"Brooklyn", "Bronx"],
octopus = ["Manhattan", "Brooklyn",
"Harlem"],
vulture = ["Manhattan", "Bronx",
"Harlem"]
)

#4:
def integrity_sweep(targets):
    valid = []

    for codename, lat, lon in targets:
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            print(f"INVALID: {codename} ({lat}, {lon})")
        else:
            valid.append((codename, lat, lon))

    valid.sort(key=lambda x: x[1], reverse=True)

    print("Briefing (N > S):")
    for codename, lat, lon in valid:
        print(f"{codename.upper()} > Lat: {lat}, Lon: {lon}")

    print("Why tuples?")
    print("Tuples are immutable, so a target's coordinates cannot be accidentally modified after they are created.\n")

integrity_sweep([("Falcon", 34.05, -118.24), ("Ghost",
99.9, 12.0), ("Condor", 40.71, -74.00)])

#5:
def smart_billing_engine(bills):
    print("Line totals (incl. GST):", end=" ")
    res = list(map(lambda bill: bill[1] * bill[2] * 1.05, bills))
    print(res)
    print(f"Grand Total: {sum(res)}\n")

smart_billing_engine([("Masala Chai", 3, 20), ("Samosa", 2,
15), ("Green Tea", 1, 30)])

#6:
def knockout_qualification(points_record):
    teams = list(map(lambda x :(x[0], x[1]*3 + x[2]*1, x[3]), points_record))
    qualifying = list(filter(lambda x : x[1] >= 6 and x[2]<=1, teams))
    qualifying.sort(key=lambda x: x[1], reverse=True)
    print("Advancing to knockouts:")
    for team, points, losses in qualifying:
        print(f"{team} - {points} pts")
    print("\n")

knockout_qualification([("Brazil", 3, 0, 0), ("Japan", 1, 2,
0), ("Spain", 2, 0, 1), ("Ghana", 0, 1,
2)])

#7:
def award_points(house, points=10, reason="general excellence", ledger=None):
    # Using ledger={} would be dangerous because the same dictionary would be reused across all function calls, causing unwanted accumulation.

    if ledger is None:
        ledger = {}

    if house not in ledger:
        ledger[house] = 0

    ledger[house] += points

    print(f"{house} +{points} ({reason}) >")
    print(f"total {ledger[house]}")

    return ledger


led = award_points("Gryffindor")
led = award_points("Gryffindor", 50, "defeating a troll", led)
led = award_points("Gryffindor", 50, "defeating a troll", led)
led = award_points("Slytherin", 30, ledger=led)

print(f"Final ledger: {led}\n")

#8:
def launch(*stages, abort_threshold=5000):
    cumulative = 0
    curr_stage = 0
    for i in stages:
        cumulative += stages[curr_stage]
        curr_stage += 1
        print(f"Stage {curr_stage} armed > cumulative {cumulative} kg")
        if cumulative > abort_threshold:
            print(f"[ABORT] at stage {curr_stage}: threshold {abort_threshold} kg exceeded.\n")
            return
    print(f"Total Mass: {cumulative}, Stage Count: {curr_stage}\n")

launch(1200, 1800, 2500, 900)

#9:
def create_hero(name, *powers, **stats):
    print(f"Hero: {name}")
    print(f"Powers: ", end=" ")
    for i in powers:
        print(i)
    print(f"\nStats:")
    for k, v in stats.items():
        print(f"{k} : {v}")
    overall_rating = sum(stats.values())/len(stats)
    print(f"Overall Rating: {overall_rating:.1f}", end=" ")
    if overall_rating > 90:
        print(" > S-Tier *\n")

create_hero("Spider-Man", "wall-crawl",
"spider-sense",
strength=85, agility=95,
intelligence=92)

#10:
def inventory_report(inventory, gst=0.05, **filters):
    categories = []

    for item, category, stock, price in inventory:
        categories.append(category)

    categories = sorted(set(categories))

    print(categories)

    print("Categories:", categories)

    low_stock = list(filter(lambda x: x[2] < 10, inventory))
    reorder_items = []
    for item, category, stock, price in low_stock:
            reorder_items.append(item)

    print("[!] Reorder soon (stock < 10):", reorder_items)

    prices_with_gst = dict(
        map(lambda x: (x[0], x[3] * (1 + gst)),inventory))

    print("Prices incl. GST:", prices_with_gst)

    matches = []

    for item, category, stock, price in inventory:
        match = True

        if "category" in filters and category != filters["category"]:
            match = False

        if "max_price" in filters and price != filters["max_price"]:
            match = False

        if "stock" in filters and stock != filters["stock"]:
                match = False

        if "item" in filters and item != filters["item"]:
                    match = False

        if match:
            matches.append(item)

    print(f"Matching filters {filters}:", matches)

    return matches

inv = [
("Masala Chai", "Tea", 5, 20),
("Green Tea", "Tea", 15, 30),
("Samosa", "Snack", 8, 15),
("Biscuit", "Snack", 25, 10),
]
inventory_report(inv, category="Snack",
max_price=15)
# inventory_report(inv, item="Samosa")