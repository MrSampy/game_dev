import pygame
import math
import random
import game_dev.TowerDefense.functions as functions

class Enemy(object):
    def __init__(self, attributes, spawnpoint, spawn_num, level):
        self.stats = attributes
        self.sprite = self.stats['sprite']
        self.mask = pygame.mask.from_surface(self.stats['sprite'], 24)
        self.status = []
        self.movetype = self.stats['movement_type']
        self.hp_bonus = level * (0.095 + level * 0.005)

        if level > 50:
            self.hp_bonus += (level - 50) * (0.3)
            level = 50
        self.speed_bonus = 0.006 * level
        self.regen_bonus = level * (0.05)
        if level > 20:
            self.regen_bonus += (level - 20) * (0.07)
        if level > 40:
            self.regen_bonus += (level - 40) * (0.08)
        self.armour_bonus = 0.04 * level
        self.bounty_bonus = 0.02 * level

        self.maxHP = int(int(self.stats['health']) * (1 + self.hp_bonus))
        self.curHP = self.maxHP
        self.speed = float(self.stats['speed']) * (1 + self.speed_bonus)
        self.regen = float(self.stats['regen']) * (1 + self.regen_bonus)
        self.armour = round(int(self.stats['armour']) * (1 + self.armour_bonus), 0)
        self.bounty = round(int(self.stats['bounty']) * (1 + self.bounty_bonus), 0)
        if 'special' in self.stats:
            self.special = self.stats['special']

        self.dmg = int(self.stats['dmg'])

        self.path_number = spawn_num
        self.direction_delay = -1
        self.endTimer = 0.1

        self.movement_dir = [0, 0]
        self.distance = 1000
        self.radius = float(self.stats['radius'])
        self.tileLoc = spawnpoint
        self.posPx = [spawnpoint[0] * 50 - 25 + random.uniform(-4, 4), spawnpoint[1] * 50 - 25 + random.uniform(-4, 4)]
        self.reachedEnd = False
        self.secSpawn = attributes['death_spawn_enemy']
        self.secValue = int(attributes['death_spawn_val'])

    def calc_tile_loc(self, pos):
        prevLoc = self.tileLoc
        self.tileLoc = [pos[0] // 50 + 1, pos[1] // 50 + 1]
        if prevLoc != self.tileLoc:
            self.direction_delay = 0.45

    def move(self, path, time):
        temp_speed = self.speed
        slow_spd = 1.0
        i = 0
        while i < len(self.status):
            if 'slow' in self.status[i]:
                slow_spd *= (1-self.status[i][1])
                
                self.status[i][2] -= time
                if self.status[i][2] <= 0:
                    del self.status[i]
                    i -= 1
                i += 1
        if slow_spd < 0:
            slow_spd = 0

        
        slow_regen_multi = slow_spd
        temp_speed *= slow_spd

        if self.curHP < self.maxHP:
            self.curHP += self.regen * time * slow_regen_multi
        else:
            self.curHP = self.maxHP

        if self.movetype == "GROUND":
            self.calc_tile_loc(self.posPx)
            if self.reachedEnd:
                self.endTimer -= time
            elif self.tileLoc == path[-1]:
                self.reachedEnd = True
                self.endTimer = 0.3
            else:
                self.distance = len(path) - path.index(self.tileLoc)

            self.direction_delay -= time * temp_speed

            if not self.reachedEnd and self.direction_delay <= 0:
                cur_tile = path.index(self.tileLoc)
                self.movement_dir = [self.tileLoc[0] - path[cur_tile + 1][0], self.tileLoc[1] - path[cur_tile + 1][1]]

            self.posPx[0] -= self.movement_dir[0] * time * temp_speed * 50
            self.posPx[1] -= self.movement_dir[1] * time * temp_speed * 50

        else:
            print("enemy movement not defined")

    def inflict_damage(self, damage, specials):
        if specials[0] == 'antiair':
            if self.movetype == "AIR":
                damage *= specials[1]
        elif specials[0] != 'none':
            self.status.append([specials[0], specials[1], specials[2]])
        
        if damage - self.armour >= 1:
            damage_dealt = min(self.curHP, damage - self.armour)
            self.curHP -= damage - self.armour
            return damage_dealt
        elif damage > 0:
            self.curHP -= 0.5
            return 0.5
        return 0

    def draw_bar(self, display, a_pic):
        if self.curHP < self.maxHP:
            hp_perc = self.curHP / self.maxHP
            pygame.draw.rect(display, (0, 0, 0), (self.posPx[0] - 20, self.posPx[1] - int(self.stats['radius']) - 8,
                                                  40, 6), 1)
            pygame.draw.rect(display, (250, 25, 25), (self.posPx[0] - 19,
                                                      self.posPx[1] - int(self.stats['radius']) - 7,
                                                      38 * hp_perc, 4))

        if self.armour > 0:
            display.blit(a_pic, (self.posPx[0] - 6, self.posPx[1] - 34))
