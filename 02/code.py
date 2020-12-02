"""
--- Day 2: Password Philosophy ---

Your flight departs in a few days from the coastal airport;
the easiest way down to the coast from here is via toboggan.

The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day::

	"Something's wrong with our computers; we can't log in!"

You ask if you can take a look.


Their password database seems to be a little corrupted:
some of the passwords wouldn't have been allowed by the Official Toboggan Corporate Policy
that was in effect when they were chosen.

To try to debug the problem, they have created a list (your puzzle input) of passwords
(according to the corrupted database) and the corporate policy when that password was set.


For example, suppose you have the following list::

	1-3 a: abcde
	1-3 b: cdefg
	2-9 c: ccccccccc


Each line gives the password policy and then the password.
The password policy indicates the lowest and highest number of times a given letter
must appear for the password to be valid.
For example, ``1-3 a`` means that the password must contain ``a`` at least ``1`` time and at most ``3`` times.

In the above example, ``2`` passwords are valid.
The middle password, ``cdefg``, is not; it contains no instances of ``b``, but needs at least ``1``.
The first and third passwords are valid: they contain one ``a`` or nine ``c``,
both within the limits of their respective policies.

How many passwords are valid according to their policies?
"""

# stdlib
from typing import Tuple

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

passwords = [x.split(": ") for x in PathPlus("input.txt").read_lines() if x]


def parse_policy(policy: str) -> Tuple[range, str]:
	count, char = policy.split(" ")
	start, stop = map(int, count.split("-"))

	return range(start, stop + 1), char


def verify_password(password: str, policy: Tuple[range, str]) -> bool:
	count = password.count(policy[1])

	return count in policy[0]


n_valid = 0

for policy, password in passwords:
	n_valid += verify_password(password, parse_policy(policy))


print(f"There are {n_valid} valid passwords.")  # 556


# ==========================
print("\nPart Two")
# ==========================

"""
While it appears you validated the passwords correctly,
they don't seem to be what the Official Toboggan Corporate Authentication System is expecting.

The shopkeeper suddenly realizes that he just accidentally explained the password policy rules 
from his old job at the sled rental place down the street! 
The Official Toboggan Corporate Policy actually works a little differently.

Each policy actually describes two positions in the password, 
where 1 means the first character, 2 means the second character, and so on. 
(Be careful; Toboggan Corporate Policies have no concept of "index zero"!) 
Exactly one of these positions must contain the given letter.
Other occurrences of the letter are irrelevant for the purposes of policy enforcement.

Given the same example list from above::

	1-3 a: abcde is valid: position 1 contains a and position 3 does not.
	1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
	2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.

How many passwords are valid according to the new interpretation of the policies?
"""


def parse_policy_v2(policy: str) -> Tuple[int, int, str]:
	count, char = policy.split(" ")
	first, second = map(int, count.split("-"))

	return first - 1, second - 1, char


def verify_password_v2(password: str, policy: Tuple[int, int, str]) -> bool:
	if password[policy[0]] == policy[2]:
		return password[policy[1]] != policy[2]
	else:
		return password[policy[1]] == policy[2]


n_valid = 0

for policy, password in passwords:
	n_valid += verify_password_v2(password, parse_policy_v2(policy))


print(f"There are {n_valid} valid passwords.")  # 605

