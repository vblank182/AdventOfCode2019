## Advent of Code 2019: Day 6
## https://adventofcode.com/2019/day/6
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 158090, [Part 2]: 241

from treelib import Tree, Node

def parseOrbits(orbitData):
    # Returns a list of orbit tuples
    orbits = []
    for orbitStr in orbitData:
        orbit = orbitStr.split(')')
        orbits.append((orbit[0], orbit[1]))
    return orbits

def populateMap(orbits, orbitMap):
    orbitMap.create_node(tag="COM", identifier="COM")  # root node (center of mass)
    # Initially (since we don't know what order the nodes will be read in), set all nodes as children of COM.
    for orbit in orbits:  # first pass
        orbitMap.create_node(tag=orbit[1], identifier=orbit[1], parent="COM")

    # Now, re-assign each node to the correct parent
    for orbit in orbits:  # second pass
        orbitMap.move_node(orbit[1], orbit[0])

    return orbitMap

if __name__ == '__main__':
    orbitMap = Tree()

    with open('day06_input.txt') as f:
        orbitData = [line[:-1] for line in f.readlines()]

    # Get list of orbit tuples
    orbits = parseOrbits(orbitData)

    # Make a tree out of orbit data
    orbitMap = populateMap(orbits, orbitMap)

    ## Part 1 ##
    # Calculate total distances of each nodes from root (COM)
    totalDist = 0
    for node in orbitMap.all_nodes():
        totalDist += orbitMap.level(node.identifier)

    print("[Part 1] Orbit count checksum: {}".format(totalDist))


    ## Part 2 ##
    # Find the YOU and SAN nodes
    node_you = orbitMap.get_node("YOU")
    node_santa = orbitMap.get_node("SAN")

    node_ptr = node_you  # start at YOU node
    while node_ptr is not None:
        if orbitMap.is_ancestor(node_ptr.identifier, node_santa.identifier):
            # This node is a direct ancestor of the SAN node.
            # Create a submap with this node as the root. (This should be the smallest tree including both YOU and SAN.)
            orbitSubmap = orbitMap.subtree(node_ptr.identifier)
            break
        else:
            # Take a step towards the root and try again.
            node_ptr = orbitMap.parent(node_ptr.identifier)

    # Calculate the number of transfers needed by checking the depth of each node from their common root in the subtree.
    # (Subtracting 2 to account for the way transfers are defined in the problem.)
    num_transfers = orbitSubmap.level(node_you.identifier) + orbitSubmap.level(node_santa.identifier) - 2

    print("[Part 2] Number of orbital transfers required: {}".format(num_transfers))

    #orbitMap.show()
