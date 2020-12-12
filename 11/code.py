"""
--- Day 11: Seating System ---

Your plane lands with plenty of time to spare.
The final leg of your journey is a ferry that goes directly to the tropical island
where you can finally start your vacation
As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area,
you're pretty sure you can predict the best place to sit.
You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid.
Each position is either floor (``.``), an empty seat (``L``), or an occupied seat (``#``).
For example, the initial seat layout might look like this::

	L.LL.LL.LL
	LLLLLLL.LL
	L.L.L..L..
	LLLL.LL.LL
	L.LL.LL.LL
	L.LLLLL.LL
	..L.L.....
	LLLLLLLLLL
	L.LLLLLL.L
	L.LLLLL.LL

Now, you just need to model the people who will be arriving shortly.
Fortunately, people are entirely predictable and always follow a simple set of rules.
All decisions are based on the number of occupied seats adjacent to a given seat
(one of the eight positions immediately up, down, left, right, or diagonal from the seat).
The following rules are applied to every seat simultaneously:

- If a seat is empty (``L``) and there are no occupied seats adjacent to it, the seat becomes occupied.
- If a seat is occupied (``#``) and four or more seats adjacent to it are also occupied, the seat becomes empty.
- Otherwise, the seat's state does not change.


Floor (``.``) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

	#.##.##.##
	#######.##
	#.#.#..#..
	####.##.##
	#.##.##.##
	#.#####.##
	..#.#.....
	##########
	#.######.#
	#.#####.##

After a second round, the seats with four or more occupied adjacent seats become empty again:

	#.LL.L#.##
	#LLLLLL.L#
	L.L.L..L..
	#LLL.LL.L#
	#.LL.LL.LL
	#.LLLL#.##
	..L.L.....
	#LLLLLLLL#
	#.LLLLLL.L
	#.#LLLL.##

This process continues for three more rounds:

	#.##.L#.##
	#L###LL.L#
	L.#.#..#..
	#L##.##.L#
	#.##.LL.LL
	#.###L#.##
	..#.#.....
	#L######L#
	#.LL###L.L
	#.#L###.##

::

	#.#L.L#.##
	#LLL#LL.L#
	L.L.L..#..
	#LLL.##.L#
	#.LL.LL.LL
	#.LL#L#.##
	..L.L.....
	#L#LLLL#L#
	#.LLLLLL.L
	#.#L#L#.##

::

	#.#L.L#.##
	#LLL#LL.L#
	L.#.L..#..
	#L##.##.L#
	#.#L.LL.LL
	#.#L#L#.##
	..L.L.....
	#L#L##L#L#
	#.LLLLLL.L
	#.#L#L#.##

At this point, something interesting happens:
the chaos stabilizes and further applications of these rules cause no seats to change state!
Once people stop moving around, you count ``37`` occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state.
How many seats end up occupied?
"""

# stdlib
from collections import Counter
from itertools import chain
from typing import Iterable

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

original_seats = seats = [list(x) for x in PathPlus("input.txt").read_lines() if x]

row_length = len(seats[0])
col_length = len(seats)

EMPTY = 'L'
OCCUPIED = '#'
FLOOR = '.'


def get_adjacent_seats(x: int, y: int) -> Iterable[str]:
	x_min = x - 1
	x_max = x + 1
	y_min = y - 1
	y_max = y + 1

	if x_min < 0:
		x_min = 0
	if y_min < 0:
		y_min = 0

	x_range = range(x_min, x_max + 1)
	y_range = range(y_min, y_max + 1)

	for y_idx in y_range:
		for x_idx in x_range:
			try:
				if y_idx == y and x_idx == x:
					continue

				yield seats[y_idx][x_idx]
			except IndexError:
				pass


iteration = 1

while True:
	changes = 0
	new_seats = []

	for y_idx, row in enumerate(seats):
		new_seats.append([])

		for x_idx, seat in enumerate(row):

			adjacent_seats = Counter(get_adjacent_seats(x_idx, y_idx))

			if seat == EMPTY:
				if not adjacent_seats[OCCUPIED]:
					new_seats[y_idx].append(OCCUPIED)
					changes += 1
					continue
			elif seat == OCCUPIED:
				if adjacent_seats[OCCUPIED] >= 4:
					new_seats[y_idx].append(EMPTY)
					changes += 1
					continue

			new_seats[y_idx].append(seat)

	if seats == new_seats:
		break

	seats = new_seats

	# print("Iteration", iteration, ",", changes, "changes")
	iteration += 1

for row in new_seats:
	print(row)

occupied_seats = Counter(chain.from_iterable(seats))[OCCUPIED]

print(f"After everyone has stopped moving, {occupied_seats} seats are occupied.")  # 2324

# ==========================
print("\nPart Two")
# ==========================
"""
As soon as people start to arrive, you realize your mistake.
People don't just care about adjacent seats - they care about the first seat they
can see in each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats,
consider the first seat in each of those eight directions.
For example, the empty seat below would see eight occupied seats::

	.......#.
	...#.....
	.#.......
	.........
	..#L....#
	....#....
	.........
	#........
	...#.....

The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones::

	.............
	.L.L.#.#.#.#.
	.............

The empty seat below would see no occupied seats::

	.##.##.
	#.#.#.#
	##...##
	...L...
	##...##
	#.#.#.#
	.##.##.

Also, people seem to be more tolerant than you expected:
it now takes five or more visible occupied seats for an occupied seat to become empty
(rather than four or more from the previous rules).
The other rules still apply: empty seats that see no occupied seats become occupied,
seats matching no rule don't change, and floor never changes.

Given the same starting layout as above,
these new rules cause the seating area to shift around as follows::

	L.LL.LL.LL
	LLLLLLL.LL
	L.L.L..L..
	LLLL.LL.LL
	L.LL.LL.LL
	L.LLLLL.LL
	..L.L.....
	LLLLLLLLLL
	L.LLLLLL.L
	L.LLLLL.LL

::

	#.##.##.##
	#######.##
	#.#.#..#..
	####.##.##
	#.##.##.##
	#.#####.##
	..#.#.....
	##########
	#.######.#
	#.#####.##

::

	#.LL.LL.L#
	#LLLLLL.LL
	L.L.L..L..
	LLLL.LL.LL
	L.LL.LL.LL
	L.LLLLL.LL
	..L.L.....
	LLLLLLLLL#
	#.LLLLLL.L
	#.LLLLL.L#

::

	#.L#.##.L#
	#L#####.LL
	L.#.#..#..
	##L#.##.##
	#.##.#L.##
	#.#####.#L
	..#.#.....
	LLL####LL#
	#.L#####.L
	#.L####.L#

::

	#.L#.L#.L#
	#LLLLLL.LL
	L.L.L..#..
	##LL.LL.L#
	L.LL.LL.L#
	#.LLLLL.LL
	..L.L.....
	LLLLLLLLL#
	#.LLLLL#.L
	#.L#LL#.L#

::

	#.L#.L#.L#
	#LLLLLL.LL
	L.L.L..#..
	##L#.#L.L#
	L.L#.#L.L#
	#.L####.LL
	..#.#.....
	LLL###LLL#
	#.LLLLL#.L
	#.L#LL#.L#

::

	#.L#.L#.L#
	#LLLLLL.LL
	L.L.L..#..
	##L#.#L.L#
	L.L#.LL.L#
	#.LLLL#.LL
	..#.L.....
	LLL###LLL#
	#.LLLLL#.L
	#.L#LL#.L#

Again, at this point, people stop shifting around and the seating area reaches equilibrium.
Once this occurs, you count ``26`` occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty,
once equilibrium is reached, how many seats end up occupied?
"""

seats = original_seats


def get_visible_seats(x: int, y: int) -> Iterable[str]:

	# looking right
	for x_idx in range(x + 1, row_length):
		seat = seats[y][x_idx]
		if seat in {OCCUPIED, EMPTY}:
			yield seat
			break

	# looking left
	for x_idx in range(x - 1, -1, -1):
		seat = seats[y][x_idx]
		if seat in {OCCUPIED, EMPTY}:
			yield seat
			break

	# looking down
	for y_idx in range(y + 1, col_length):
		seat = seats[y_idx][x]
		if seat in {OCCUPIED, EMPTY}:
			yield seat
			break

	# looking up
	for y_idx in range(y - 1, -1, -1):
		seat = seats[y_idx][x]
		if seat in {OCCUPIED, EMPTY}:
			yield seat
			break

	def look_diagonally(x_idx, y_idx):
		if y_idx < 0:
			return
		if x_idx < 0:
			return

		if y_idx == y or x_idx == x:
			return

		try:
			seat = seats[y_idx][x_idx]

			return seat
		except IndexError:
			pass

	# looking northeast
	offset = 1
	while True:
		y_idx = y - offset
		x_idx = x + offset

		status = look_diagonally(x_idx, y_idx)
		if status in {OCCUPIED, EMPTY}:
			yield status
			break
		elif status is None:
			break

		offset += 1

	# looking northwest
	offset = 1
	while True:
		y_idx = y - offset
		x_idx = x - offset

		status = look_diagonally(x_idx, y_idx)
		if status in {OCCUPIED, EMPTY}:
			yield status
			break
		elif status is None:
			break

		offset += 1

	# looking southwest
	offset = 1
	while True:
		y_idx = y + offset
		x_idx = x - offset

		status = look_diagonally(x_idx, y_idx)
		if status in {OCCUPIED, EMPTY}:
			yield status
			break
		elif status is None:
			break

		offset += 1

	# looking southeast
	offset = 1
	while True:
		y_idx = y + offset
		x_idx = x + offset

		status = look_diagonally(x_idx, y_idx)
		if status in {OCCUPIED, EMPTY}:
			yield status
			break
		elif status is None:
			break

		offset += 1


iteration = 1

while True:
	changes = 0
	new_seats = []

	for y_idx, row in enumerate(seats):
		new_seats.append([])

		for x_idx, seat in enumerate(row):

			adjacent_seats = Counter(get_visible_seats(x_idx, y_idx))

			if seat == EMPTY:
				print(adjacent_seats)
				if not adjacent_seats[OCCUPIED]:
					new_seats[y_idx].append(OCCUPIED)
					changes += 1
					continue
			elif seat == OCCUPIED:
				if adjacent_seats[OCCUPIED] >= 5:
					new_seats[y_idx].append(EMPTY)
					changes += 1
					continue

			new_seats[y_idx].append(seat)

	if seats == new_seats:
		break

	seats = new_seats

	# print("Iteration", iteration, ",", changes, "changes")
	iteration += 1

occupied_seats = Counter(chain.from_iterable(seats))[OCCUPIED]

print(f"After everyone has stopped moving, {occupied_seats} seats are occupied.")  # 2068
