"""
--- Day 24: Lobby Layout ---

Your raft makes it to the tropical island; it turns out that the small crab was an excellent navigator.
You make your way to the resort.

As you enter the lobby, you discover a small problem: the floor is being renovated.
You can't even reach the check-in desk until they've finished installing the new tile floor.

The tiles are all hexagonal; they need to be arranged in a hex grid with a very specific color pattern.
Not in the mood to wait, you offer to help figure out the pattern.

The tiles are all white on one side and black on the other.
They start with the white side facing up.
The lobby is large enough to fit whatever pattern might need to appear there.

A member of the renovation crew gives you a list of the tiles that need to be flipped over (your puzzle input).
Each line in the list identifies a single tile that needs to be flipped by giving a series of steps
starting from a reference tile in the very center of the room.
(Every line starts from the same reference tile.)

Because the tiles are hexagonal, every tile has six neighbors:
east, southeast, southwest, west, northwest, and northeast.
These directions are given in your list, respectively, as ``e``, ``se``, ``sw``, ``w``, ``nw``, and ``ne``.
A tile is identified by a series of these directions with no delimiters;
for example, ``esenee`` identifies the tile you land on if you start at the reference tile
and then move one tile east, one tile southeast, one tile northeast, and one tile east.

Each time a tile is identified, it flips from white to black or from black to white.
Tiles might be flipped more than once.
For example, a line like ``esew`` flips a tile immediately adjacent to the reference tile,
and a line like ``nwwswee`` flips the reference tile itself.

Here is a larger example::

	sesenwnenenewseeswwswswwnenewsewsw
	neeenesenwnwwswnenewnwwsewnenwseswesw
	seswneswswsenwwnwse
	nwnwneseeswswnenewneswwnewseswneseene
	swweswneswnenwsewnwneneseenw
	eesenwseswswnenwswnwnwsewwnwsene
	sewnenenenesenwsewnenwwwse
	wenwwweseeeweswwwnwwe
	wsweesenenewnwwnwsenewsenwwsesesenwne
	neeswseenwwswnwswswnw
	nenwswwsewswnenenewsenwsenwnesesenew
	enewnwewneswsewnwswenweswnenwsenwsw
	sweneswneswneneenwnewenewwneswswnese
	swwesenesewenwneswnwwneseswwne
	enesenwswwswneneswsenwnewswseenwsese
	wnwnesenesenenwwnenwsewesewsesesew
	nenewswnwewswnenesenwnesewesw
	eneswnwswnwsenenwnwnwwseeswneewsenese
	neswnwewnwnwseenwseesewsenwsweewe
	wseweeenwnesenwwwswnew

In the above example, 10 tiles are flipped once (to black), and 5 more are flipped twice (to black, then back to white).
After all of these instructions have been followed, a total of ``10`` tiles are black.

Go through the renovation crew's list and determine which tiles they need to flip.
After all of the instructions have been followed, how many tiles are left with the black side up?
"""

# stdlib
from collections import Counter
from typing import List, Tuple

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

instructions = [x for x in PathPlus("input.txt").read_lines() if x]

flipped_tiles: List[Tuple[int, int]] = []

for instruction in instructions:
	x_pos = 0
	y_pos = 0

	for idx, char in enumerate(instruction):
		if char == 'e':
			if instruction[idx - 1] == 's':
				y_pos -= 1

			elif instruction[idx - 1] == 'n':
				y_pos += 1
				x_pos += 1

			else:
				x_pos += 1

		elif char == 'w':
			if instruction[idx - 1] == 's':
				y_pos -= 1
				x_pos -= 1

			elif instruction[idx - 1] == 'n':
				y_pos += 1

			else:
				x_pos -= 1

	flipped_tiles.append((x_pos, y_pos))

black_tiles = []

for tile, flips in Counter(flipped_tiles).items():
	if flips % 2:
		black_tiles.append(tile)

print(f"{len(black_tiles)} tiles were turned to black.")  # 459

# ==========================
print("\nPart Two")
# ==========================
"""
The tile floor in the lobby is meant to be a living art exhibit. #
Every day, the tiles are all flipped according to the following rules:

- Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
- Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.

Here, tiles immediately adjacent means the six tiles directly touching the tile in question.

The rules are applied simultaneously to every tile; put another way,
it is first determined which tiles need to be flipped,
then they are all flipped at the same time.

In the above example, the number of black tiles that are facing up
after the given number of days has passed is as follows:

	Day 1: 15
	Day 2: 12
	Day 3: 25
	Day 4: 14
	Day 5: 23
	Day 6: 28
	Day 7: 41
	Day 8: 37
	Day 9: 49
	Day 10: 37

	Day 20: 132
	Day 30: 259
	Day 40: 406
	Day 50: 566
	Day 60: 788
	Day 70: 1106
	Day 80: 1373
	Day 90: 1844
	Day 100: 2208

After executing this process a total of 100 times, there would be ``2208`` black tiles facing up.

How many tiles will be black after 100 days?
"""


def get_adjacent_tiles(x: int, y: int):
	yield x, y + 1
	yield x, y - 1
	yield x + 1, y
	yield x - 1, y
	yield x + 1, y + 1
	yield x - 1, y - 1


def flip_tiles(current_black_tiles: List[Tuple[int, int]]):
	new_black_tiles: List[Tuple[int, int]] = []

	for tile in current_black_tiles:
		adjacent_tiles = list(get_adjacent_tiles(*tile))

		adjacent_blacks = []
		adjacent_whites = []

		for adjacent_tile in adjacent_tiles:
			if adjacent_tile in current_black_tiles:
				adjacent_blacks.append(adjacent_tile)
			else:
				adjacent_whites.append(adjacent_tile)

		if len(adjacent_blacks) in (1, 2):
			new_black_tiles.append(tile)

		for white_tile in adjacent_whites:
			whites_adjacent_tiles = list(get_adjacent_tiles(*white_tile))

			whites_adjacent_blacks = []

			for whites_adjacent_tile in whites_adjacent_tiles:
				if whites_adjacent_tile in current_black_tiles:
					whites_adjacent_blacks.append(whites_adjacent_tile)

			if len(whites_adjacent_blacks) == 2:
				new_black_tiles.append(white_tile)

	return sorted(set(new_black_tiles))


for day in range(100):
	black_tiles = flip_tiles(black_tiles)
	# print(f"Day {day + 1}:", len(black_tiles))

print(f"After 100 days there will be {len(black_tiles)} black tiles.")  # 4150
