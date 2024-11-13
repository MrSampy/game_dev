def parse_wave_info(file_name):
    file = open("data/" + file_name, "r")
    wave_info = []
    cur_wave = 0

    for line in file:
        if len(line.strip()) != 0:
            if line.split()[0] == 'wave':
                cur_wave = int(line.split()[1])
                while len(wave_info) < cur_wave:
                    wave_info.append([])
            else:
                cur_line = line.split()
                enemy_name = ' '.join(map(str, cur_line))
                cur_line = file.readline().split()
                amount = int(cur_line[0])
                delay = float(cur_line[1])
                interval = float(cur_line[2])
                wave_info[cur_wave - 1].append([enemy_name, amount, delay, interval])

    return wave_info