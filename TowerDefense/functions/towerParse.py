def get_stats(name):
    data_file = open("data/towerData", "r")
    stat_list = {}
    start_read = False

    for line in data_file:
        if len(line.strip()) != 0:
            if start_read:
                cur_line = line.split()
                if cur_line[0] == "end":
                    return stat_list
                stat_key = cur_line[0]
                stat_val = cur_line[1:]
                stat_list[str(stat_key)] = stat_val
            else:
                if line.split()[0] == "name":
                    cur_line = ' '.join(map(str, line.split()[1:]))
                    if cur_line == name:
                        start_read = True
