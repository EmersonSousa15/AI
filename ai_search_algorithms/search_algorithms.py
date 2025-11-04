import numpy as np

from typing import NamedTuple
from itertools import count
from collections import deque


class Node(NamedTuple):
    STATE: str
    PARENT: 'Node | None'
    ACTION: str
    PATHCOST: int
    HEURISTIC: float
    DEPTH: int

def expand(problem, node):
    s = node.STATE
    for action in problem['actions'][s]:
        sl = problem['result'][(s,action)]
        cost = node.PATHCOST + problem['action_cost'][(s,action,sl)]
        yield Node(STATE=sl,PARENT=node,ACTION=action,
                   PATHCOST=cost,HEURISTIC=problem['heuristic'][sl],DEPTH=node.DEPTH+1)

def best_first_search(problem, method='bfs', depth=0):
    node = Node(STATE=problem['initial_state'], 
                PARENT= None,
                ACTION= None,  # type: ignore
                PATHCOST=0, 
                HEURISTIC=problem['heuristic'][problem['initial_state']],
                DEPTH=0)
    frontier = [node]
    reached = {problem['initial_state']: node}
    explored_nodes = 0
    while frontier != []:
        node = frontier.pop(0)
        explored_nodes += 1
        if node.STATE in problem['goal_state'] and (method!='dfs_limited'):
            print(f"Nós explorados: {explored_nodes}")
            return node
        
        for child in expand(problem,node):
            s = child.STATE
            if (s in problem['goal_state']) and (method=='dfs'):
                print(f"Nós explorados: {explored_nodes}")
                return child
            
            if (method=='bfs') and (s not in reached):
                reached[s] = child
                frontier.append(child)
                
            if (method=='dfs') and (s not in reached):  
                reached[s] = child
                frontier.insert(0, child)
                
            # Busca com profundidade limitada
            if (method=='dfs_limited') and (s not in reached):
                if node.STATE in problem['goal_state']:
                    print(f"Finalizando em profundidade {node.DEPTH}; Nós explorados: {explored_nodes}")
                    return node
                if node.DEPTH > depth:
                    print(f"Finalizando em profundidade {depth}; Nós explorados: {explored_nodes}")
                    return 'cutoff'
                elif not is_cycle(node):
                    for child in expand(problem,node):
                        frontier.insert(0, child)

                
            elif (method in ['uniform','a*','gbf']) and ((s not in reached) or (child.PATHCOST < reached[s].PATHCOST)):
                reached[s] = child
                frontier.append(child)
                if method == 'a*':
                    frontier = [frontier[i] for i in np.argsort([(n.PATHCOST + n.HEURISTIC) for n in frontier])]
                elif method == 'gbf':
                    frontier = [frontier[i] for i in np.argsort([n.HEURISTIC for n in frontier])]
                else:
                    frontier = [frontier[i] for i in np.argsort([n.PATHCOST for n in frontier])]
                    
    print(frontier)
    return False

def is_cycle(node: Node) -> bool:
    s = node.STATE
    p = node.PARENT
    while p is not None:
        if p.STATE == s:
            return True
        p = p.PARENT
    return False

# iterative_deepening_search (busca em profundidade iterativa)
def iterative_deepening_search(problem):
    for depth in count(0):
        result = best_first_search(problem, method='dfs_limited', depth=depth)
        if result != 'cutoff':
            return result

'''
# depth_first_search (busca em profundidade)
def depth_first_search(problem):
    node = Node(STATE=problem['initial_state'], 
                PARENT= None,
                ACTION= None,  # type: ignore
                PATHCOST=0, 
                HEURISTIC=problem['heuristic'][problem['initial_state']],
                DEPTH=0)
    if node.STATE in problem['goal_state']:
        return node
    frontier = [node]
    reached = {problem['initial_state']}
    explored_nodes = 0
    while frontier != []:
        node = frontier.pop()
        explored_nodes += 1
        for child in expand(problem,node):
            s = child.STATE
            if s in problem['goal_state']:
                print(f"Nós explorados: {explored_nodes}")
                return child
            if s not in reached:
                reached.add(s)
                frontier.append(child)
                print([n.STATE for n in frontier])
    return False



# depth_limited_search (busca em profundidade limitada)
def depth_limited_search(problem, depth):
    node = Node(STATE=problem['initial_state'], 
                PARENT= None,
                ACTION= None,  # type: ignore
                PATHCOST=0, 
                HEURISTIC=problem['heuristic'][problem['initial_state']],
                DEPTH=0)
    frontier = [node]
    explored_nodes = 0
    while frontier !=[]:
        node = frontier.pop()
        explored_nodes += 1
        if node.STATE in problem['goal_state']:
            print(f"Finalizando em profundidade {node.DEPTH}; Nós explorados: {explored_nodes}")
            return node
        if node.DEPTH > depth:
            print(f"Finalizando em profundidade {depth}; Nós explorados: {explored_nodes}")
            return 'cutoff'
        elif not is_cycle(node):
            for child in expand(problem,node):
                frontier.append(child)
'''
    