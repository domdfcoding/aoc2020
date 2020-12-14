"""
--- Day 7: Handy Haversacks ---

You land at the regional airport in time for your next flight.
In fact, it looks like you'll even have time to grab some food:
all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents;
bags must be color-coded and must contain specific quantities of other color-coded bags.
Apparently, nobody responsible for these regulations considered how long they would take to enforce!.

For example, consider the following rules::

	light red bags contain 1 bright white bag, 2 muted yellow bags.
	dark orange bags contain 3 bright white bags, 4 muted yellow bags.
	bright white bags contain 1 shiny gold bag.
	muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
	shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
	dark olive bags contain 3 faded blue bags, 4 dotted black bags.
	vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
	faded blue bags contain no other bags.
	dotted black bags contain no other bags.

These rules specify the required contents for 9 bag types.
In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags
(5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag.
If you wanted to carry it in at least one other bag,
how many different bag colors would be valid for the outermost bag?
(In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

- A bright white bag, which can hold your shiny gold bag directly.
- A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
- A dark orange bag, which can hold bright white and muted yellow bags,
  either of which could then hold your shiny gold bag.
- A light red bag, which can hold bright white and muted yellow bags,
  either of which could then hold your shiny gold bag.

So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag?
(The list of rules is quite long; make sure you get all of it.)
"""

# stdlib
import functools
import re
from typing import List

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

rules = [x for x in PathPlus("input.txt").read_lines() if x]

bags_re = re.compile(r"([a-z ]*) bags contain ((?:[0-9] [a-z ]*? (?:bag|bags)(?:, |\.))*)")
delimiter_re = re.compile("[,.]")
num_bags_re = re.compile("([0-9]) ([a-z ]*) (?:bag|bags)")

bags = {}

for rule in rules:
	m = bags_re.match(rule)

	if m:
		bag_colour = m.group(1)
		bag_contents = list(filter(bool, delimiter_re.split(m.group(2))))

		if bag_colour in bags:
			raise ValueError("Duplicate bag!")

		bags[bag_colour] = bag_contents

for colour, contents in bags.items():
	flat_contents = []

	for inner_bag in contents:
		# print(inner_bag)
		m = num_bags_re.match(inner_bag.strip())
		if m:
			flat_contents.extend([m.group(2)] * int(m.group(1)))

	bags[colour] = flat_contents

shiny_gold_contents = bags.pop("shiny gold")


@functools.lru_cache(594)
def get_contents(colour: str) -> List[str]:
	contents = bags[colour]

	flat_contents = []

	for inner_bag in contents:
		if inner_bag == "shiny gold":
			flat_contents.append(inner_bag)
		else:
			flat_contents.extend(get_contents(inner_bag))

	return flat_contents


valid_bags = 0

for colour in bags:
	contents = get_contents(colour)
	# print(colour, sorted(set(contents)))
	if contents:
		valid_bags += 1

print(f"{valid_bags} bags contain at least one shiny gold bag.")  # 161

# ==========================
print("\nPart Two")
# ==========================
"""
It's getting pretty expensive to fly these days - not because of ticket prices,
but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example::

	faded blue bags contain 0 other bags.
	dotted black bags contain 0 other bags.
	vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
	dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.

So, a single shiny gold bag must contain ``1`` dark olive bag (and the 7 bags within it)
plus 2 vibrant plum bags (and the ``11`` bags within each of those): ``1 + 1*7 + 2 + 2*11 = 32`` bags!

Of course, the actual rules have a small chance of going several levels deeper than this example;
be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example::

	shiny gold bags contain 2 dark red bags.
	dark red bags contain 2 dark orange bags.
	dark orange bags contain 2 dark yellow bags.
	dark yellow bags contain 2 dark green bags.
	dark green bags contain 2 dark blue bags.
	dark blue bags contain 2 dark violet bags.
	dark violet bags contain no other bags.

In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
"""


@functools.lru_cache(594)
def get_contents_v2(colour: str) -> List[str]:
	contents = bags[colour]

	total_contents = []

	for inner_bag in contents:
		total_contents.append(inner_bag)
		total_contents.extend(get_contents_v2(inner_bag))

	return total_contents


total_contents = []

for bag in shiny_gold_contents:
	total_contents.append(bag)
	total_contents.extend(get_contents_v2(bag))

print(f"A shiny gold bag contains {len(total_contents)} bags!")  # 30899
