## Advent of Code 2019: Day 4
## https://adventofcode.com/2019/day/4
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 579, [Part 2]: 358

input_range = (353096, 843212)

from collections import Counter

def identicalAdjacentDigits(n):
    # Returns true if n has at least one pair of identical adjacent digits
    digits = str(n)
    for i in range(len(digits)-1):
        if digits[i] == digits[i+1]:
            return True
    return False

def monotoniclyIncreasing(n):
    # Returns true if n is monotonically increasing
    digits = str(n)
    for i in range(len(digits)-1):
        if digits[i] > digits[i+1]:
            return False
    return True

def exactlyTwoIdenticalAdjacentDigits(n):
    # Returns true if n has at least one pair of identical adjacent digits without repeating more than twice

    # Since the sequences must be monotonically increasing, we can just count the occurences of each digit.
    # If any digit occurs exactly twice, the condition is met (assuming we've already filtered for monotonicity).
    digitCounts = Counter(str(n))
    for digit in digitCounts:
        if digitCounts[digit] == 2:
            return True
    return False


## Part 1 ##
password_list = []
for n in range(input_range[0], input_range[1]+1):
    if identicalAdjacentDigits(n) and monotoniclyIncreasing(n):
        password_list.append(n)
print("[Part 1] There are {} passwords matching the criteria in this range.".format(len(password_list)))


## Part 2 ##
password_list = []
for n in range(input_range[0], input_range[1]+1):
    if monotoniclyIncreasing(n) and exactlyTwoIdenticalAdjacentDigits(n):
        password_list.append(n)
print("[Part 2] There are {} passwords matching the criteria in this range.".format(len(password_list)))
