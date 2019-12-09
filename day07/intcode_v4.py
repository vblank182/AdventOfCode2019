## Advent of Code 2019: Intcode Computer v4
## https://adventofcode.com/2019
## Jesse Williams | github.com/vblank182

# **Compatible with Day 7, Part 1&2**

# Changelog:
# - Added support for multiple inputs (as a deque)
# - Added "feedback mode" for programs that require new inputs dependent on their outputs to continue
#   - Suspends the program after each output to await next input by returning the current state of the tape, current pointer location, and any outputs
#   - Program returns None in feedback mode to indicate the program has halted

from collections import deque, namedtuple

#~# Opcodes #~#
ADD, MUL, IN, OUT, JIT, JIF, LT, EQ = 1, 2, 3, 4, 5, 6, 7, 8
END = 99

#~# Parameter Modes #~#
POS = 0
IMM = 1

# Formatted tuple for holding the state of a suspended program
ProgramState = namedtuple('ProgramState', ['tape', 'ptr', 'output'])

# Numbers of expected parameters for each opcode
num_params = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 99:0}

def loadProgram(inputFile):
    ''' Loads a program file in "0,1,2,3,..." format and returns a list of integers. '''
    with open(inputFile) as f:
        initialTapeStrs = f.read()[:-1].split(',')
        initialTape = [int(i) for i in initialTapeStrs]
    return initialTape

def runProgram(initialTape, input, debugLevel=0, feedbackMode=False, feedbackPtr=0):
    # Make a copy of the initial tape.
    workTape = initialTape.copy()

    try: input = deque(input)  # convert input list to a deque to act as a queue
    except TypeError: input = deque([input])  # if a single int is input, make it into a list first

    output = []

    running = True
    cycle = 0

    if feedbackMode:
        ptr = feedbackPtr
    else:
        ptr = 0

    while running:
        # Determine the current opcode and parameter modes
        opcode = int( str(workTape[ptr])[-2:] )  # get the opcode from the last 2 digits of the current position
        param_modes = [0]*num_params[opcode]
        for i in range(num_params[opcode]):
            try:
                # Set param mode to digit found (scanning right-to-left from opcode)
                param_modes[i] = int( str(workTape[ptr])[-3-i] )
            except IndexError:
                # Default to param mode 0 if no digit is found
                param_modes[i] = 0

        if debugLevel >=2:
            print("[{}] Opcode {} at position {} with parameters {} in modes {}.  Raw instruction: '{}'".format(cycle, opcode, ptr, workTape[ptr+1:ptr+num_params[opcode]+1], param_modes, workTape[ptr:ptr+num_params[opcode]+1]))

        #::  [1] Addition  ::#
        if opcode == ADD:
            param = [0]*num_params[opcode]  # initialize list of parameters

            # Param 1 (left addend)
            if param_modes[0] == POS:
                param[0] = workTape[workTape[ptr+1]]  # position mode
            elif param_modes[0] == IMM:
                param[0] = workTape[ptr+1]            # immediate mode

            # Param 2 (right addend)
            if param_modes[1] == POS:
                param[1] = workTape[workTape[ptr+2]]  # position mode
            elif param_modes[1] == IMM:
                param[1] = workTape[ptr+2]            # immediate mode

            # Param 3 (sum)
            if param_modes[2] == POS:
                workTape[workTape[ptr+3]] = param[0] + param[1]             # set output (position mode)
            elif param_modes[2] == IMM:
                raise InvalidParameterMode(opcode, 3, param_modes[2], "Immediate mode not supported for output.")
                break

            ptr += num_params[opcode] + 1  # advance instruction pointer

        #::  [2] Multiplication  ::#
        elif opcode == MUL:
            param = [0]*num_params[opcode]  # initialize list of parameters

            # Param 1 (left multiplicand)
            if param_modes[0] == POS:
                param[0] = workTape[workTape[ptr+1]]  # position mode
            elif param_modes[0] == IMM:
                param[0] = workTape[ptr+1]            # immediate mode

            # Param 2 (right multiplicand)
            if param_modes[1] == POS:
                param[1] = workTape[workTape[ptr+2]]  # position mode
            elif param_modes[1] == IMM:
                param[1] = workTape[ptr+2]            # immediate mode

            # Param 3 (product)
            if param_modes[2] == POS:
                workTape[workTape[ptr+3]] = param[0] * param[1]             # set output (position mode)
            elif param_modes[2] == IMM:
                raise InvalidParameterMode(opcode, 3, param_modes[2], "Immediate mode not supported for output.")
                break

            ptr += num_params[opcode] + 1  # advance instruction pointer

        #::  [3] Input  ::#
        elif opcode == IN:
            # Param 1 (position)
            if param_modes[0] == POS:
                workTape[workTape[ptr+1]] = input.popleft()  # store next input at position in parameter (position mode)
            elif param_modes[0] == IMM:
                raise InvalidParameterMode(opcode, 1, param_modes[0], "Immediate mode not supported for this instruction.")
                break

            ptr += num_params[opcode] + 1  # advance instruction pointer

        #::  [4] Output  ::#
        elif opcode == OUT:
            # Param 1 (position)
            if param_modes[0] == POS:
                output.append(workTape[workTape[ptr+1]])    # write output (position mode)
            elif param_modes[0] == IMM:
                output.append(workTape[ptr+1])              # write output (immediate mode)

            ptr += num_params[opcode] + 1  # advance instruction pointer

            if feedbackMode: return ProgramState(workTape, ptr, output)

        #::  [5] Jump-If-True  ::#
        elif opcode == JIT:
            param = [0]*num_params[opcode]  # initialize list of parameters

            # Param 1 (condition)
            if param_modes[0] == POS:
                param[0] = workTape[workTape[ptr+1]]  # position mode
            elif param_modes[0] == IMM:
                param[0] = workTape[ptr+1]            # immediate mode

            # Param 2 (destination)
            if param_modes[1] == POS:
                param[1] = workTape[workTape[ptr+2]]  # position mode
            elif param_modes[1] == IMM:
                param[1] = workTape[ptr+2]            # immediate mode

            if param[0] != 0:   # if nonzero (true),
                ptr = param[1]  # jump
            else:
                ptr += num_params[opcode] + 1  # advance instruction pointer

        #::  [6] Jump-If-False  ::#
        elif opcode == JIF:
            param = [0]*num_params[opcode]  # initialize list of parameters

            # Param 1 (condition)
            if param_modes[0] == POS:
                param[0] = workTape[workTape[ptr+1]]  # position mode
            elif param_modes[0] == IMM:
                param[0] = workTape[ptr+1]            # immediate mode

            # Param 2 (destination)
            if param_modes[1] == POS:
                param[1] = workTape[workTape[ptr+2]]  # position mode
            elif param_modes[1] == IMM:
                param[1] = workTape[ptr+2]            # immediate mode

            if param[0] == 0:   # if zero (false),
                ptr = param[1]  # jump
            else:
                ptr += num_params[opcode] + 1  # advance instruction pointer

        #::  [7] Less Than  ::#
        elif opcode == LT:
            param = [0]*num_params[opcode]  # initialize list of parameters

            # Param 1 (left comparison)
            if param_modes[0] == POS:
                param[0] = workTape[workTape[ptr+1]]  # position mode
            elif param_modes[0] == IMM:
                param[0] = workTape[ptr+1]            # immediate mode

            # Param 2 (right comparison)
            if param_modes[1] == POS:
                param[1] = workTape[workTape[ptr+2]]  # position mode
            elif param_modes[1] == IMM:
                param[1] = workTape[ptr+2]            # immediate mode

            # Param 3 (output position)
            if param_modes[2] == POS:
                param[2] = workTape[ptr+3]  # position mode
            elif param_modes[2] == IMM:
                raise InvalidParameterMode(opcode, 3, param_modes[2], "Immediate mode not supported for output.")
                break

            if param[0] < param[1]:
                workTape[param[2]] = 1
            else:
                workTape[param[2]] = 0

            ptr += num_params[opcode] + 1  # advance instruction pointer

        #::  [8] Equals  ::#
        elif opcode == EQ:
            param = [0]*num_params[opcode]  # initialize list of parameters

            # Param 1 (left comparison)
            if param_modes[0] == POS:
                param[0] = workTape[workTape[ptr+1]]  # position mode
            elif param_modes[0] == IMM:
                param[0] = workTape[ptr+1]            # immediate mode

            # Param 2 (right comparison)
            if param_modes[1] == POS:
                param[1] = workTape[workTape[ptr+2]]  # position mode
            elif param_modes[1] == IMM:
                param[1] = workTape[ptr+2]            # immediate mode

            # Param 3 (output position)
            if param_modes[2] == POS:
                param[2] = workTape[ptr+3]            # position mode
            elif param_modes[2] == IMM:
                raise InvalidParameterMode(opcode, 3, param_modes[2], "Immediate mode not supported for output.")
                break

            if param[0] == param[1]:
                workTape[param[2]] = 1
            else:
                workTape[param[2]] = 0

            ptr += num_params[opcode] + 1  # advance instruction pointer


        #::  [99] End of Program  ::#
        elif opcode == END:  # Program finished
            running = False

        else:
            raise UnknownOpcode(opcode, ptr, workTape, debugLevel)
            return False

        cycle += 1

        if debugLevel >= 3:
            print(workTape)

    # End of program
    if feedbackMode: return None
    else: return output


## Exception Classes ##

class InvalidParameterMode(Exception):
    '''Exception raised for an invalid parameter mode.'''
    def __init__(self, opcode, position, param_mode, message):
        print("[Error] Invalid parameter mode '{}' for parameter {} of opcode {}.\n".format(param_mode, position, opcode))
        if message != "":
            print(message)

class UnknownOpcode(Exception):
    '''Exception raised for an unknown opcode.'''
    def __init__(self, opcode, ptr, workTape, debugLevel):
        if debugLevel == 1:
            print("[Error] Unknown opcode '{}' at location {}. Following instructions: ".format(opcode, ptr, workTape[ptr:ptr+9]))
        elif debugLevel >= 2:
            print("[Error] Unknown opcode '{}' at location {}.".format(opcode, ptr))
            print("Current tape state:\n")
            print(workTape)
        else:  # debug level 0
            print("[Error] Unknown opcode '{}' at location {}.".format(opcode, ptr))
