# -*- coding: utf-8 -*-
from dataclasses import dataclass
import sys
from argparse import ArgumentParser


def main():

    # List of characters you can gift to.
    CHARACTERS = "Shulk Reyn Fiora Dunban Sharla Riki Melia".lower().split()

    parser = ArgumentParser(
        description="""Print the gift that are best for any character.
        Best means that a gift will yield the biggest bonus for all character."""
    )
    parser.add_argument(
        "character",
        type=str,
        help="Name of the character. Can be one of: {}".format(", ".join(CHARACTERS)),
        choices=CHARACTERS,
    )
    parser.add_argument(
        "--any",
        action="store_true",
        default=False,
        help="If set, this prints any gifts that give bonus to a relationship instead of only the best.",
    )

    args = parser.parse_args()

    @dataclass(order=True)
    class Gift:
        """
        This will store a row from gifts.txt
        """

        item_name: str
        location: str
        category: str
        affinities: str

    def read_gifts():
        """
        Read the gift from the resource file.

        Here's a sample of the layout:

        Category: Vegetable
        Sweet Wasabi
        Colony 9    -4  6   8   -10 2   14  -4
        Cool Potato
        Colony 9    2   4   10  2   -10 14  -4
        Red Lettuce
        Colony 9    -8  12  2   2   14  8   -10
        ...

        So the input is

        Category
        Gift
        Location bonus/minuses
        Gift
        Location bonus/minuses
        ...

        Until we reach another category.
        """
        gifts = []
        for line in open("gifts.txt", "rt"):
            # Some lines are empty, so skip those.
            line = line.strip()
            if not line:
                continue

            # There are some comments, skip those
            if line.startswith("#"):
                continue

            # We have a new category, so update the current category.
            if line.startswith("Category:"):
                category = line.replace("Category:", "").strip()
                continue

            # We either have a line with an item name or a location and bonuses/minuses at this point.

            # Split into tokens.
            tokens = line.split()

            # If we have more than 7 tokens, we clearly have a location/bonuses/minuses line.
            if len(tokens) >= 7:
                affinities = dict(
                    # The last 7 items are the bonuses/minuses
                    zip(CHARACTERS, (int(t) for t in tokens[-7:]))
                )
                # Everything before that is the region name.
                region = " ".join(tokens[:-7])
                # Add the new item to the list.
                gifts.append(Gift(item_name, region, category, affinities))
            else:
                # We have an item name, so rejoin the tokens and update the current item name.
                item_name = " ".join(tokens)

        return gifts

    gifts = read_gifts()

    # Drop anything that people hate, we don't want those.
    gifts = filter(lambda gift: int(gift.affinities[args.character]) > 0, gifts)

    def is_best(gift):
        # First, pick the affinity change for the character we're optimising for.
        affinity = gift.affinities[args.character]
        # If one of the characters would get a better boost, then this item is not the
        # best for the selected character.
        for other_char, other_affinity in gift.affinities.items():
            if other_char == args.character:
                continue
            if other_affinity > affinity:
                return False

        # Nobody gets a better boost, this is the best use of the item.
        return True

    # If we don't want any gifts, but only the best, then filter anything that can be better
    # if given to someone else.
    if args.any is False:
        gifts = filter(is_best, gifts)

    # Sort everything by name.
    gifts = sorted(gifts, key=lambda gift: gift.item_name)

    # Print out the items.
    for gift in gifts:
        print(
            ", ".join(
                (gift.item_name, gift.category, gift.location, str(gift.affinities))
            )
        )


main()
