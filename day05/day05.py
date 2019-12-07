## Advent of Code 2019: Day 5
## https://adventofcode.com/2019/day/5
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 5821753, [Part 2]: 11956381

import intcode_v2 as ic2
import intcode_v3 as ic3

if __name__ == '__main__':

    ## Part 1 ##
    diagnostic_test_input = 1

    tape = ic2.loadProgram(inputFile="day05_input.txt")

    outputs = ic2.runProgram(tape, diagnostic_test_input, debugLevel=0)
    if outputs[:-1] == [0]*len(outputs[:-1]):
        # If all outputs except the last are 0, the test was successful.
        print("[Part 1] Test successful. Diagnostic code: {}".format(outputs[-1]))
    else:
        print("[Part 1] Test unsuccessful. Output sequence:\n")
        print(outputs)


    #TEST
    # testinput=9
    # test="3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    # testtape=test.split(',')
    # testtape = [int(i) for i in testtape]
    # print("\n")
    # print(ic3.runProgram(testtape, testinput, debugLevel=3))

    ## Part 2 ##
    diagnostic_test_input = 5

    tape = ic3.loadProgram(inputFile="day05_input.txt")

    outputs = ic3.runProgram(tape, diagnostic_test_input, debugLevel=0)
    print("[Part 2] Test successful. Diagnostic code: {}".format(outputs[0]))
