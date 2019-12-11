## Advent of Code 2019: Day 9
## https://adventofcode.com/2019/day/9
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 3533056970, [Part 2]: 72852

import intcode_v5 as ic5

if __name__ == '__main__':

    ## Part 1 ##
    boost_test_input = 1
    tape = ic5.loadProgram(inputFile="day09_input.txt")
    outputs = ic5.runProgram(tape, boost_test_input)
    print("[Part 1] Test successful! BOOST keycode: {}".format(outputs[-1]))

    ## Part 2 ##
    boost_test_input = 2
    tape = ic5.loadProgram(inputFile="day09_input.txt")
    outputs = ic5.runProgram(tape, boost_test_input)
    print("[Part 2] BOOST program finished. Distress signal coordinates: {}".format(outputs[-1]))
