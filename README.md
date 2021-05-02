# Xenoblade Gift Optimizer

In Xenoblade Chronicles, you'll want to make the best use of gifts in order to get the most out of any gift you can make.

This script allows you to optimize your gift donation by telling you for any given character which gifts can be optimally given to them. This means that no other character will get a bigger affinity boost from getting it.

The tool is pretty easy to use.

```
usage: get_best_gift.py [-h] [--any] {shulk,reyn,fiora,dunban,sharla,riki,melia}

Print the gift that are best for any character. Best means that a gift will yield the biggest bonus for all character.

positional arguments:
  {shulk,reyn,fiora,dunban,sharla,riki,melia}
                        Name of the character. Can be one of: shulk, reyn, fiora, dunban, sharla, riki, melia

optional arguments:
  -h, --help            show this help message and exit
  --any                 If set, this prints any gifts that give bonus to a relationship instead of only the best.
```

For example to get the best gifts for Fiora, type `python get_best_gifts.py fiora`. If you are in the endgame and are not looking for giving the best gift but any gift, as long as it boosts affinity, add `-any`.

The affinity scores were extracted from https://game8.co/games/Xenoblade-Chronicles-Definitive-Edition/archives/289015
