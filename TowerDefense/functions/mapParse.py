def parse_coords(file_name):
    file = open("data/maps/" + file_name, "r")
    map_info = [[], [], []]
    cur_line = file.readline().split()
    cur_line = ' '.join(map(str, cur_line))
    map_info[0].append(cur_line)
    cur_line = file.readline().split()
    map_info[0].append(cur_line)
    cur_line = file.readline().split()
    map_info[0].append(cur_line)
    cur_mode = "spawns"
    for line in file:
        cur_line = line.split()
        if cur_line[0] == "spawns":
            cur_mode = "spawns"
        elif cur_line[0] == "obstacles":
            cur_mode = "obstacles"
        elif cur_mode == "spawns":
            map_info[1].append(cur_line)
        elif cur_mode == "obstacles":
            map_info[2].append(cur_line)

    return map_info

