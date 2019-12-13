## Advent of Code 2019: Day 10
## https://adventofcode.com/2019/day/10
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 286, [Part 2]: 504

from collections import namedtuple
from math import sqrt, floor, isclose, acos, atan2, degrees
import numpy as np
import pickle
from os import path

Asteroid = namedtuple('Asteroid', ['x','y'])
FILLED = '#'
EMPTY = '.'

def raycast(pointA, pointB, testPoint):
    # Returns True if testPoint is on a ray from A to B (and closer to A than B) and False otherwise

    refVector = np.array([pointB.x-pointA.x, pointB.y-pointA.y])
    testVector = np.array([testPoint.x-pointA.x, testPoint.y-pointA.y])

    # Check distance first. If testPoint is farther than pointB, automatically return False
    if np.linalg.norm(testVector) < np.linalg.norm(refVector):

        # Find the angle between the vectors
        cosine = np.vdot(refVector, testVector) / (np.linalg.norm(refVector)*np.linalg.norm(testVector))
        #if cosine > 1: cosine = 1.  # snap cosine value to 1 if rounding errors cause it to be greater
        #if cosine < -1: cosine = -1.  # snap cosine value to -1 if rounding errors cause it to be less
        cosine = np.clip(cosine, -1.0, 1.0)  # snap cosine value to [-1, 1] if rounding errors cause it to be outside
        theta = acos(cosine)

        # Check if the angle is 0 (up to tolerance). If the angle is pi, the vectors have opposite directions and the asteroid isn't in the ray.
        return isclose(theta, 0, abs_tol=1e-07)

    else:
        return False

def inDirectLOS(Station, Asteroid, AllAsteroids):
    # Tests whether a monitoring station at has direct line of sight to an asteroid
    for OtherAsteroid in AllAsteroids:
        if OtherAsteroid == Asteroid or OtherAsteroid == Station: continue
        if raycast(Station, Asteroid, OtherAsteroid):
            # If another asteroid is in line with this one and closer to the station, then LOS to this asteroid is blocked
            return False  # no LOS
    return True  # LOS

def countDirectLOS(Station, AllAsteroids):
    # Counts the total number of asteroids in direct line of sight of station
    count = 0
    for Asteroid in AllAsteroids:
        if Asteroid == Station: continue  # skip if same location
        if inDirectLOS(Station, Asteroid, AllAsteroids): count += 1
    return count

def getAsteroids(map):
    # Returns a list of coordinate pairs corresponding to asteroid locations in the map
    astList = []
    for ast in map:
        if map[ast] == FILLED:
            astList.append(ast)
    return astList


def shortestDistance(AsteroidList):
    # Takes a list of coordinates and returns the coord pair with the shortest distance from the origin
    nearestAstDist = sqrt(AsteroidList[0].x**2 + AsteroidList[0].y**2)
    for Ast in AsteroidList:
        if sqrt(Ast.x**2 + Ast.y**2) <= nearestAstDist:
            nearestAstDist = sqrt(Ast.x**2 + Ast.y**2)
            nearestAst = Ast
    return nearestAst

def toRelCoords(Station, absCoords):
    # Converts absolute map coords to relative station coords
    return Asteroid(absCoords.x-Station.x, absCoords.y-Station.y)

def toAbsCoords(Station, relCoords):
    # Converts relative station coords to absolute map coords
    return Asteroid(Station.x+relCoords.x, Station.y+relCoords.y)

def sortAsteroids(Station, AllAsteroids):
    # Returns a list of asteroid coords sorted first by angle from 0 and then by distance from Station. This list is relative to station.
    # This will simulate the order that each asteroid would be hit in according to the laser behavior
    # Angle 0 defined as direction of (0, -1) ("up") and positive rotations are clockwise

    asteroidsByAngle = {}  # a dict mapping each possible angle to the list of asteroid coords at that angle from station

    for Ast in AllAsteroids:
        if Ast == Station: continue  # skip station's asteroid

        # Measure angle from station
        relCoords = toRelCoords(Station, Ast)

        absAngle = atan2(relCoords.y, relCoords.x)  # angle relative to standard polar coord system
        absAngleDeg = degrees(absAngle)  # convert to degrees

        relAngleDeg = absAngleDeg + 90.  # this transformation produces angle relative to asteroid map coord system

        if relAngleDeg < 0: relAngleDeg += 360.  # put all angles in [0, 360)

        relAngleDeg = round(relAngleDeg, 6)  # round to make sure equivalent angles fall into the same baskets


        # Fill dict with all angles and coords (relative to station)
        try:
            asteroidsByAngle[relAngleDeg] += [relCoords]
        except KeyError:
            asteroidsByAngle[relAngleDeg] = [relCoords]


    # Sort list of dict keys (angles) and make a new list
    sortedAngleList = sorted(asteroidsByAngle.keys())

    # Loop through the list of sorted angles, adding the nearest asteroid to the list each pass until all coords have been added.
    coordsInVaporizationOrder = []
    sortedUniqueAngleList = sorted(list(set(sortedAngleList)))

    while True:
        failedChecks = 0
        for angle in sortedUniqueAngleList:
            if len(asteroidsByAngle[angle]) > 0:  # if there's at least one asteroid left at this angle
                closestAsteroidAtAngle = shortestDistance(asteroidsByAngle[angle])  # find the coords with shortest distance from station
                coordsInVaporizationOrder.append(closestAsteroidAtAngle)
                asteroidsByAngle[angle].remove(closestAsteroidAtAngle)  # remove coords from asteroid coord dict
            else:
                failedChecks += 1
        if failedChecks == len(sortedUniqueAngleList):
            # If we've failed to find coords for all angles in a pass, we've exhausted the list and we're done.
            return coordsInVaporizationOrder


if __name__ == '__main__':

    with open('day10_input.txt') as f:
        asteroidData = f.read()
    map_width = asteroidData.find('\n')  # determine length of map row by finding first newline
    asteroidData = asteroidData.replace('\n', '')  # strip out newline characters
    map_height = int( len(asteroidData)/map_width )

    # Populate coordinate dictionary of all asteroid locations
    asteroidMap = {}
    for idx, label in enumerate(asteroidData):
        x = idx % map_width
        y = floor(idx/map_width)
        asteroidMap[Asteroid(x, y)] = label

    try: # Load from cache if possible
        with open(path.join('cache','data.pickle'), 'r+b') as f:
            AllAsteroids, stationDetections = pickle.load(f)

    except FileNotFoundError:
        AllAsteroids = getAsteroids(asteroidMap)

        # Make a dict of each asteroid location with the number of other asteroids that can be detected from that point
        stationDetections = {}
        for Station in AllAsteroids:
            stationDetections[Station] = countDirectLOS(Station, AllAsteroids)

        with open(path.join('cache','data.pickle'), 'w+b') as f:
            pickle.dump((AllAsteroids, stationDetections), f)  # save cache

    ## Part 1 ##
    # Search dict for largest signal
    bestStationCount = 0
    for loc in stationDetections:
        if stationDetections[loc] > bestStationCount:
            bestStationCount = stationDetections[loc]
            bestStationLocation = loc

    print(f'[Part 1] Location ({bestStationLocation.x}, {bestStationLocation.y}) is optimal for monitoring station with {bestStationCount} asteroids in direct line of sight.')


    ## Part 2 ##
    coordsInVaporizationOrder = sortAsteroids(bestStationLocation, AllAsteroids)

    answer = toAbsCoords(bestStationLocation, coordsInVaporizationOrder[199])
    print(f'[Part 2] The 200th asteroid to be vaporized is at ({answer.x}, {answer.y}).')
