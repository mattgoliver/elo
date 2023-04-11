import json

elo_list = []

names = ["big arms", "corvette buyer", "mr creatine", "mr anime"]

for name in names:
    data = {"name": name, "rating": 1500, "matches": 0}

    elo_list.append(data)

print(elo_list)

with open("db.json", 'w') as file:
    json.dump(elo_list, file, indent=2)