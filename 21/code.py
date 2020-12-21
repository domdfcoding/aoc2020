"""
--- Day 21: Allergen Assessment ---

You reach the train's last stop and the closest you can get to your vacation island without getting wet.
There aren't even any boats here, but nothing can stop you now: you build a raft.
You just need a few days' worth of food for your journey.

You don't speak the local language, so you can't read any ingredients lists.
However, sometimes, allergens are listed in a language you do understand.
You should be able to use this information to determine which ingredient contains
which allergen and work out which foods are safe to take with you on your trip.

You start by compiling a list of foods (your puzzle input), one food per line.
Each line includes that food's ingredients list followed by some or all of the allergens the food contains.

Each allergen is found in exactly one ingredient.
Each ingredient contains zero or one allergen.
Allergens aren't always marked; when they're listed (as in ``(contains nuts, shellfish)`` after an ingredients list),
the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list.
However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present:
maybe they forgot to label it, or maybe it was labeled in a language you don't know.

For example, consider the following list of foods::

	mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
	trh fvjkl sbzzf mxmxvkd (contains dairy)
	sqjhc fvjkl (contains soy)
	sqjhc mxmxvkd sbzzf (contains fish)

The first food in the list has four ingredients (written in a language you don't understand):
``mxmxvkd``, ``kfcds``, ``sqjhc``, and ``nhms``.
While the food might contain other allergens, a few allergens the food definitely contains are listed afterward:
``dairy`` and ``fish``.

The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list.
In the above example, none of the ingredients ``kfcds``, ``nhms``, ``sbzzf``, or ``trh`` can contain an allergen.
Counting the number of times any of these ingredients appear in any ingredients list produces ``5``:
they all appear once each except ``sbzzf``, which appears twice.

Determine which ingredients cannot possibly contain any of the allergens in your list.
How many times do any of those ingredients appear?
"""

# stdlib
import re
from collections import Counter
from itertools import chain
from operator import itemgetter
from typing import Dict, List, NamedTuple

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import DelimitedList

# ==========================
print("Part One")
# ==========================

foods = [x for x in PathPlus("input.txt").read_lines() if x]


class Food(NamedTuple):
	allergens: List[str]
	ingredients: List[str]

	@classmethod
	def parse(cls, string: str):
		m = re.match(r"^([a-z ]*) \(contains ([a-z ,]*)\)$", string)
		ingredients = m.group(1).split(' ')
		allergens = m.group(2).split(", ")
		return cls(allergens, ingredients)


all_foods = [Food.parse(food) for food in foods]
all_allergens = sorted(set(chain.from_iterable(food.allergens for food in all_foods)))
allergen_possibilities: Dict[str, List[str]] = {}

for allergen in all_allergens:

	all_ingredients = []
	matching_foods = 0

	for food in all_foods:
		if allergen in food.allergens:
			assert max(Counter(food.ingredients).values()) == 1
			# print(food)
			all_ingredients.extend(food.ingredients)
			matching_foods += 1

	allergen_possibilities[allergen] = [k for k, v in Counter(all_ingredients).items() if v == matching_foods]

# print(allergen_possibilities)

finalised_allergens = {}

while True:
	for field_name, candidate_indices in allergen_possibilities.items():
		if len(candidate_indices) == 1:
			new_allergen_possibilities = {}
			for key, value in allergen_possibilities.items():
				if key == field_name:
					continue

				if candidate_indices[0] in value:
					value.remove(candidate_indices[0])
				new_allergen_possibilities[key] = value

			finalised_allergens[candidate_indices[0]] = field_name
			allergen_possibilities = new_allergen_possibilities
			break
	else:
		break

# print(finalised_allergens)
assert sorted(finalised_allergens.values()) == all_allergens
assert not allergen_possibilities

non_allergen_ingredients = 0

for ingredient, frequency in Counter(chain.from_iterable(food.ingredients for food in all_foods)).items():
	if ingredient in finalised_allergens:
		continue
	else:
		non_allergen_ingredients += frequency

print("The number of times ingredients which aren't allergens appear is:", non_allergen_ingredients)  # 2203

# ==========================
print("\nPart Two")
# ==========================
"""
Now that you've isolated the inert ingredients, you should have enough information to figure out which ingredient
contains which allergen.

In the above example:

- ``mxmxvkd`` contains dairy.
- ``sqjhc`` contains fish.
- ``fvjkl`` contains soy.

Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your
canonical dangerous ingredient list.
(There should not be any spaces in your canonical dangerous ingredient list.)
In the above example, this would be ``mxmxvkd,sqjhc,fvjkl``.

Time to stock your raft with supplies. What is your canonical dangerous ingredient list?
"""

sorted_allergens = sorted(finalised_allergens.items(), key=itemgetter(1))
dengerous_ingredient_list = DelimitedList(map(itemgetter(0), sorted_allergens))
print(
		f"The dangerous allergens are: {dengerous_ingredient_list:,}"
		)  # fqfm,kxjttzg,ldm,mnzbc,zjmdst,ndvrq,fkjmz,kjkrm
