import json
from operator import itemgetter

matches = {}
relative_elo_values = {}
elo_values = {}
k = 40

jsonFile = "db.json"


with open(jsonFile, 'r') as file:
    elo_list = json.load(file)

print(elo_list)

#elo_list = [{"name": "A", "rating": 1309, "matches": 2}, {"name": "B", "rating": 1467, "matches": 4}, {"name": "C", "rating": 1345, "matches": 3}]


def elo_probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * pow(10, 1.0 * (rating1 - rating2) / 400))


def elo_rating(player_a, player_b, k, d):
    b_win_probability = elo_probability(player_a["rating"], player_b["rating"])
    a_win_probability = elo_probability(player_b["rating"], player_a["rating"])

    print(player_a["name"] + ": " + str(round(a_win_probability, 2)) + ", " + player_b["name"] + ": " + str(round(b_win_probability, 2)))

    if d == "a_win":
        player_a_change = k * (1 - a_win_probability)
        player_b_change = k * (0 - b_win_probability)
        player_a["rating"] += player_a_change
        player_b["rating"] += player_b_change

    elif d == "b_win":
        player_a_change = k * (0 - a_win_probability)
        player_b_change = k * (1 - b_win_probability)
        player_a["rating"] += player_a_change
        player_b["rating"] += player_b_change

    return player_a, player_b


def get_next_match(lst):
    i = 0

    for item in lst:
        matches[i] = item["matches"]

        i += 1

    lowest_match_index = min(matches, key=matches.get)
    player_a = lst[lowest_match_index]

    i = 0
    for item in lst:
        relative_elo_values[i] = abs(player_a["rating"] - item["rating"])

        i += 1

    del relative_elo_values[lowest_match_index]

    closest_match_index = min(relative_elo_values, key=relative_elo_values.get)
    player_b = lst[closest_match_index]

    return player_a, player_b


def sort_elo(lst):
    for item in lst:
        elo_values[item["name"]] = item["rating"]

    sorted_list = sorted(elo_values.items(), key=itemgetter(1), reverse=True)

    i = 1
    for item in sorted_list:
        print(str(i) + ". " + str(item))
        i += 1


sort_elo(elo_list)


while True:
    player_a, player_b = get_next_match(elo_list)

    print("\nOption 1: " + player_a["name"] + "\nOption 2: " + player_b["name"])
    response = input("Who is better? ")
    if response == "n":
        break

    if response == "1":
        player_a, player_b = elo_rating(player_a, player_b, k, d="a_win")
    elif response == "2":
        player_a, player_b = elo_rating(player_a, player_b, k, d="b_win")
    else:
        print("Error with input")
        break

    player_a["matches"] += 1
    player_b["matches"] += 1

    print(player_a["name"] + " elo: " + str(round(player_a["rating"], 2)))
    print(player_b["name"] + " elo: " + str(round(player_b["rating"], 2)))

with open(jsonFile, 'w') as file:
    json.dump(elo_list, file, indent=2)