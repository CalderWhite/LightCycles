from LightCycles.Racer import Racer

def findSpace(Map):
    numRows = len(Map)
    numCols = len(Map[0])
    maxRow = 50 # default center
    maxCol = 50
    count = 0
    
    for i in range(numRows):
        empty = Map[i].count(0)
        if empty > count:
            maxRow = i
            count = empty

    count = 0
    for i in range(numCols):
        col = [r[i] for r in Map]
        empty = col.count(0)
        if empty > count:
            maxCol = i
            count = empty

    return maxRow, maxCol

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
                                ret = spaceCol(r+1, i, 1, Map, currentDepth, maxDepth, space+pspace, maxpspace//5, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                        if r-1 != -1:
                            if Map[r-1][i] == 0:
                                gaps += 1
                                ret = spaceCol(r-1, i, -1, Map, currentDepth, maxDepth, space+pspace, maxpspace//5, checked, maxGaps)
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
                                ret = spaceCol(r+1, i, 1, Map, currentDepth, maxDepth, space+pspace, maxpspace//5, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                        if r-1 != -1:
                            if Map[r-1][i] == 0:
                                gaps += 1
                                ret = spaceCol(r-1, i, -1, Map, currentDepth, maxDepth, space+pspace, maxpspace//5, checked, maxGaps)
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
                    #checked.append((r, i))
                else:
                    break
                if space+pspace > maxpspace:
                    return space, checked
        else:
            for i in range(c, -1, -1):
                if Map[r][i] == 0 and (r, i) not in checked:
                    space += 1
                    #checked.append((r, i))
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
                                ret = spaceRow(i, c+1, 1, Map, currentDepth, maxDepth, space+pspace, maxpspace//5, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                        if c-1 != -1:
                            if Map[i][c-1] == 0:
                                gaps += 1
                                ret = spaceRow(i, c-1, -1, Map, currentDepth, maxDepth, space+pspace, maxpspace//5, checked, maxGaps)
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
                                ret = spaceRow(i, c+1, 1, Map, currentDepth, maxDepth, space+pspace, maxpspace//5, checked, maxGaps)
                                space += ret[0]
                                checked = ret[1]
                        if c-1 != -1:
                            if Map[i][c-1] == 0:
                                gaps += 1
                                ret = spaceRow(i, c-1, -1, Map, currentDepth, maxDepth, space+pspace, maxpspace//5, checked, maxGaps)
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
                    #checked.append((i, c))
                    space += 1
                else:
                    break
                if space+pspace > maxpspace:
                    return space, checked
        else:
            for i in range(r, -1, -1):
                if Map[i][c] == 0 and (i, c) not in checked:
                    c#hecked.append((i, c))
                    space += 1
                else:
                    break
                if space+pspace > maxpspace:
                    return space, checked
    return space, checked

def findMove(Map, r, c):
    numRows = len(Map)
    numCols = len(Map[0])
    col = [row[c] for row in Map]
    row = Map[r]
    
##    col1 = pathLength(col[:c], -1)
##    col2 = pathLength(col[c:], 1)
##    row1 = pathLength(row[:r], -1)
##    row2 = pathLength(row[r:], 1)
    if 0 <= r-1 < numRows:
        if Map[r-1][c] == 0:
            col1 = spaceCol(r-1, c, -1, Map, 0, 50, 0, 10000, [], 50)[0]
        else:
            col1 = 0
    else:
        col1 = 0

    if 0 <= r+1 < numRows:
        if Map[r+1][c] == 0:
            col2 = spaceCol(r+1, c, 1, Map, 0, 50, 0, 10000, [], 50)[0]
        else:
            col2 = 0
    else:
        col2 = 0

    if 0 <= c-1 < numCols:
        if Map[r][c-1] == 0:
            row1 = spaceRow(r, c-1, -1, Map, 0, 50, 0, 10000, [], 50)[0]
        else:
            row1 = 0
    else:
        row1 = 0

    if 0 <= c+1 < numCols:
        if Map[r][c+1] == 0:
            row2 = spaceRow(r, c+1, -1, Map, 0, 50, 0, 10000, [], 50)[0]
        else:
            row2 = 0
    else:
        row2 = 0
    
    dirQ = [[(-1, 0), col1], [(1, 0), col2], [(0, -1), row1], [(0, 1), row2]]
    dirQ.sort(key=lambda x: x[1])
    dirQ = dirQ[::-1]
    #print(dirQ)
    for Dir in dirQ:
        tr = r+Dir[0][0]
        tc = c+Dir[0][1]
        if tr < numRows and tr >= 0 and tc < numCols and tc >= 0:
            if Map[tr][tc] == 0:
                return Dir[0], dirQ
    return (0,0), dirQ

class SpaceHunter(Racer):
    direction = 0
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    lastMove = directions[1]
    lastSpace = 0

    def __init__(self, start_row, start_col, grid_width):
        super().__init__(start_row, start_col, grid_width)

    def get_next_move(self, racer_positions, Map):
        r, c = self.get_pos()
        move, dirQ = findMove(Map, r, c)

        for Dir in dirQ:
            if Dir[0] == self.lastMove:
                if self.lastSpace/(Dir[1]+1) <= 0.8 or self.lastSpace/(Dir[1]+1) >= 1.2:
                    self.lastMove = move
                    for Dir in dirQ:
                        if Dir[0] == move:
                            self.lastSpace = Dir[1]
                            break
                    return self.lastMove
                else:
                    break

        return self.lastMove
        #if minScore < 1500:
        #    return move
    
        numRows = len(Map)
        numCols = len(Map[0])
        tr, tc = findSpace(Map)
        #print(self.color)
        dr = tr-r
        dc = tc-c

        dnr = normalize(dr)
        dnc = normalize(dc)

        if abs(dr)>=abs(dc):
            direction = (dnr, 0)
        else:
            direction = (0, dnc)

        if direction == (0,0):
            return Move

        if r+direction[0] >= numRows or c+direction[1] >= numCols or r+direction[0] < 0 or c+direction[1] < 0:
            return Move
        
        if Map[r+direction[0]][c+direction[1]] != 0:
            return Move

        return direction
