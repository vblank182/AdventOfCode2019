## Advent of Code 2019: Day 1
## https://adventofcode.com/2019/day/1
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 3126794, [Part 2]: 4687331

from math import floor

def calcFuel(mass):
    # Returns the fuel mass required to launch the input module mass
    return floor(int(mass)/3) - 2

def calcAllFuel(mass):
    # Returns the fuel mass required to launch the input module mass, plus the fuel required for the mass of that fuel, and so on until the fuel becomes <= 0.
    thisFuel = calcFuel(mass)
    if thisFuel > 0:
        return thisFuel + calcAllFuel(thisFuel)
    else:
        return 0

if __name__ == '__main__':
    with open('day01_input.txt') as f:
        masses = f.readlines()

    ## Part 1
    totalFuel = 0
    for mass in masses:
        totalFuel += calcFuel(mass)

    print("[Part 1] Require {} units of fuel.".format(totalFuel))


    ## Part 2
    totalAllFuel = 0
    for mass in masses:
        totalAllFuel += calcAllFuel(mass)
    print("[Part 2] Require {} units of fuel.".format(totalAllFuel))
