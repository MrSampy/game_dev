from game_dev.TowerDefense.functions import mapParse
from game_dev.TowerDefense.functions import pathFinder
import pygame


class Map(object):
    def __init__(self, name):
        info = mapParse.parse_coords(name)
        self.mapName = info[0][0]
        self.colBackground = [int(x) for x in info[0][1]]
        self.colObs = [int(x) for x in info[0][2]]
        self.colGrid = [x - 20 for x in self.colBackground]

        self.spawnList = []
        self.exitList = []
        self.obsList = []
        self.obsPxList = []
        for i in range(len(info[1])):
            self.spawnList.append([int(info[1][i][0]), int(info[1][i][1])])
            self.exitList.append([int(info[1][i][2]), int(info[1][i][3])])
        for i in range(len(info[2])):
            self.obsList.append([int(info[2][i][0]), int(info[2][i][1]),
                                 int(info[2][i][2]), int(info[2][i][3])])
            self.obsPxList.append(pygame.Rect(int(info[2][i][0]) * 50 - 50, int(info[2][i][1]) * 50 - 50,
                                              int(info[2][i][2]) * 50, int(info[2][i][3]) * 50))

    def draw_obstacles(self, display):
        for i in range(len(self.obsPxList)):
            pygame.draw.rect(display, self.colObs, self.obsPxList[i])

    def calc_valid(self, xy):
        for i in range(len(self.obsPxList)):
            if self.obsPxList[i].collidepoint(xy):
                return False

        return True

    def find_path(self, placed_towers):
        obstacle_list = []
        for i in range(len(self.obsList)):
            for j in range(self.obsList[i][2]):
                for k in range(self.obsList[i][3]):
                    if [self.obsList[i][0] + j, self.obsList[i][1] + k] not in obstacle_list:
                        obstacle_list.append([self.obsList[i][0] + j, self.obsList[i][1] + k])

        obstacle_list += placed_towers

        paths = [pathFinder.find_a_path(self.spawnList[i], self.exitList[i], obstacle_list)
                 for i in range(len(self.spawnList))]

        if -1 in paths:
            return -1

        return paths
