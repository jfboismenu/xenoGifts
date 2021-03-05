from dataclasses import dataclass
import sys

CHARACTERS = "Shulk Reyn Fiora Dunban Sharla Riki Melia".lower().split()

@dataclass(order=True)
class Gift():
    item_name: str
    location: str
    category: str
    affinities: str

def read_gifts():
    gifts = []
    for line in open("gifts.txt", "rt"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("Category:"):
            category = line.replace("Category:", "").strip()
            continue

        tokens = line.split()
        if len(tokens) >= 7:
            affinities = dict(
                zip(
                    CHARACTERS,
                    (int(t) for t in tokens[-7:])
                )
            )
            region = " ".join(tokens[:-7])
            gifts.append(
                Gift(
                    item_name,
                    region,
                    category,
                    affinities
                )
            )
        else:
            item_name = " ".join(tokens)

    return gifts


gifts = read_gifts()
character = sys.argv[1]

if "sort" in sys.argv:
    sys.argv.remove("sort")
    sort_by_name = True
else:
    sort_by_name = False

if "best" in sys.argv:
    sys.argv.remove("best")
    keep_only_if_best = True
else:
    keep_only_if_best = False

if len(sys.argv) == 3:
    category = sys.argv[2]
else:
    category = None

gifts = filter(lambda gift: int(gift.affinities[character]) > 0, gifts)

def is_best(gift):
    affinity = gift.affinities[character]
    for other_char, other_affinity in gift.affinities.items():
        if other_char == character:
            continue
        if other_affinity > affinity:
            return False

    return True


if category:
    gifts = filter(lambda gift: gift.category.lower() == category.lower(), gifts)

if keep_only_if_best:
    gifts = filter(is_best, gifts)

def sorter(gift):
    return 

if sort_by_name:
    gifts = sorted(gifts, key=lambda gift: gift.item_name)
else:
    gifts = sorted(gifts, key=lambda gift: int(gift.affinities[character]))

for gift in gifts:
    print(", ".join((gift.item_name, gift.category, gift.location, str(gift.affinities))))
