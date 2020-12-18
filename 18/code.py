"""
--- Day 18: Operation Order ---

As you look out the window and notice a heavily-forested continent slowly appear over the horizon,
you are interrupted by the child sitting next to you.
They're curious if you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you remember.

The homework (your puzzle input) consists of a series of expressions that consist of addition (``+``),
multiplication (``*``), and parentheses (``(...)``).
Just like normal math, parentheses indicate that the expression inside must be evaluated
before it can be used by the surrounding expression.
Addition still finds the sum of the numbers on both sides of the operator,
and multiplication still finds the product.

However, the rules of operator precedence have changed.
Rather than evaluating multiplication before addition, the operators have the same precedence,
and are evaluated left-to-right regardless of the order in which they appear.

For example, the steps to evaluate the expression ``1 + 2 * 3 + 4 * 5 + 6`` are as follows::

	1 + 2 * 3 + 4 * 5 + 6
	  3   * 3 + 4 * 5 + 6
		  9   + 4 * 5 + 6
			 13   * 5 + 6
				 65   + 6
					 71

Parentheses can override this order;
for example, here is what happens if parentheses are added to form ``1 + (2 * 3) + (4 * (5 + 6))``::

	1 + (2 * 3) + (4 * (5 + 6))
	1 +    6    + (4 * (5 + 6))
		 7      + (4 * (5 + 6))
		 7      + (4 *   11   )
		 7      +     44
				51

Here are a few more examples::

- ``2 * 3 + (4 * 5)`` becomes ``26``.
- ``5 + (8 * 3 + 9 + 3 * 4 * 3)`` becomes ``437``.
- ``5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))`` becomes ``12240``.
- ``((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2`` becomes ``13632``.

Before you can help with the homework, you need to understand it yourself.
Evaluate the expression on each line of the homework; what is the sum of the resulting values?
"""

# stdlib
import operator
import re
from typing import Callable, Optional

# 3rd party
from domdf_python_tools.paths import PathPlus

# ==========================
print("Part One")
# ==========================

sums = [x for x in PathPlus("input.txt").read_lines() if x]


def evaluate_group(expression: str) -> int:
	tokens = expression.split(' ')
	total = int(tokens[0])

	next_op: Optional[Callable] = None

	for token in tokens[1:]:
		if token == '*':
			next_op = operator.mul
		elif token == '+':
			next_op = operator.add
		elif token.isdigit() and next_op:
			total = next_op(total, int(token))
		else:
			raise NotImplementedError(token, next_op)

	return total


def evaluate_expression(expression: str) -> int:

	while True:
		paren_groups = re.findall(r"\(([0-9 +*]+)\)", expression)
		if paren_groups:
			for group in paren_groups:
				expression = expression.replace(f"({group})", str(evaluate_group(group)), 1)
		else:
			break

	return evaluate_group(expression)


total = 0

for sum_ in sums:
	answer = evaluate_expression(sum_)
	print(sum_, '=', answer)
	total += answer

print("The sum of all expressions is:", total)  # 3159145843816

# ==========================
print("\nPart Two")
# ==========================
"""
You manage to answer the child's questions and they finish part 1 of their homework,
but get stuck when they reach the next section: advanced math.

Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with.
Instead, addition is evaluated before multiplication.

For example, the steps to evaluate the expression ``1 + 2 * 3 + 4 * 5 + 6`` are now as follows::

	1 + 2 * 3 + 4 * 5 + 6
	  3   * 3 + 4 * 5 + 6
	  3   *   7   * 5 + 6
	  3   *   7   *  11
		 21       *  11
			 231

Here are the other examples from above::

- ``1 + (2 * 3) + (4 * (5 + 6))`` still becomes ``51``.
- ``2 * 3 + (4 * 5)`` becomes ``46``.
- ``5 + (8 * 3 + 9 + 3 * 4 * 3)`` becomes ``1445``.
- ``5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes ``669060``.
- ``((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes ``23340``.

What do you get if you add up the results of evaluating the homework problems using these new rules?
"""


def evaluate_addition_advanced(expression: str) -> int:
	tokens = expression.split(' ')
	assert len(tokens) == 3
	return int(tokens[0]) + int(tokens[-1])


def evaluate_multiplication_advanced(expression: str) -> int:
	tokens = expression.split(' ')
	assert len(tokens) == 3
	return int(tokens[0]) * int(tokens[-1])


def evaluate_group_advanced(expression: str) -> int:
	while True:
		addition_groups = re.findall(r"([0-9]+ \+ [0-9]+)", expression)
		if addition_groups:
			for group in addition_groups:
				expression = expression.replace(f"{group}", str(evaluate_addition_advanced(group)), 1)
		else:
			break

	while True:
		multiplication_groups = re.findall(r"([0-9]+ \* [0-9]+)", expression)
		if multiplication_groups:
			for group in multiplication_groups:
				expression = expression.replace(f"{group}", str(evaluate_multiplication_advanced(group)), 1)
		else:
			break

	return int(expression)


def evaluate_expression_advanced(expression: str) -> int:
	while True:
		paren_groups = re.findall(r"\(([0-9 +*]+)\)", expression)
		if paren_groups:
			for group in paren_groups:
				expression = expression.replace(f"({group})", str(evaluate_group_advanced(group)), 1)
		else:
			break

	return evaluate_group_advanced(expression)


total = 0

for sum_ in sums:
	answer = evaluate_expression_advanced(sum_)
	print(sum_, '=', answer)
	total += answer

print("The sum of all expressions in advanced math is:", total)  # 55699621957369
