import time
import tracemalloc
from problem import SearchProblem
from util import *

def breadthFirstSearch(problem: SearchProblem):
    start_time = time.time()  
    node_generated = 0

    queue = Queue()
    tracemalloc.start()
    explored = set()
    startState = (problem.getAresStart(), problem.getStonesStart())
    queue.push((startState, [], 0, 0))

    while not queue.isEmpty():
        node, path, cost, weight = queue.pop()
        
        if problem.isGoalState(node):
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory = peak / (1024 ** 2)  # Convert to MB
            return process_result('BFS', path, weight, node_generated, start_time, memory)
        
        if node not in explored:
            explored.add(node)
            node_generated += 1
            
            if node_generated >= 1000000:
                break

            for successor, action, step_cost in problem.getSuccessors(node):
                new_cost, new_weight = cost, weight
                if action[-1].isupper():  
                    stone_pos = (node[0][0] + action[0], node[0][1] + action[1])
                    stone_index = node[1].index(stone_pos)
                    new_cost += problem.gameState.weights[stone_index]
                    new_weight += problem.gameState.weights[stone_index]  
                queue.push((successor, path + [action[-1]], new_cost + step_cost, new_weight))

    return "No solution"

def depthFirstSearch(problem: SearchProblem):
    start_time = time.time()
    node_generated = 0

    stack = Stack()
    tracemalloc.start()
    explored = set()
    startState = (problem.getAresStart(), problem.getStonesStart())
    stack.push((startState, [], 0, 0))

    while not stack.isEmpty():
        node, path, cost, weight = stack.pop()
        
        if problem.isGoalState(node):
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory = peak / (1024 ** 2)  # Convert to MB
            return process_result('DFS', path, weight, node_generated, start_time, memory)
            
        if node not in explored:
            explored.add(node)
            node_generated += 1

            if node_generated >= 1000000:
                break

            for successor, action, step_cost in problem.getSuccessors(node):
                new_cost, new_weight = cost, weight
                if action[-1].isupper():  
                    stone_pos = (node[0][0] + action[0], node[0][1] + action[1])
                    stone_index = node[1].index(stone_pos)
                    new_cost += problem.gameState.weights[stone_index]
                    new_weight += problem.gameState.weights[stone_index]
                stack.push((successor, path + [action[-1]], new_cost + step_cost, new_weight))

    return "No solution"

def uniformCostSearch(problem: SearchProblem):
    start_time = time.time()
    node_generated = 0

    pq = PriorityQueue()
    tracemalloc.start()
    explored = set()
    startState = (problem.getAresStart(), problem.getStonesStart())
    pq.push((startState, [], 0, 0), 0)

    while not pq.isEmpty():
        node, path, cost, weight = pq.pop()
        
        if problem.isGoalState(node):
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory = peak / (1024 ** 2)  # Convert to MB
            return process_result('UCS', path, weight, node_generated, start_time, memory)
        
        if node not in explored:
            explored.add(node)
            node_generated += 1

            if node_generated >= 1000000:
                break

            for successor, action, step_cost in problem.getSuccessors(node):
                new_cost, new_weight = cost, weight
                if action[-1].isupper():  
                    stone_pos = (node[0][0] + action[0], node[0][1] + action[1])
                    stone_index = node[1].index(stone_pos)
                    new_cost += problem.gameState.weights[stone_index]
                    new_weight += problem.gameState.weights[stone_index]
                pq.push((successor, path + [action[-1]], new_cost + step_cost, new_weight), new_cost + step_cost)

    return "No solution"

def calc_manhattan(p1, p2):
    return sum(abs(sum1-sum2) for sum1, sum2 in zip(p1,p2))

def heuristic(node, problem: SearchProblem):
    ares_pos = node[0]
    stones_pos = node[1]
    heuristic_ares_distance = 0
    heuristic_stone_distance = 0

    min_ares_distance = None
    for i, stone_pos in enumerate(stones_pos):
        ares_distance = calc_manhattan(stone_pos, ares_pos) # Tính khoảng cách từ Ares đến viên đá gần nhất
        if min_ares_distance == None or ares_distance < min_ares_distance:
            min_ares_distance = ares_distance
        min_stone_distance = None                
        for switch_pos in problem.gameState.switches:
            stone_distance = calc_manhattan(stone_pos, switch_pos) * problem.gameState.weights[i] # Tính toán tổng chi phí di chuyển của từng viên đá đến mục tiêu gần nhất
            if min_stone_distance == None or stone_distance < min_stone_distance:
                min_stone_distance = stone_distance
        heuristic_stone_distance += min_stone_distance
    heuristic_ares_distance = min_ares_distance

    return heuristic_ares_distance + heuristic_stone_distance

def aStarSearch(problem: SearchProblem, heuristic=heuristic):
    start_time = time.time()
    node_generated = 0

    pq = PriorityQueue()
    tracemalloc.start()
    explored = set()
    startState = (problem.getAresStart(), problem.getStonesStart())
    pq.push((startState, [], 0, 0), 0)

    while not pq.isEmpty():
        node, path, cost, weight = pq.pop()
        
        if problem.isGoalState(node):
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop() 
            memory = peak / (1024 ** 2)  # Convert to MB
            return process_result('A*', path, weight, node_generated, start_time, memory)
        
        if node not in explored:
            explored.add(node)
            node_generated += 1

            if node_generated >= 1000000:
                break

            for successor, action, step_cost in problem.getSuccessors(node):
                new_cost, new_weight = cost, weight
                if action[-1].isupper():  
                    stone_pos = (node[0][0] + action[0], node[0][1] + action[1])
                    stone_index = node[1].index(stone_pos)
                    new_cost += problem.gameState.weights[stone_index]
                    new_weight += problem.gameState.weights[stone_index]
                heuristic_cost = heuristic(successor, problem)
                pq.push((successor, path + [action[-1]], new_cost + step_cost, new_weight), new_cost + step_cost + heuristic_cost)

    return "No solution"