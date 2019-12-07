## Advent of Code 2019: Day 2
## https://adventofcode.com/2019/day/2
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 3516593, [Part 2]: 7749

### Intcode Computer v1 ###

def runTape(initialTape, input):
    workTape = initialTape.copy()

    (workTape[1], workTape[2]) = input

    ptr = 0
    while True:
        # Determine the current opcode
        opcode = workTape[ptr]

        if opcode == 1:  # Addition
            workTape[workTape[ptr+3]] = workTape[workTape[ptr+1]] + workTape[workTape[ptr+2]]
        elif opcode == 2:  # Multiplication
            workTape[workTape[ptr+3]] = workTape[workTape[ptr+1]] * workTape[workTape[ptr+2]]
        elif opcode == 99:  # Program finished
            return workTape
            break
        else:
            print("ERROR: Unknown opcode '{}'.".format(opcode))
            break

        ptr = ptr + 4

def reverseSearch(initialTape, targetOutput):
    # Searches for an input pair that produces the desired output.
    for inputL in range(0, len(initialTape)):
        for inputR in range(0, len(initialTape)):
            output = runTape(initialTape, (inputL, inputR))[0]
            if targetOutput == output:
                return (inputL, inputR)
    print("Output not found.")
    return (-1, -1)

if __name__ == '__main__':

    # Load program
    with open("day02_input.txt") as f:
        initialTapeStrs = f.read()[:-1].split(',')
        initialTape = [int(i) for i in initialTapeStrs]

    ## Part 1
    finalTape = runTape(initialTape, (12, 2))
    print("[Part 1] Output: {}".format(finalTape[0]))

    ## Part 2
    inputsNeeded = reverseSearch(initialTape, 19690720)
    print("[Part 2] Inputs: {} {}".format(inputsNeeded[0], inputsNeeded[1]))
