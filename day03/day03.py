## Advent of Code 2019: Day 3
## https://adventofcode.com/2019/day/3
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 529, [Part 2]: 20386

class Wire():
    def __init__(self, path):
        self.path = path
        self.coords = self.getCoords()

    def getCoords(self):
        # Returns a set of all coordinates occupied by this wire with the given path from the central port, defined as (0, 0).
        coords = []
        curPos = (0, 0)
        steps = self.path.split(',')

        for step in steps:
            dist = int(step[1:])  # distance to move in this direction (number part of step)

            if step[0] == 'L':
                for i in range(1, dist+1):
                    coords.append((curPos[0]-i, curPos[1]))     # add all coords between current position and destination
                curPos = (curPos[0]-dist, curPos[1])            # update current position after moving to end of step
            elif step[0] == 'R':
                for i in range(1, dist+1):
                    coords.append((curPos[0]+i, curPos[1]))
                curPos = (curPos[0]+dist, curPos[1])
            elif step[0] == 'D':
                for i in range(1, dist+1):
                    coords.append((curPos[0], curPos[1]-i))
                curPos = (curPos[0], curPos[1]-dist)
            elif step[0] == 'U':
                for i in range(1, dist+1):
                    coords.append((curPos[0], curPos[1]+i))
                curPos = (curPos[0], curPos[1]+dist)

        return set(coords)

    def countSteps(self, location):
        # Follows the wire's path and counts the number of steps it takes to get to the given location
        curPos = (0, 0)
        steps = self.path.split(',')
        stepCount = 0

        for step in steps:
            dist = int(step[1:])  # distance to move in this direction (number part of step)

            for _ in range(1, dist+1):
                if step[0] == 'L':
                    curPos = (curPos[0]-1, curPos[1])  # move a step in this direction
                elif step[0] == 'R':
                    curPos = (curPos[0]+1, curPos[1])
                elif step[0] == 'D':
                    curPos = (curPos[0], curPos[1]-1)
                elif step[0] == 'U':
                    curPos = (curPos[0], curPos[1]+1)

                stepCount += 1
                if curPos == location:
                    return stepCount


if __name__ == '__main__':

    with open('day03_input.txt') as f:
        allPaths = [path[:-1] for path in f.readlines()]  # trim '\n' characters from end of lines

        # Make a list of the Wire objects containing all of their coordinates
        wires = []
        for path in allPaths:
            wires.append(Wire(path))

        # Find all intersections between the two wires
        allIntersections = wires[0].coords.intersection(wires[1].coords)

        ## Part 1 ##
        # Find the nearest intersection (by Manhattan distance) to the central port at (0, 0)
        least_mdist = 0
        for isc in allIntersections:
            mdist = abs(isc[0]) + abs(isc[1])
            if (0 < mdist < least_mdist) or least_mdist==0:
                # Closer intersection found
                least_mdist = mdist
                nearest_isc = isc

        print("[Part 1] The closest intersection to the central port is at location ({}, {}), a distance of {}".format(nearest_isc[0], nearest_isc[1], least_mdist))


        ## Part 2 ##
        # For each intersection, find the number of steps each wire takes to reach it (the first time)
        min_steps = 0
        for isc in allIntersections:
            totalSteps = wires[0].countSteps(isc) + wires[1].countSteps(isc)
            if (0 < totalSteps < min_steps) or min_steps==0:
                min_steps = totalSteps
                min_wire1 = wires[0].countSteps(isc)
                min_wire2 = wires[1].countSteps(isc)
                min_isc = isc

        print("\n[Part 2] The minimum number of steps to reach an intersection is {}.\nThis will reach the intersection at ({}, {}) in {} steps along the first wire and {} steps along the second wire.".format(min_steps, min_isc[0], min_isc[1], min_wire1, min_wire2))
