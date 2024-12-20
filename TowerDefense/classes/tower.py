import math
import pygame
from pygame import gfxdraw
from game_dev.TowerDefense.functions import towerParse
from game_dev.TowerDefense.functions import components
from game_dev.TowerDefense.classes import projectile


def load_pics(folder, name):
    location = folder + name + ".png"
    return pygame.image.load(location).convert_alpha()


class Turret(object):
    def __init__(self, name):
        self.stats = towerParse.get_stats(name)
        self.name = name
        self.total_damage_dealt = 0
        self.rotation = math.pi / 2
        self.type = self.stats['type'][0]
        self.curLevel = 1
        self.maxLevel = int(self.stats['max_level'][0])
        self.dmgBoost = 0
        self.rateBoost = 0
        self.rangeBoost = 0
        self.projBoost = 0
        self.cost = int(self.stats['cost'][0])
        self.energy = int(self.stats['energy'][0])
        self.upCost = int(self.stats['up_cost'][0])
        self.totalCost = self.cost
        self.sellPrice = self.totalCost
        if self.type == "turret":
            self.can_hit = self.stats['can_hit'][0]

        self.targeting = self.stats['targeting'][0]
        if 'targeting_val' in self.stats:
            self.targetingVal = float(self.stats['targeting_val'][0])
        else:
            self.targetingVal = 0

        self.effRange = float(self.stats['effective_range'][0])
        self.reload = 0.01

        self.damage = 0
        self.rate = 0
        self.range = 0
        self.projSpd = 0

        self.special = self.stats['special'][0]
        self.specialVal = 0
        if self.special != 'none':
            if 'special_val' in self.stats:
                self.specialVal = float(self.stats['special_val'][0])
                if 'special_val2' in self.stats:
                    self.specialVal2 = float(self.stats['special_val2'][0])
                else:
                    self.specialVal2 = 0
        else:
            self.special = 'none'
            self.specialVal = 0
            self.specialVal2 = 0
        self.spriteBase = load_pics("images/towers/", str(self.stats['sprite_base'][0]))
        self.spriteGun = load_pics("images/towers/", str(self.stats['sprite_turret'][0]))
        self.spriteProj = load_pics("images/projectiles/", str(self.stats['sprite_proj'][0]))
        self.rotSpriteGun = self.spriteGun.copy()
        self.canFire = False
        self.update_stats(self.curLevel)
        self.upgrade_preview(self.curLevel)
        self.placed = False
        self.pos = [0, 0]
        tar = []

    def upgrade_preview(self, cur_level):
        if self.maxLevel > 1 and self.curLevel < self.maxLevel:
            self.preview_damage = int(round(float(self.stats['damage'][cur_level]) * (1 + self.dmgBoost), 0))
            self.preview_rate = float(float(self.stats['rate'][cur_level]) * (1 + self.rateBoost))
            self.preview_range = float(float(self.stats['range'][cur_level]) * (1 + self.rangeBoost))
            self.preview_projSpd = float(float(self.stats['proj_spd'][cur_level]) * (1 + self.projBoost))
            if 'targeting_val' in self.stats:
                self.preview_targetingVal = float(self.stats['targeting_val'][cur_level])
            if 'special_val' in self.stats:
                self.preview_specialVal = float(self.stats['special_val'][cur_level])

    def update_stats(self, cur_level):
        if self.curLevel < self.maxLevel:
            self.upCost = int(self.stats['up_cost'][cur_level - 1])
        self.damage = int(round(float(self.stats['damage'][cur_level - 1]) * (1 + self.dmgBoost), 0))
        self.rate = float(float(self.stats['rate'][cur_level - 1]) * (1 + self.rateBoost))
        self.range = float(float(self.stats['range'][cur_level - 1]) * (1 + self.rangeBoost))
        self.projSpd = float(float(self.stats['proj_spd'][cur_level - 1]) * (1 + self.projBoost))
        if 'targeting_val' in self.stats:
            if self.targeting == 'pulse':
                self.targetingVal = self.range
            else:
                self.targetingVal = float(self.stats['targeting_val'][cur_level - 1])
        if 'special_val' in self.stats:
            self.specialVal = float(self.stats['special_val'][cur_level - 1])
        if 'special_val2' in self.stats:
            self.specialVal2 = float(self.stats['special_val2'][cur_level - 1])

    def calc_boost(self, adj_tower_list):
        self.dmgBoost = 0
        self.rateBoost = 0
        self.rangeBoost = 0
        self.projBoost = 0
        if len(adj_tower_list) > 0:
            for i in adj_tower_list:
                if i.special == "damage":
                    self.dmgBoost += i.specialVal
                elif i.special == "rate":
                    self.rateBoost += i.specialVal
                elif i.special == "range":
                    self.rangeBoost += i.specialVal
                    self.projBoost += (i.specialVal / 2)
        
            self.update_stats(self.curLevel)
            self.upgrade_preview(self.curLevel)

    def upgrade(self):
        self.totalCost += self.upCost
        self.sellPrice = self.totalCost // 2
        self.curLevel += 1
        self.update_stats(self.curLevel)
        if self.curLevel < self.maxLevel:
            self.upgrade_preview(self.curLevel)

    def rotate(self, angle):
        self.rotation = math.radians(angle)
        self.rotSpriteGun = components.rot_center(self.spriteGun, angle)

    def calc_rotation(self, enemy_list, dt):
        self.canFire = False
        tar = []
        path_left_cur = 1000

        for i in enemy_list:
            dist_to_enemy = math.sqrt(((self.pos[0] * 50 - 25) - i.posPx[0]) ** 2 +
                                      ((self.pos[1] * 50 - 25) - i.posPx[1]) ** 2)
            if (self.can_hit == "BOTH" or self.can_hit == i.movetype) and \
                        i.distance < path_left_cur and dist_to_enemy <= self.range * 50 + float(i.radius) * 0.7:
                tar = [i.posPx[0], i.posPx[1]]
                path_left_cur = i.distance

        if self.reload > 0:
            self.reload -= dt
        elif tar != []:
            self.canFire = True

        if tar != []:
            diff = [tar[0] - (self.pos[0] * 50 - 25), tar[1] - (self.pos[1] * 50 - 25)]
            self.rotation = math.atan2(-diff[1], diff[0])
        self.rotSpriteGun = components.rot_center(self.spriteGun, math.degrees(self.rotation))

    def fire_projectile(self):
        self.reload += (1 / self.rate) - 0.0166
        tempSpecial = []
        if self.reload <= 0:
            self.canFire = True
        tempTargeting = [self.targeting, self.targetingVal]
        if self.targeting == 'pulse':
            tempTargeting[1] = self.range
        tempSpecial = [self.special, self.specialVal, self.specialVal2]

        self.canFire = False
        xy_vel = [self.projSpd * math.cos(self.rotation) * 50, self.projSpd * -math.sin(self.rotation) * 50]
        temp_spr = components.rot_center(self.spriteProj, math.degrees(self.rotation))
        return projectile.Projectile(self, [self.pos[0] * 50 - 25, self.pos[1] * 50 - 25], xy_vel,
                                    self.damage, self.range * self.effRange * 50, tempTargeting, tempSpecial,
                                    temp_spr, str(self.stats['sprite_proj'][0]), self.rotation, self.can_hit)
    def draw_tower_gun(self, display, xy):
        temp = self.rotSpriteGun.get_rect()
        display.blit(self.rotSpriteGun, (xy[0] - temp[2] // 2, xy[1] - temp[3] // 2))

    def draw_tower_base(self, display, xy):
        temp = self.spriteBase.get_rect()
        display.blit(self.spriteBase, (xy[0] - temp[2] // 2, xy[1] - temp[3] // 2))

    def draw_tower_full(self, display, xy):
        self.draw_tower_base(display, xy)
        self.draw_tower_gun(display, xy)

    def draw_range(self, display, valid, xy=0):
        col_range_valid = [120, 140, 140, 20]
        col_range_valid_outline = [50, 50, 50, 225]
        col_range_invalid = [200, 25, 25, 35]
        col_range_invalid_outline = [125, 0, 0, 150]
        if xy == 0:
            xy = [self.pos[0] * 50 - 25, self.pos[1] * 50 - 25]

        if valid:
            pygame.gfxdraw.aacircle(display, xy[0], xy[1], int(self.range * 50),
                                    col_range_valid_outline)
            pygame.gfxdraw.filled_circle(display, xy[0], xy[1], int(self.range * 50), col_range_valid)
        elif not valid:
            pygame.gfxdraw.aacircle(display, xy[0], xy[1], int(self.range * 50),
                                    col_range_invalid_outline)
            pygame.gfxdraw.filled_circle(display, xy[0], xy[1], int(self.range * 50),
                                         col_range_invalid)
    
    def draw_boost_range(self, display, valid, xy=0):
        xy = [self.pos[0] * 50 - 25, self.pos[1] * 50 - 25]
        pygame.draw.rect(display, (60, 100, 250), (xy[0] -26, xy[1] -76, 52, 52), 1)
        pygame.draw.rect(display, (60, 100, 250), (xy[0] +24, xy[1] -26, 52, 52), 1)
        pygame.draw.rect(display, (60, 100, 250), (xy[0] -26, xy[1] +24, 52, 52), 1)
        pygame.draw.rect(display, (60, 100, 250), (xy[0] -76, xy[1] -26, 52, 52), 1)
