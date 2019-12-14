## Advent of Code 2019: Day 11
## https://adventofcode.com/2019/day/11
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 1894, [Part 2]: JKZLZJBH

from collections import namedtuple
from PIL import Image
from math import floor
import intcode_v5_1 as ic5

Coords = namedtuple('Coords', ['x','y'])

# Colors
BLACK = 0
WHITE = 1

# Directions in clockwise order from Up
d_U = 0  # up
d_R = 1  # right
d_D = 2  # down
d_L = 3  # left

class Robot():
    def __init__(self):
        self.pos = Coords(0,0)
        self.dir = d_U
        self.totalMoves = 0
        self.panelsVisited = {Coords(0,0)}

    def move(self, turnDir):
        if turnDir == 0:  # turn left/counterclockwise
            self.dir = (self.dir - 1) % 4

        elif turnDir == 1:  # turn right/clockwise
            self.dir = (self.dir + 1) % 4

        self.pos = Robot._stepForward(self.pos, self.dir)
        self.panelsVisited.add(self.pos)
        self.totalMoves += 1


    @staticmethod
    def _stepForward(pos, dir):
        # Takes a position and direction and returns the final position after taking a step forward
        if dir == d_U:
            return Coords(pos.x, pos.y+1)
        elif dir == d_R:
            return Coords(pos.x+1, pos.y)
        elif dir == d_D:
            return Coords(pos.x, pos.y-1)
        elif dir == d_L:
            return Coords(pos.x-1, pos.y)


if __name__ == '__main__':

    ## Part 1 ##
    PaintRobotSim = Robot()

    hullPaintMap = {Coords(0,0): BLACK}  # dict mapping ship hull coords to paint colors

    initTape = ic5.loadProgram(inputFile="day11_input.txt")
    outputDirection = ic5.ProgramState(initTape, 0, [], 0, 0)  # dummy program state to initialize loop

    while True:
        # Get input from paint map or use 0 if panel hasn't been seen before
        try: input = hullPaintMap[PaintRobotSim.pos]
        except KeyError: input = 0

        # Run program with paint color at current position as input starting from the program state of the last output
        outputColor = ic5.runProgram(outputDirection.tape, input, feedbackMode=True, feedbackPtr=outputDirection.ptr, feedbackRelbase=outputDirection.relbase)
        if outputColor == None: break  # program halted

        # Run program again, feeding last state back in to force second output (this basically simulates a program that never stops between these outputs)
        outputDirection = ic5.runProgram(outputColor.tape, input, feedbackMode=True, feedbackPtr=outputColor.ptr, feedbackRelbase=outputColor.relbase)

        # Update paint map with first program output
        hullPaintMap[PaintRobotSim.pos] = outputColor.output[0]

        # Update robot location and direction with second program output
        PaintRobotSim.move(outputDirection.output[0])

    print(f'[Part 1] Simulation complete. Hull painting robot will paint {len(PaintRobotSim.panelsVisited)} panels at least once.')


    ## Part 2 ##
    PaintRobot = Robot()

    hullPaintMap = {Coords(0,0): WHITE}  # dict mapping ship hull coords to paint colors (starting at a white tile)

    initTape = ic5.loadProgram(inputFile="day11_input.txt")
    outputDirection = ic5.ProgramState(initTape, 0, [], 0, 0)  # dummy program state to initialize loop

    while True:
        # Get input from paint map or use 0 if panel hasn't been seen before
        try: input = hullPaintMap[PaintRobot.pos]
        except KeyError: input = 0

        # Run program with paint color at current position as input starting from the program state of the last output
        outputColor = ic5.runProgram(outputDirection.tape, input, feedbackMode=True, feedbackPtr=outputDirection.ptr, feedbackRelbase=outputDirection.relbase)
        if outputColor == None: break  # program halted

        # Run program again, feeding last state back in to force second output (this basically simulates a program that never stops between these outputs)
        outputDirection = ic5.runProgram(outputColor.tape, input, feedbackMode=True, feedbackPtr=outputColor.ptr, feedbackRelbase=outputColor.relbase)

        # Update paint map with first program output
        hullPaintMap[PaintRobot.pos] = outputColor.output[0]

        # Update robot location and direction with second program output
        PaintRobot.move(outputDirection.output[0])


    # Find the boundaries of the map coords
    map_U, map_R, map_D, map_L = 0, 0, 0, 0
    for coords in hullPaintMap.keys():
        if coords.x < map_L: map_L = coords.x
        if coords.x > map_R: map_R = coords.x
        if coords.y > map_D: map_D = coords.y
        if coords.y < map_U: map_U = coords.y

    img_w = map_R-map_L
    img_h = map_D-map_U + 3
    img_numpixels = img_w*img_h

    # Generate a list of pixels for the image with colors determined by the final hull paint map
    img_pixelArray = [0]*img_numpixels
    for px in range(img_numpixels):
        px_coords = Coords(px%img_w, floor(px/img_w))
        try:
            img_pixelArray[px] = hullPaintMap[Coords(px_coords.x, px_coords.y-7)]  # boo magic numbers but i've already spent too much time on this one ‾\_(ツ)_/‾
        except KeyError:
            img_pixelArray[px] = 0  # default if coords not in paint map

    # The pixel array is flipped vertically since the map is indexed from the bottom-left corner and the image from the top-left, so rearrange the pixels to flip it back
    img_pixelArrayFlipped = [0]*img_numpixels
    for row in range(img_h):
        img_pixelArrayFlipped[row*img_w : row*img_w + img_w] = img_pixelArray[(img_h-row)*img_w : (img_h-row)*img_w + img_w]

    # Generate image using final pixel array
    img = Image.new('1', (img_w, img_h))
    img.putdata(img_pixelArrayFlipped)
    img.save('day11_output.png')
