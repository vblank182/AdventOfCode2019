## Advent of Code 2019: Day 6
## https://adventofcode.com/2019/day/6
## Jesse Williams | github.com/vblank182

# ** Failed Attempt 1 **

class Orbit():
    def __init__(self, orbitStr):
        self.orbitee, self.orbiter = orbitStr.split(')')

class Body():
    def __init__(self, orbit):
        self.name = orbit.orbiter
        self.orbits = orbit.orbitee

    def distanceToCOM(self, bodies):
        # Counts the number of orbits connecting this body to COM
        dist = 0
        currentBody = self
        while True:
            dist += 1
            if currentBody.orbits == "COM":
                break
            else:
                dist += 1
                currentBody = bodies[self.orbits]
        return dist


def parseOrbits(orbitData):
    # Returns a list of Orbit objects
    orbits = []
    for orbitStr in orbitData:
        orbits.append(Orbit(orbitStr))
    return orbits

def getBodies(orbits):
    # Finds all bodies described in orbital data and assigns each its direct orbiter. Returns a list of orbital Body objects.
    bodies = {}  # Lookup dict for body names/objects. The key for each entry is the orbiter since each orbiter only orbits one orbitee.

    # Create Body objects and set direct orbits.
    for orbit in orbits:
        # If we haven't already created an object for this orbiter, make one now.
        if orbit.orbiter not in bodies.keys():
            bodies[orbit.orbiter] = Body(orbit)
        else:
            print("Error: The body {} is already in the dictionary.".format(orbit.orbiter))

    return bodies

def countDistances(bodies):
    # Count steps to COM for each body
    totalDist = 0
    for body in bodies:
        totalDist += bodies[body].distanceToCOM(bodies)
    return totalDist

if __name__ == '__main__':
    with open('day06_input.txt') as f:
        orbitData = [line[:-1] for line in f.readlines()]

    orbits = parseOrbits(orbitData)
    # for orb in orbits:
    #    print('{} ) {}'.format(orb.orbitee, orb.orbiter))
    bodies = getBodies(orbits)
    #for body in bodies:
    #    print('{}: {} ) {}'.format(body, bodies[body].orbiter, bodies[body].name))
    distance = countDistances(bodies)
