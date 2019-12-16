## Advent of Code 2019: Day 12
## https://adventofcode.com/2019/day/12
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 5350, [Part 2]: 467034091553512

import re
from collections import namedtuple
from itertools import combinations
from math import gcd

class Coords():
    def __init__(self, x, y=None, z=None):
        self.x, self.y, self.z = x, y, z
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'
    def __add__(self, other):
        if type(other) == tuple: return Coords(self.x+other[0], self.y+other[1], self.z+other[2])
        else: return Coords(self.x+other.x, self.y+other.y, self.z+other.z)
    def __sub__(self, other):
        if type(other) == tuple: return Coords(self.x-other[0], self.y-other[1], self.z-other[2])
        else: return Coords(self.x-other.x, self.y-other.y, self.z-other.z)


class Moon():
    def __init__(self, name, initialCoords):
        self.name = name
        self.pos = Coords(initialCoords[0], initialCoords[1], initialCoords[2])
        self.x, self.y, self.z = initialCoords
        self.vel = Coords(0,0,0)
        # For part 1
        self.PE = Moon.calcPE(self)
        self.KE = 0
        self.TE = self.PE * self.KE
        # For part 2
        self.period = [0, 0, 0, 0, 0, 0]  # [x, y, z, vel.x, vel.y, vel.z]
        self.History = [[],[],[],[],[],[]]

    def __repr__(self):
        return f'{self.name} @ ({self.x}, {self.y}, {self.z})'

    def step(self):
        # Simulate a step forward in time and apply velocities
        self.pos += self.vel
        self.x, self.y, self.z = self.pos.x, self.pos.y, self.pos.z
        self.PE = Moon.calcPE(self)
        self.KE = Moon.calcKE(self)
        self.TE = Moon.calcTE(self)

    @staticmethod
    def calcPE(Mun):
        # Returns the potential energy of the moon (sum of absolute values of position coords)
        return abs(Mun.x) + abs(Mun.y) + abs(Mun.z)
    @staticmethod
    def calcKE(Mun):
        # Returns the kinetic energy of the moon (sum of absolute values of velocity coords)
        return abs(Mun.vel.x) + abs(Mun.vel.y) + abs(Mun.vel.z)
    @staticmethod
    def calcTE(Mun):
        # Returns the total energy of the moon (kinetic energy times potential energy)
        return Mun.KE * Mun.PE

    @staticmethod
    def stateHash(Moons):
        ## * Unused hashing method from first part 2 solution attempt *
        stateSet = []  # list of all position and velocity coords of all moons in sequence
        for Mun in Moons:
            stateSet += [Mun.x, Mun.y, Mun.z]  # append the position coords of this moon
            stateSet += [Mun.vel.x, Mun.vel.y, Mun.vel.z]  # append the velocity coords of this moon
        return hash(tuple(stateSet))  # convert to a tuple and return the hash of the pos/vel state set of all moons


if __name__ == '__main__':
    ## Part 1 ##
    with open('day12_input.txt') as f:
        positionData = f.readlines()

    moons = [(0,0,0)]*4
    for i, line in enumerate(positionData):
        moons[i] = ( int(re.search("x=([-]*[\d]+)", line).groups()[0]), int(re.search("y=([-]*[\d]+)", line).groups()[0]), int(re.search("z=([-]*[\d]+)", line).groups()[0]) )

    # Initialize moons
    Io = Moon('Io', moons[0])
    Euro = Moon('Europa', moons[1])
    Gany = Moon('Ganymede', moons[2])
    Calli = Moon('Callisto', moons[3])
    Moons = [Io, Euro, Gany, Calli]

    t = 0  # time step
    t_final = 1000

    while t < t_final:

        # Apply gravity (update velocities)
        for (MoonA, MoonB) in combinations(Moons, 2):
            if MoonA.x < MoonB.x:
                MoonA.vel.x += 1
                MoonB.vel.x -= 1
            elif MoonA.x > MoonB.x:
                MoonA.vel.x -= 1
                MoonB.vel.x += 1
            else: pass  # no change if equal

            if MoonA.y < MoonB.y:
                MoonA.vel.y += 1
                MoonB.vel.y -= 1
            elif MoonA.y > MoonB.y:
                MoonA.vel.y -= 1
                MoonB.vel.y += 1
            else: pass  # no change if equal

            if MoonA.z < MoonB.z:
                MoonA.vel.z += 1
                MoonB.vel.z -= 1
            elif MoonA.z > MoonB.z:
                MoonA.vel.z -= 1
                MoonB.vel.z += 1
            else: pass  # no change if equal

        # Apply velocity (update positions)
        for Mun in Moons:
            Mun.step()

        t += 1  # advance time step

    # Get total system energy
    totalSystemEnergy = 0
    for Mun in Moons:
        totalSystemEnergy += Mun.TE

    print(f'[Part 1] After {t} timesteps, the total energy in the system is {totalSystemEnergy}.')


    ## Part 2 ##
    with open('day12_input.txt') as f:
        positionData = f.readlines()

    moons = [(0,0,0)]*4
    for i, line in enumerate(positionData):
        moons[i] = ( int(re.search("x=([-]*[\d]+)", line).groups()[0]), int(re.search("y=([-]*[\d]+)", line).groups()[0]), int(re.search("z=([-]*[\d]+)", line).groups()[0]) )

    # Initialize moons
    Io = Moon('Io', moons[0])
    Euro = Moon('Europa', moons[1])
    Gany = Moon('Ganymede', moons[2])
    Calli = Moon('Callisto', moons[3])
    Moons = [Io, Euro, Gany, Calli]

    t = 0  # time step
    #pastHashes = []  # start hash list with initial state
    #lastHash = Moon.stateHash(Moons)

    #while lastHash not in pastHashes:
        #pastHashes.append(lastHash)  # put hash of last step into past hashes list

    # Initialize histories
    for Mun in Moons:
        Mun.History[0].append(Mun.x)
        Mun.History[1].append(Mun.y)
        Mun.History[2].append(Mun.z)
        Mun.History[3].append(Mun.vel.x)
        Mun.History[4].append(Mun.vel.y)
        Mun.History[5].append(Mun.vel.z)

    # Find periods of each component of each moon's position
    done = False
    while not done:
        # Apply gravity (update velocities)
        for (MoonA, MoonB) in combinations(Moons, 2):
            if MoonA.x < MoonB.x:
                MoonA.vel.x += 1
                MoonB.vel.x -= 1
            elif MoonA.x > MoonB.x:
                MoonA.vel.x -= 1
                MoonB.vel.x += 1
            else: pass  # no change if equal

            if MoonA.y < MoonB.y:
                MoonA.vel.y += 1
                MoonB.vel.y -= 1
            elif MoonA.y > MoonB.y:
                MoonA.vel.y -= 1
                MoonB.vel.y += 1
            else: pass  # no change if equal

            if MoonA.z < MoonB.z:
                MoonA.vel.z += 1
                MoonB.vel.z -= 1
            elif MoonA.z > MoonB.z:
                MoonA.vel.z -= 1
                MoonB.vel.z += 1
            else: pass  # no change if equal

        # Apply velocity (update positions)
        for Mun in Moons:
            Mun.step()

        t += 1  # advance time step

        # Calculate hash of the state of the system at the end of this timestep
        #lastHash = Moon.stateHash(Moons)

        # Update history
        for Mun in Moons:
            Mun.History[0].append(Mun.x)
            Mun.History[1].append(Mun.y)
            Mun.History[2].append(Mun.z)
            Mun.History[3].append(Mun.vel.x)
            Mun.History[4].append(Mun.vel.y)
            Mun.History[5].append(Mun.vel.z)

        # Wait to see a list with two copies of the same pattern to confirm the period.
        for Mun in Moons:
            for i, axis in enumerate(Mun.History):
                if len(axis)%2 == 0 and axis[:int(len(axis)/2)] == axis[int(len(axis)/2):]:
                    # We found the period for this axis of this moon
                    if Mun.period[i] == 0:
                        Mun.period[i] = len(axis[:int(len(axis)/2)])

        # If all periods have been found, stop simulating
        done = True
        for Mun in Moons:
            for j in Mun.period:
                if j == 0: done = False


        # Print status
        if t%1000 == 0:
            allPeriods = []
            for Mun in Moons:
                allPeriods += (Mun.period)
            print(f'{t}:  {allPeriods}')



    allPeriods = []
    for Mun in Moons:
        allPeriods += (Mun.period)
    print(f'{t}:  {allPeriods}')

    # "Borrowed" from https://stackoverflow.com/questions/37237954/calculate-the-lcm-of-a-list-of-given-numbers-in-python
    lcm = allPeriods[0]
    for i in allPeriods[1:]:
        lcm = int( lcm*i/gcd(lcm, i) )

    print(allPeriods)

    print(f'[Part 2] After {lcm} timesteps, the universe will reach a state identical to time t=0.')
