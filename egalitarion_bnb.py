NUM_OF_PLAYERS = 2
ITEM_NUM_INDEX = NUM_OF_PLAYERS
PLAYER_ONE = 0
PLAYER_TWO = 1

def give_item_to_player(player_num, state, valuations, item_num):
    state[0][player_num]+=valuations[player_num][item_num]
    state[0][ITEM_NUM_INDEX]+=1
    state[player_num + 1].append(item_num)
    return state

def deep_copy(state):
    allocations = state[0].copy()
    player_one_items = state[1].copy()
    player_two_items = state[2].copy()
    return [allocations, player_one_items, player_two_items]

def get_key(state):
    return tuple(state[0][:-1])

def calc_pessimitic_bound(state, num_of_items, valuations, pessamistic_bound):
    items_allocated = state[0][ITEM_NUM_INDEX]
    ans = state[0][:-1].copy()
    for i in range(items_allocated, num_of_items):
        if i%2:
            ans[PLAYER_ONE] += valuations[PLAYER_ONE][i]
        else:
            ans[PLAYER_TWO] += valuations[PLAYER_TWO][i]
    pessamistic_bound = max(pessamistic_bound, min(ans))
    return pessamistic_bound

def calc_optimistic_bound(state, num_of_items, valuations):
    items_allocated = state[0][ITEM_NUM_INDEX]
    ans = state[0][:-1].copy()
    for i in range(items_allocated, num_of_items):    
        ans[PLAYER_ONE] += valuations[PLAYER_ONE][i]
        ans[PLAYER_TWO] += valuations[PLAYER_TWO][i]
    return min(ans)

def prune(queue, visited, pessamistic_bound, state, num_of_items, valuations):
    pessamistic_bound = calc_pessimitic_bound(state, num_of_items, valuations, pessamistic_bound)
    if (get_key(state) not in visited) and (calc_optimistic_bound(state, num_of_items, valuations) >= pessamistic_bound): #pruning  
        queue.append(state)
        visited[get_key(state)] = 1
    return pessamistic_bound
    
def branch_and_bound(root: list[list[int]], valuations: list[list[int]]):
    queue = []
    visited = {}
    pessamistic_bound = -float('inf')
    num_of_items = len(valuations[0])
    queue.append(root)
    ans = [[-float('inf'), -float('inf')], [], []]
    while queue:
        state = queue.pop(0)
        item_num = state[0][ITEM_NUM_INDEX]
        if item_num == len(valuations[0]): # is goal state
            if min(ans[0][:-1]) < min(state[0][:-1]):
                ans = state
            continue;
        left = give_item_to_player(PLAYER_ONE, deep_copy(state), valuations, item_num)
        right = give_item_to_player(PLAYER_TWO, deep_copy(state), valuations, item_num)
        pessamistic_bound = prune(queue, visited, pessamistic_bound, left, num_of_items, valuations)
        pessamistic_bound = prune(queue, visited, pessamistic_bound, right, num_of_items, valuations)
    return ans

def egalitarion_allocation(valuations: list[list[int]]):
    root_val = [[0 for _ in range(NUM_OF_PLAYERS + 1)], [], []]
    ans = branch_and_bound(root_val, valuations)
    print(f"player 0 takes items {', '.join([str(a + 1) for a in ans[1]])} with value {ans[0][PLAYER_ONE]}")
    print(f"player 1 takes items {', '.join([str(a + 1) for a in ans[2]])} with value {ans[0][PLAYER_TWO]}")

#without pruning, loops = 63
#without duplicates = 56
#without duplicates and pessamistic/optimisitic bound checking = 26
egalitarion_allocation([[4,5,6,7,8], [8,7,6,5,4]])

