import pygame
import math

class Projectile(object):
    def __init__(self, source_tower, xy, vel_xy, damage, range, targeting, special, sprite, exp, angle, can_hit):
        self.angle = angle
        self.posXYPx = xy
        self.vel = vel_xy
        self.proj_can_hit = can_hit
        self.totalVel = math.sqrt(vel_xy[0] ** 2 + vel_xy[1] ** 2)
        self.damage = damage
        self.distance = [0, range]
        self.targeting = targeting
        self.special = special
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(sprite, 20)
        self.size = sprite.get_size()
        self.rectPos = [self.posXYPx[0] - self.size[0] / 2, self.posXYPx[1] - self.size[1]]
        self.exp = exp + "-hit"
        self.can_hit = can_hit
        self.source_tower = source_tower
        if self.targeting[0] == 'pierce':
            self.hitlist = []

    def update(self, time, display, enemies):
        collided = []
        num_intervals = int(self.totalVel * time / 8) + 1
        time /= num_intervals
        for i in range(num_intervals):
            self.posXYPx[0] += self.vel[0] * time
            self.posXYPx[1] += self.vel[1] * time
            self.rectPos = [self.posXYPx[0] - self.size[0] / 2, self.posXYPx[1] - self.size[1] / 2]
            self.distance[0] += math.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2) * time
            for j in range(len(enemies)):
                diff = [int(self.rectPos[0] - enemies[j].posPx[0]), int(self.rectPos[1] - enemies[j].posPx[1])]
                if ((self.can_hit == "BOTH" or self.can_hit == enemies[j].movetype) and self.mask.overlap(enemies[j].mask, diff) is not None) or self.targeting[0] == 'pulse':
                    display.blit(self.sprite,
                                 (int(self.posXYPx[0] - self.size[0] / 2), int(self.posXYPx[1] - self.size[1] / 2)))
                    if self.targeting[0] == 'splash' or self.targeting[0] == 'pulse':
                        for k in range(len(enemies)):
                            aoe = self.targeting[1] * 50
                            dist = math.sqrt((self.posXYPx[0] - enemies[k].posPx[0]) ** 2 +
                                             (self.posXYPx[1] - enemies[k].posPx[1]) ** 2)
                            if dist <= aoe + int(enemies[k].stats['radius']) * 0.7 and (self.can_hit == "BOTH" or self.can_hit == enemies[k].movetype):
                                collided.append(enemies[k])
                        return collided
                    elif self.targeting[0] == 'pierce':
                        if enemies[j] not in self.hitlist and len(self.hitlist) <= self.targeting[1]:
                            collided.append(enemies[j])
                            self.hitlist.append(enemies[j])
                            return collided
                    else:
                        collided.append(enemies[j])
                        return collided

        display.blit(self.sprite, (int(self.posXYPx[0] - self.size[0] / 2), int(self.posXYPx[1] - self.size[1] / 2)))

        return collided
