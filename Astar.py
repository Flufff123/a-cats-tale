'''
This program is used by fleas and ticks to find the shortest path from their current position to the player, avoiding obtacles on the map.
Gcost = Cost from the start node to the current node.
Hcost = Estimated cost from the current node to the end node (heuristic).
Fcost = Total estimated cost of the path through this node:
F = G + H

OpenList = valid neighbour tiles waiting to be explored.
ClosedList =  tiles that have already been explored.
'''

# Calc estimated cost of the path through this node to the end node.
def calcCosts(tile, endNode, Gcost):
    Hcost = abs(tile[0] - endNode[0]) + abs(tile[1] - endNode[1])
    Fcost = Gcost + Hcost
    return Hcost, Fcost # Returns estimated cost form current node to end node and tot estimated cost.

# A* pathfinding algorithm.
def astar(row,col,backArray,midCol,midRow): 
    startNode = [col,row] # Current enemy pos on array.
    endNode = [midCol,midRow] # Current player pos on array.
    Hcost, Fcost = calcCosts(startNode, endNode, 0)
    openList = [[Fcost, 0, Hcost, startNode[0], startNode[1], None]] # Start node is the only one fully explored. openList format: [Fcost, Gcost, Hcost, column, row, parentIndex]
    closedList = [] # No nodes fully explored yet.
    path = []

    found = False
    while len(openList) > 0:
        openList.sort(key=lambda n: (n[0], n[2]))  # sort by Fcost, then Hcost.
        currentNode = openList.pop(0)
        closedList.append(currentNode) # Remove currentNode from openList and add to closedList now it is fully explored.

        if currentNode[3] == endNode[0] and currentNode[4] == endNode[1]: # Current node = end node?
            found = True
            if len(path) == 0: # I.e. current pos is the same as that of the player.
                path = [[col,row]]
            break

        adjacentNodes = [[-1,0],[1,0],[0,-1],[0,1]] # Nodes to explore are: left, right, up, down (no diagonal).

        for move in adjacentNodes: # Try each adjacent node to the current tile in turn.
            newColumn = currentNode[3] + move[0]
            newRow = currentNode[4] + move[1]

            if 0 <= newColumn < len(backArray[0]) and 0 <= newRow < len(backArray): # New tile within bounds of array?
                if backArray[newRow][newColumn] in [1,3]: # Check new tile is traverseable.
                    skip = False
                    for node in closedList: # Check if the new tile has already been explored.
                        if node[3] == newColumn and node[4] == newRow:
                            skip = True # If so skip this tile.
                            break
                    if skip == True:
                        continue # Node already explored so skip to next iteration of the FOR loop to try another node.

                    newGcost = currentNode[1] + 1
                    Hcost, Fcost = calcCosts([newColumn, newRow], endNode, newGcost) # Node not already explored so calc its costs.

                    betterPathFound = False
                    for node in openList:
                        if node[3] == newColumn and node[4] == newRow: # Check a shorter path to the node has not already been found.
                            if newGcost < node[1]:
                                node[1] = newGcost
                                node[0] = newGcost + node[2]
                                node[5] = len(closedList) - 1
                            betterPathFound = True
                            break

                    if not betterPathFound: # No better path to this node so add this to the set of nodes still being explored.
                        openList.append([Fcost, newGcost, Hcost, newColumn, newRow, len(closedList)-1])

    # Reconstruct path.
    path = []
    if found: # ... But only if a path was actually found.
        current = closedList[-1]
        while current[5] is not None: # current[5] contains the parent of the current node: loop repeats as long as the current node has a parent.
            path.append([current[3], current[4]]) # Append the current node's grid coordinates to the path.
            current = closedList[current[5]] # The new current node is the parent node (working backwards from end to start node).
        path.append([startNode[0], startNode[1]])
        path.reverse() # Must reverse the path to get it from start to end node.
    return path

import random