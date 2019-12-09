## Advent of Code 2019: Day 7
## https://adventofcode.com/2019/day/7
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 117312, [Part 2]: 1336480

import intcode_v4 as ic4
from itertools import permutations
from collections import namedtuple

# Formatted tuple for holding the state of a suspended program
ProgramState = namedtuple('ProgramState', ['tape', 'ptr', 'output'])

if __name__ == '__main__':
    initTape = ic4.loadProgram("day07_input.txt")

    ## Part 1 ##

    # Generate all permutations of phase settings
    phaseSpace = permutations([0,1,2,3,4])

    thrusterSignals = {}  # a dict to hold each phase space permutation with its corresponding output signal
    for phaseSet in phaseSpace:
        amps = [0]*5  # an ordered list of amplifier outputs
        signal = 0  # initial input signal to Amp A

        for i in range(len(amps)):
            signal = ic4.runProgram(initTape, [phaseSet[i], signal])[-1]
            amps[i] = signal  # output
        thrusterSignals[phaseSet] = amps[-1]  # add the final output from the amp chain to the signals dict for this phase set

    # Search dict for largest signal
    largestThrusterSignal = 0
    for pset in thrusterSignals:
        if thrusterSignals[pset] > largestThrusterSignal:
            largestThrusterSignal = thrusterSignals[pset]
            largestThrusterPhaseSet = pset

    print("[Part 1] Largest thruster signal {} obtained using phases {}.".format(largestThrusterSignal, largestThrusterPhaseSet))


    ## Part 2 ##

    # Generate all permutations of phase settings
    phaseSpace = permutations([5,6,7,8,9])

    thrusterSignals = {}  # a dict to hold each phase space permutation with its corresponding output signal
    for phaseSet in phaseSpace:

        amps = [0]*5  # an ordered list of amplifier outputs
        prgStates = [ProgramState([],0,[0])]*5  # an ordered list of amplifier program states (initialized with dummy states)
        done = False
        firstRun = True

        while not done:
            for i in range(len(amps)):
                if firstRun:
                    prgStates[i] = ic4.runProgram(initTape, [phaseSet[i], prgStates[i-1].output[-1]], feedbackMode=True)
                else:
                    returnState = ic4.runProgram(prgStates[i].tape, [prgStates[i-1].output[-1]], feedbackMode=True, feedbackPtr=prgStates[i].ptr)
                    if returnState == None:
                        done = True  # program halted
                    else:
                        prgStates[i] = returnState  # update program state
                        amps[i] = prgStates[i].output[-1]  # update outputs
            firstRun = False

        thrusterSignals[phaseSet] = amps[-1]  # add the final output from the amp chain to the signals dict for this phase set

    # Search dict for largest signal
    largestThrusterSignal = 0
    for pset in thrusterSignals:
        if thrusterSignals[pset] > largestThrusterSignal:
            largestThrusterSignal = thrusterSignals[pset]
            largestThrusterPhaseSet = pset

    print("[Part 2] Largest thruster signal {} obtained using phases {} in feedback loop mode.".format(largestThrusterSignal, largestThrusterPhaseSet))
