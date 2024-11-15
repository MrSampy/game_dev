import pygame
import game_dev.TowerDefense.functions as functions
import math


class Explosion(object):
    def __init__(self, xy, pictures, scaling, angle):
        self.picList = pictures.copy()
        self.scale = int(scaling)
        if self.scale != -1:
            for i in range(len(self.picList)):
                self.picList[i] = pygame.transform.scale(self.picList[i], (self.scale, self.scale))
        self.rotPicList = []
        for i in self.picList:
            self.rotPicList.append(functions.components.rot_center(i, math.degrees(angle)))
        self.posXYPx = xy
        self.timer = 0.15
        self.curpic = 0
        self.stopped = False
        self.size = self.rotPicList[0].get_size()

    def show(self, display, dt):
        display.blit(self.rotPicList[self.curpic], (self.posXYPx[0] - self.size[0] // 2, self.posXYPx[1] - self.size[1] // 2))
        self.timer -= dt
        if self.timer <= 0:
            self.timer = 0.15
            if self.curpic < len(self.picList) - 1:
                self.curpic += 1
            else:
                self.stopped = True
