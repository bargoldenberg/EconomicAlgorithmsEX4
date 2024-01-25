NUM_OF_PLAYERS = 2
PLAYER_ONE = 0
PLAYER_TWO = 1

def give_item_to_player(player_num, state, valuations, item_num):
    state[0][player_num]+=valuations[player_num][item_num]
    state[0][NUM_OF_PLAYERS]+=1
    state[player_num + 1].append(item_num)
    return state

def deep_copy(state):
    allocations = state[0].copy()
    player_one_items = state[1].copy()
    player_two_items = state[2].copy()
    return [allocations, player_one_items, player_two_items]

def get_key(state):
    return tuple(state[0][:-1])

def branch_and_bound(root: list[list[int]], valuations: list[list[int]]):
    queue = []
    loops = 0
    visited = {}
    queue.append(root)
    ans = [[-float('inf'), -float('inf')], [], []]
    while queue:
        loops+=1
        state = queue.pop(0)
        item_num = state[0][NUM_OF_PLAYERS]
        if item_num == len(valuations[0]): # is goal state
            if min(ans[0][:-1]) < min(state[0][:-1]):
                ans = state
            continue;       
        left = give_item_to_player(PLAYER_ONE, deep_copy(state), valuations, item_num)
        right = give_item_to_player(PLAYER_TWO, deep_copy(state), valuations, item_num)
        if get_key(left) not in visited: #pruning
            queue.append(left)
            visited[get_key(left)] = 1
        if get_key(right) not in visited: #pruning
            queue.append(right)
            visited[get_key(right)] = 1 
    print(loops)
    return ans

def egalitarion_allocation(valuations: list[list[int]]):
    root_val = [[0 for _ in range(NUM_OF_PLAYERS + 1)], [], []]
    ans = branch_and_bound(root_val, valuations)
    print(f"player 0 takes items {', '.join([str(a + 1) for a in ans[1]])} with value {ans[0][PLAYER_ONE]}")
    print(f"player 1 takes items {', '.join([str(a + 1) for a in ans[2]])} with value {ans[0][PLAYER_TWO]}")

#without pruning, loops = 63
#without duplicates = 56

egalitarion_allocation([[4,5,6,7,8], [8,7,6,5,4]])

