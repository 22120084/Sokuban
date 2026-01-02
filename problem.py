from sokoban import GameState

class SearchProblem:
    def __init__(self, gameState: GameState, costFunc = lambda x: 1):    
        self.gameState = gameState
        self.costFunc = costFunc
        self.deadlocks = find_deadlock_cells(gameState)

    def getAresStart(self):
        return self.gameState.ares
	
    def getStonesStart(self):
        return self.gameState.stones

    def isGoalState(self, state):
        stones = state[1]
        return sorted(stones) == sorted(self.gameState.switches)

    def isLegalAction(self, state, action):
        ares = state[0]
        stones = state[1]
        attemptCoor = move_towards(ares, (action[0], action[1]))

        if attemptCoor in self.gameState.walls: # if it bumps into a wall 
            return False
        elif attemptCoor in stones: # if it bumps into a stone. Need to check more.
            if move_towards(attemptCoor, (action[0], action[1])) in self.gameState.walls:  # if a tile ahead is a wall.
                return False
            elif move_towards(attemptCoor, (action[0], action[1])) in stones: # if a tile ahead is another stone.
                return False
            elif move_towards(attemptCoor, (action[0], action[1])) in self.deadlocks: # if a tile ahead is deadlock cell
                return False

        return True

    def getSuccessors(self, state):
        actions = [[0, -1, 'u', 'U'], [0, 1, 'd', 'D'], [-1, 0, 'l', 'L'], [1, 0, 'r', 'R']]
        aresX, aresY = state[0]  # ares
        successors = []
        
        for action in actions:
            nextAresX, nextAresY = aresX + action[0], aresY + action[1]
            if (nextAresX, nextAresY) in state[1]:  # stones
                action.pop(2)
            else:
                action.pop(3)
            
            if self.isLegalAction(state, action):
                nextAresPos = (nextAresX, nextAresY)
                nextStonesPos = [list(x) for x in state[-1]]
                if action[-1].isupper():  # if pushing, update the position of stone
                    index = nextStonesPos.index(list(nextAresPos))
                    nextStonesPos.remove(list(nextAresPos))
                    nextStonesPos.insert(index, [nextAresX + action[0], nextAresY + action[1]])
                nextStonesPos = tuple(tuple(x) for x in nextStonesPos)
                cost = self.costFunc(nextAresPos)
                successors.append(((nextAresPos, nextStonesPos), action, cost))
            else: 
                continue
        
        return successors
    
def move_towards(ares, action):
    return (ares[0] + action[0], ares[1] + action[1])

def find_corner_cells(gameState: GameState): 
    corners = []
    for y in range(gameState.nrows):
        for x in range(gameState.ncols):
            if( not (x,y) in gameState.walls and not (x,y) in gameState.switches):
                if( ((x-1,y) in gameState.walls and (x,y-1) in gameState.walls) or 
                    ((x-1,y) in gameState.walls and (x,y+1) in gameState.walls) or
                    ((x+1,y) in gameState.walls and (x,y-1) in gameState.walls) or
                    ((x+1,y) in gameState.walls and (x,y+1) in gameState.walls)
                ):
                    corners.append((x,y))
    return corners

def find_deadlock_cells(gameState: GameState):
    corners = find_corner_cells(gameState)
    deadlocks = []
    for x,y in corners:
        for (dx,dy) in [(0,-1), (0,1), (-1,0), (1,0)]:
            checking_cell = (x + dx,y + dy)
            if dy == 0:        
                if(checking_cell in corners or checking_cell in gameState.walls or checking_cell in gameState.switches):
                    continue
                checking_cell = move_towards(checking_cell, (dx,dy))

                while(not checking_cell in corners):
                    if(checking_cell in gameState.switches or checking_cell in gameState.walls or checking_cell[0] < 0  or checking_cell[0] > gameState.ncols - 1):
                        break
                    checking_cell = move_towards(checking_cell, (dx,dy))

                if(checking_cell in gameState.switches or checking_cell in gameState.walls or checking_cell[0] < 0  or checking_cell[0] > gameState.ncols - 1):
                    continue

                t = []
                is_set_deadlock = True
                checking_cell = move_towards(checking_cell, (-dx,-dy))

                while(checking_cell != (x,y) ):                                                                                            
                    t.append((checking_cell))
                    checking_cell = move_towards(checking_cell, (-dx,-dy))

                for potential_deadlock in t :
                    if not ((potential_deadlock[0], potential_deadlock[1]-1) in gameState.walls) :
                        is_set_deadlock = False
                        break

                if(not is_set_deadlock):
                    is_set_deadlock = True
                    for potential_deadlock in t :
                        if not ((potential_deadlock[0], potential_deadlock[1]+1) in gameState.walls) :
                            is_set_deadlock = False
                            break

                if(not is_set_deadlock):
                    t = []
                
                deadlocks = deadlocks + t  

            if dx == 0:
                if(checking_cell in corners or checking_cell in gameState.walls or checking_cell in gameState.switches):
                    continue
                checking_cell = move_towards(checking_cell, (dx,dy))

                while(not checking_cell in corners):
                    if(checking_cell in gameState.switches or checking_cell in gameState.walls or checking_cell[1] < 0  or checking_cell[1] > gameState.nrows - 1):
                        break
                    checking_cell = move_towards(checking_cell, (dx,dy))

                if(checking_cell in gameState.switches or checking_cell in gameState.walls or checking_cell[1] < 0  or checking_cell[1] > gameState.nrows - 1):
                    continue

                t = []
                is_set_deadlock = True
                checking_cell = move_towards(checking_cell, (-dx,-dy))

                while(checking_cell != (x,y)):                                                                                     
                    t.append((checking_cell))
                    checking_cell = move_towards(checking_cell, (-dx,-dy))

                for potential_deadlock in t:
                    if not ((potential_deadlock[0]-1, potential_deadlock[1]) in gameState.walls) :
                        is_set_deadlock = False
                        break

                if(not is_set_deadlock):
                    is_set_deadlock = True
                    for potential_deadlock in t:
                        if not ((potential_deadlock[0]+1, potential_deadlock[1]) in gameState.walls) :
                            is_set_deadlock = False
                            break

                if(not is_set_deadlock):
                    t = []
                
                deadlocks = deadlocks + t  

    return list(set(corners + deadlocks))