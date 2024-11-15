def find_a_path(start, end, obs):
    ret_path = -1
    searched_map = []
    for i in range(22):
        searched_map.append([-1 for j in range(17)])

    next_tiles = [start]
    cur_moves = -1

    while len(next_tiles) > 0:
        cur_tiles = [[next_tiles[i][0], next_tiles[i][1]] for i in range(len(next_tiles))]
        next_tiles.clear()
        cur_moves += 1
        for i in range(len(cur_tiles)):
            if (1 <= cur_tiles[i][0] <= 20 and 1 <= cur_tiles[i][1] <= 15) \
                    or cur_tiles[i] == start or cur_tiles[i] == end:
                if cur_tiles[i] not in obs and searched_map[cur_tiles[i][0]][cur_tiles[i][1]] == -1:
                    searched_map[cur_tiles[i][0]][cur_tiles[i][1]] = cur_moves
                    next_tiles.append([cur_tiles[i][0] + 1, cur_tiles[i][1]])  # right
                    next_tiles.append([cur_tiles[i][0], cur_tiles[i][1] + 1])  # down
                    next_tiles.append([cur_tiles[i][0] - 1, cur_tiles[i][1]])  # left
                    next_tiles.append([cur_tiles[i][0], cur_tiles[i][1] - 1])  # up

    ret_path = [end]
    bt_moves = searched_map[end[0]][end[1]]
    
    while ret_path[0] != start:
        bt_moves -= 1

        if ret_path[0][1] - 1 >= 0 and searched_map[ret_path[0][0]][ret_path[0][1] - 1] == bt_moves:
            ret_path.insert(0, [ret_path[0][0], ret_path[0][1] - 1])
        elif ret_path[0][1] + 1 <= 16 and searched_map[ret_path[0][0]][ret_path[0][1] + 1] == bt_moves:
            ret_path.insert(0, [ret_path[0][0], ret_path[0][1] + 1])
        elif ret_path[0][0] - 1 >= 0 and searched_map[ret_path[0][0] - 1][ret_path[0][1]] == bt_moves:
            ret_path.insert(0, [ret_path[0][0] - 1, ret_path[0][1]])
        elif ret_path[0][0] + 1 <= 21 and searched_map[ret_path[0][0] + 1][ret_path[0][1]] == bt_moves:
            ret_path.insert(0, [ret_path[0][0] + 1, ret_path[0][1]])
        else:
            return -1

    return ret_path
