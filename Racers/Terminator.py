from LightCycles.Racer import Racer

SPACE_SEARCH_BREADTH = 3 # higher is not nec. better

def findSpace(r, c, Map, depthMap, sampledMap):
    mapRows = len(Map)
    mapCols = len(Map[0])
    numRows = len(sampledMap)
    numCols = len(sampledMap[0])
    sortedRows = []
    sortedCols = []
    
    for i in range(numRows):
        empty = sampledMap[i].count(0)
        sortedRows.append((i, empty))

    for i in range(numCols):
        col = [r[i] for r in sampledMap]
        empty = col.count(0)
        sortedCols.append((i, empty))

    sortedRows.sort(key=lambda x: x[1])
    sortedCols.sort(key=lambda x: x[1])
    
    for row in sortedRows:
        for col in sortedCols:
            trow = int(row[0]*mapRows/numRows)
            tcol = int(col[0]*mapCols/numCols)
            for dx in range(-SPACE_SEARCH_BREADTH, SPACE_SEARCH_BREADTH):
                for dy in range(-SPACE_SEARCH_BREADTH, SPACE_SEARCH_BREADTH):
                        ttrow = trow+dx
                        ttcol = tcol+dy
                        if 0<=ttrow<mapRows and 0<=ttcol<mapCols:
                            if depthMap[ttrow][ttcol] != 9999 and Map[ttrow][ttcol] == 0 and (ttrow != r and ttcol != c):
                                return ttrow, ttcol, depthMap[ttrow][ttcol] 
        
    return numRows//2, numCols//2, 9999

def depthMap(r, c, Map, maxDepth):
    numRows = len(Map)
    numCols = len(Map[0])
    tMap = [[0 for i in range(numCols)] for j in range(numRows)]

    for i in range(numRows):
        for j in range(numCols):
            if Map[i][j] == 0:
                tMap[i][j] = 9999
            else:
                tMap[i][j] = -1

    tMap[r][c] = 0
    endPoints = [(r, c)]
    tree = [[(r, c)]]
    for depth in range(maxDepth):
        tendPoints = endPoints.copy()
        endPoints = []
        for coord in tendPoints:
            if 0<=coord[0]+1<numRows:
                if tMap[coord[0]+1][coord[1]] > depth+1 and tMap[coord[0]+1][coord[1]] != -1:
                    tMap[coord[0]+1][coord[1]] = depth+1
                    endPoints.append((coord[0]+1, coord[1]))
            if 0<=coord[0]-1<numRows:
                if tMap[coord[0]-1][coord[1]] > depth+1 and tMap[coord[0]-1][coord[1]] != -1:
                    tMap[coord[0]-1][coord[1]] = depth+1
                    endPoints.append((coord[0]-1, coord[1]))
            if 0<=coord[1]+1<numCols:
                if tMap[coord[0]][coord[1]+1] > depth+1 and tMap[coord[0]][coord[1]+1] != -1:
                    tMap[coord[0]][coord[1]+1] = depth+1
                    endPoints.append((coord[0], coord[1]+1))
            if 0<=coord[1]-1<numCols:
                if tMap[coord[0]][coord[1]-1] > depth+1 and tMap[coord[0]][coord[1]-1] != -1:
                    tMap[coord[0]][coord[1]-1] = depth+1
                    endPoints.append((coord[0], coord[1]-1))
        tree.append(endPoints)

    return tMap, tree

def dom(array):
    numZ = sum([subarray.count(0) for subarray in array])
    if numZ > sum([len(subarray) for subarray in array])/2:
        return 0
    return 1

def sample(Map, n):
    sampled = []
    for row in range(0,len(Map),n):
        srow = []
        for col in range(0, len(Map[0]), n):
            srow.append(dom([x[col:col+n] for x in Map[row:row+n]]))
        sampled.append(srow)
    return sampled

def sampleToQuarterQuadrants(Map):
    tMap = Map.copy()
    while len(tMap) > 8:
        tMap = sample(tMap, 2)
    return tMap

def normalize(x):
    if x>0:
        return 1
    elif x<0:
        return -1
    else:
        return 0

def pathLength(path, direction):
    Len = 0
    if direction == -1:
        for i in range(len(path)-1, -1, -1):
            if path[i] == 0:
                Len += 1
            else:
                break
    else:
        for i in range(len(path)):
            if path[i] == 0:
                Len += 1
            else:
                break
    return Len

def spaceRow(r, c, direction, Map, currentDepth, maxDepth, pspace, maxpspace, checked, maxGaps):
    # space in a row
    currentDepth += 1
    space = 0
    numRows = len(Map)
    numCols = len(Map[0])
    gaps = 0
    if r>=numRows or c>=numCols or r<0 or c<0:
        return 0, None
    if currentDepth <= maxDepth and pspace < maxpspace:
        if direction == 1:
            for i in range(c, numCols):
                if (r, i) not in checked:
                    if Map[r][i] == 0:
                        space += 1
                        checked.append((r, i))
                        if r+1 != numRows:
                            if Map[r+1][i] == 0:
                                gaps += 1
                                ret = spaceCol(r+1, i, 1, Map, currentDepth, maxDepth, space+pspace, maxpspace, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                        if r-1 != -1:
                            if Map[r-1][i] == 0:
                                gaps += 1
                                ret = spaceCol(r-1, i, -1, Map, currentDepth, maxDepth, space+pspace, maxpspace, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                    else:
                        break
                else:
                    break
                if gaps > maxGaps:
                    break
                if space+pspace > maxpspace:
                    return space, checked
        else:
            for i in range(c, -1, -1):
                if (r, i) not in checked:
                    if Map[r][i] == 0:
                        space += 1
                        checked.append((r, i))
                        if r+1 != numRows:
                            if Map[r+1][i] == 0:
                                gaps += 1
                                ret = spaceCol(r+1, i, 1, Map, currentDepth, maxDepth, space+pspace, maxpspace, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                        if r-1 != -1:
                            if Map[r-1][i] == 0:
                                gaps += 1
                                ret = spaceCol(r-1, i, -1, Map, currentDepth, maxDepth, space+pspace, maxpspace, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                    else:
                        break
                else:
                    break
                if gaps > maxGaps:
                    break
                if space+pspace > maxpspace:
                    return space, checked
    else:
        if direction == 1:
            for i in range(c, numCols):
                if Map[r][i] == 0 and (r, i) not in checked:
                    space += 1
                    checked.append((r, i))
                else:
                    break
                if space+pspace > maxpspace:
                    return space, checked
        else:
            for i in range(c, -1, -1):
                if Map[r][i] == 0 and (r, i) not in checked:
                    space += 1
                    checked.append((r, i))
                else:
                    break
                if space+pspace > maxpspace:
                    return space, checked
    return space, checked
    
def spaceCol(r, c, direction, Map, currentDepth, maxDepth, pspace, maxpspace, checked, maxGaps):
    # space in a row
    # edge case: loops
    currentDepth += 1
    space = 0
    numRows = len(Map)
    numCols = len(Map[0])
    gaps = 0
    if r>=numRows or c>=numCols or r<0 or c<0:
            return 0, None
    if currentDepth <= maxDepth and pspace < maxpspace:
        if direction == 1:
            for i in range(r, numRows):
                if (i, c) not in checked:
                    if Map[i][c] == 0:
                        space += 1
                        checked.append((i, c))
                        if c+1 != numRows:
                            if Map[i][c+1] == 0:
                                gaps += 1
                                ret = spaceRow(i, c+1, 1, Map, currentDepth, maxDepth, space+pspace, maxpspace, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                        if c-1 != -1:
                            if Map[i][c-1] == 0:
                                gaps += 1
                                ret = spaceRow(i, c-1, -1, Map, currentDepth, maxDepth, space+pspace, maxpspace, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                    else:
                        break
                else:
                    break
                if gaps > maxGaps:
                    break
                if space+pspace > maxpspace:
                    return space, checked
        else:
            for i in range(r, -1, -1):
                if (i, c) not in checked:
                    if Map[i][c] == 0:
                        space += 1
                        checked.append((i, c))
                        if c+1 != numRows:
                            if Map[i][c+1] == 0:
                                gaps += 1
                                ret = spaceRow(i, c+1, 1, Map, currentDepth, maxDepth, space+pspace, maxpspace, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                        if c-1 != -1:
                            if Map[i][c-1] == 0:
                                gaps += 1
                                ret = spaceRow(i, c-1, -1, Map, currentDepth, maxDepth, space+pspace, maxpspace, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                    else:
                        break
                else:
                    break
                if gaps > maxGaps:
                    break
                if space+pspace > maxpspace:
                    return space, checked
    else:
        if direction == 1:
            for i in range(r, numRows):
                if Map[i][c] == 0 and (i, c) not in checked:
                    checked.append((i, c))
                    space += 1
                else:
                    break
                if space+pspace > maxpspace:
                    return space, checked
        else:
            for i in range(r, -1, -1):
                if Map[i][c] == 0 and (i, c) not in checked:
                    checked.append((i, c))
                    space += 1
                else:
                    break
                if space+pspace > maxpspace:
                    return space, checked
    return space, checked

def trace(r, c, tr, tc, tree, targetDist, Map):
    if targetDist == 9999:
        return [(r, c), (r, c)]
    path = []
    #print(targetDist)
    #print(len(tree))
    try:
        lastP = tree[targetDist][tree[targetDist].index((tr, tc))]
    except:
        return [(r, c), (r, c)]

    for i in range(targetDist-1, -1, -1):
        for j in range(len(tree[i])):
            point = tree[i][j]
            if abs(point[0]-lastP[0])+abs(point[1]-lastP[1]) == 1 and Map[point[0]][point[1]] != -1:
                path.append(lastP)
                lastP = point
                break
    return path

def dist_squared(coord1, coord2):
    r1, c1 = coord1
    r2, c2 = coord2
    return (r1-r2)**2+(c1-c2)**2

def findMove(Map, r, c, racer_positions):
    close = False
    if (r+1, c+1) in racer_positions:
        corner = (r+1, c+1)
        close = True
    elif (r-1, c-1) in racer_positions:
        corner = (r-1, c-1)
        close = True
    elif (r+1, c-1) in racer_positions:
        corner = (r+1, c-1)
        close = True
    elif (r-1, c+1) in racer_positions:
        corner = (r-1, c+1)
        close = True
    elif (r, c+1) in racer_positions:
        corner = (r, c+1)
        close = True
    elif (r, c-1) in racer_positions:
        corner = (r, c-1)
        close = True
    elif (r-1, c) in racer_positions:
        corner = (r-1, c)
        close = True
    elif (r+1, c) in racer_positions:
        corner = (r+1, c)
        close = True

    potentialTrap = False
    if (r+2, c+1) in racer_positions:
        corner2 = (r+2, c+1)
        potentialTrap = True
    elif (r+2, c-1) in racer_positions:
        corner2 = (r+2, c-1)
        potentialTrap = True
    elif (r+1, c-2) in racer_positions:
        corner2 = (r+1, c-2)
        potentialTrap = True
    elif (r+1, c+2) in racer_positions:
        corner2 = (r+1, c+2)
        potentialTrap = True
    elif (r-2, c+1) in racer_positions:
        corner2 = (r-2, c+1)
        potentialTrap = True
    elif (r-2, c-1) in racer_positions:
        corner2 = (r-2, c-1)
        potentialTrap = True
    elif (r-1, c-2) in racer_positions:
        corner2 = (r-1, c-2)
        potentialTrap = True
    elif (r-1, c+2) in racer_positions:
        corner2 = (r-1, c+2)
        potentialTrap = True 
    
    numRows = len(Map)
    numCols = len(Map[0])
    col = [row[c] for row in Map]
    row = Map[r]

    sampledMap = sampleToQuarterQuadrants(Map) # smth smaller than a 64 by 64 array
    rowQuad = int(len(sampledMap)/numRows*r)
    colQuad = int(len(sampledMap[0])/numCols*c)
    
    
    if 0 <= r-1 < numRows:
        if Map[r-1][c] == 0:
            col1 = spaceCol(r-1, c, -1, Map, 0, 10, 0, 400, [], 5)[0]
        else:
            col1 = 0
    else:
        col1 = 0

    if 0 <= r+1 < numRows:
        if Map[r+1][c] == 0:
            col2 = spaceCol(r+1, c, 1, Map, 0, 10, 0, 400, [], 5)[0]
        else:
            col2 = 0
    else:
        col2 = 0

    if 0 <= c-1 < numCols:
        if Map[r][c-1] == 0:
            row1 = spaceRow(r, c-1, -1, Map, 0, 10, 0, 400, [], 5)[0]
        else:
            row1 = 0
    else:
        row1 = 0

    if 0 <= c+1 < numCols:
        if Map[r][c+1] == 0:
            row2 = spaceRow(r, c+1, -1, Map, 0, 10, 0, 400, [], 5)[0]
        else:
            row2 = 0
    else:
        row2 = 0

    # check if going towards good quarter-quadrant
    dirQP = []
    
    col = [sampledMap[x][colQuad] for x in range(len(sampledMap))]
    row = sampledMap[rowQuad]

    dirQP.append([(-1, 0), col1])
    dirQP.append([(1, 0), col2])
    dirQP.append([(0, -1), row1])
    dirQP.append([(0, 1), row2])
    
    dirQP.sort(key=lambda x: x[1])
    dirQP = dirQP[::-1]

    # target empty space, default center
    depthMapM, tree = depthMap(r, c, Map.copy(), 80)

    tr, tc, targetDist = findSpace(r, c, Map, depthMapM, sampledMap)
    path = trace(r, c, tr, tc, tree, targetDist, Map)
    
    dr = path[-1][0]-r
    dc = path[-1][1]-c

    dnr = normalize(dr)
    dnc = normalize(dc)

    if abs(dr)>=abs(dc):
        direction = (dnr, 0)
    else:
        direction = (0, dnc)

    enemyRoutes = []
    for enemy in racer_positions:
        er, ec = enemy
        for dr in range(-SPACE_SEARCH_BREADTH, SPACE_SEARCH_BREADTH):
            for dc in range(-SPACE_SEARCH_BREADTH, SPACE_SEARCH_BREADTH):
                ter = er+dr
                tec = ec+dc
                if 0<=ter<numRows and 0<=tec<numCols and Map[ter][tec] == 0:
                    tpath = trace(r, c, ter, tec, tree, depthMapM[ter][tec], Map)
                    tdr = tpath[-1][0]-r
                    tdc = tpath[-1][1]-c
                    if tdr != 0 or tdc != 0:
                        if abs(tdr)>=abs(tdc):
                            tdir = (tdr, 0)
                        else:
                            tdir = (0, tdc)
                        if Map[r+tdir[0]][c+tdir[1]] == 0:
                            enemyRoutes.append(tdir)
                    break

    ndirQP = dirQP.copy()

    if len(racer_positions) != 1:
        if close == True:
            for i in range(len(ndirQP)):
                if dist_squared((r+ndirQP[i][0][0], c+ndirQP[i][0][1]), corner) <= 2:
                    for diR in dirQP:
                        if diR[0] == corner:
                            dirQP.remove(diR)
                            break

        if potentialTrap == True:
            for i in range(len(ndirQP)):
                if dist_squared((r+ndirQP[i][0][0], c+ndirQP[i][0][1]), corner2) <= 5:
                    for diR in dirQP:
                        if diR[0] == corner2:
                            dirQP.remove(diR)
                            break 
    else:
        for route in enemyRoutes:
            if route in [x[0] for x in dirQP]:
                for DirC in dirQP:
                    if DirC[0] == route:
                        score = DirC[1]
                        break
                bestMove, bestScore = dirQP[0]
                if abs(score-bestScore) <= bestScore*0.05:
                    return route, dirQP

    if direction in [x[0] for x in dirQP]:
        for DirC in dirQP:
            if DirC[0] == direction:
                score = DirC[1]
                break
        bestMove, bestScore = dirQP[0]
        if abs(score-bestScore) <= bestScore*0.4:
            return direction, dirQP

    for Dir in dirQP:
        tr = r+Dir[0][0]
        tc = c+Dir[0][1]
        if tr < numRows and tr >= 0 and tc < numCols and tc >= 0:
            if Map[tr][tc] == 0:
                return Dir[0], dirQP
    #UNREACHABLE
    return (0,0), dirQP

class Terminator(Racer):
    direction = 0
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    def __init__(self, start_row, start_col, grid_width):
        super().__init__(start_row, start_col, grid_width)

    def get_next_move(self, racer_positions, Map):
        r, c = self.get_pos()
        racer_positions.remove((r, c))
        move, dirQ = findMove(Map, r, c, racer_positions)

        return move
