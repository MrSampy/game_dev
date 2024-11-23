from functions import components
from functions import waveParse
from functions import enemyParse
from functions import waveGenerator
from classes import spawner
from classes import tower
from classes import map
from classes import explosion
from classes import enemy
import os.path
import pygame
from pygame import K_SPACE
import random
import time
import sys


def load_pics(folder, name):
    location = folder + name + ".png"
    return pygame.image.load(location).convert_alpha()


def display_wave_info(waveInfo, enemyInfo, curWave):
    waveIndex = curWave + 1
    if waveIndex >= len(waveInfo):
        return
    currWave = waveInfo[waveIndex]
    enemyName = currWave[0][0]
    currEnemyInfo = enemyInfo[enemyName]
    stat_col = (0, 0, 100)
    ver_dist = 28

    components.create_text(screen, (disL - 150, 360), enemyName, True,
                           levelTowerTitleFont, (0, 50, 175))
    components.create_text(screen, (disL - 150, 385), "Enemy count during next wave {count}".format(count = currWave[0][1]), True,
                           levelTowerDescriptionFont, (50, 50, 50))

    components.create_text(screen, (disL - 280, 410), '  Health:', False, levelTowerFont, (0, 0, 0))
    components.create_text(screen, (disL - 208, 410), str(currEnemyInfo['health']), False, levelTowerFont, stat_col)

    components.create_text(screen, (disL - 280, 410 + ver_dist), '  Damage:', False, levelTowerFont, (0, 0, 0))
    components.create_text(screen, (disL - 200, 410 + ver_dist), str(currEnemyInfo['dmg']), False, levelTowerFont,
                           stat_col)

    components.create_text(screen, (disL - 280, 410 + ver_dist * 2), '  Speed:', False, levelTowerFont, (0, 0, 0))
    components.create_text(screen, (disL - 212, 410 + ver_dist * 2), str(currEnemyInfo['speed']), False, levelTowerFont,
                           stat_col)

def display_stats(sel_tower):
    global msgTimer, msgText, money, mousePressed, income
    if not sel_tower.placed:
        if sel_tower.cost > money:
            components.create_text(screen, (disL - 100, 410), "$" + str(sel_tower.cost),
                                   True, levelTowerFont2, (200, 25, 25))
        else:
            components.create_text(screen, (disL - 100, 410), "$" + str(sel_tower.cost),
                                   True, levelTowerFont2, (0, 0, 0))



    components.create_text(screen, (disL - 150, 360), sel_tower.name, True,
                           levelTowerTitleFont, (0, 50, 175))
    components.create_text(screen, (disL - 150, 385), str(round(sel_tower.total_damage_dealt)), True,
                           levelTowerDescriptionFont, (50, 50, 50))

    ver_dist = 28
    if (not butUpgrade.collidepoint(mousePos[0], mousePos[1])) or sel_tower.curLevel == sel_tower.maxLevel:
        stat_col = (0, 0, 100)
        if sel_tower.type == 'turret':
            components.create_text(screen, (disL - 280, 410), '  Dmg:', False, levelTowerFont, (0, 0, 0))
            components.create_text(screen, (disL - 220, 410), str(sel_tower.damage), False, levelTowerFont, stat_col)
            components.create_text(screen, (disL - 280, 410 + ver_dist), '  Rate:', False, levelTowerFont, (0, 0, 0))
            components.create_text(screen, (disL - 220, 410 + ver_dist), str(round(sel_tower.rate, 2)), False, levelTowerFont, stat_col)
            components.create_text(screen, (disL - 280, 410 + ver_dist * 2), 'Range:', False, levelTowerFont, (0, 0, 0))
            components.create_text(screen, (disL - 220, 410 + ver_dist * 2), str(round(sel_tower.range, 2)), False, levelTowerFont, stat_col)
            if sel_tower.projSpd > 0:
                components.create_text(screen, (disL - 280, 410 + ver_dist * 3), ' P.Spd:', False, levelTowerFont, (0, 0, 0))
                components.create_text(screen, (disL - 220, 410 + ver_dist * 3), str(round(sel_tower.projSpd, 2)), False, levelTowerFont, stat_col)
        if sel_tower.targeting != 'projectile' and sel_tower.targeting != 'none' and sel_tower.targeting != 'pulse':
            components.create_text(screen, (disL - 265 - len(sel_tower.targeting) * 3, 410 + ver_dist * 4), sel_tower.targeting + ":", False, levelTowerFont, (0, 0, 0))
            components.create_text(screen, (disL - 230 + len(sel_tower.targeting) * 2, 410 + ver_dist * 4), sel_tower.targetingVal, False, levelTowerFont, stat_col)
        if sel_tower.special != 'none':
            components.create_text(screen, (disL - 265 - len(sel_tower.special) * 3, 410 + ver_dist * 5), sel_tower.special + ":", False, levelTowerFont, (0, 0, 0))
            components.create_text(screen, (disL - 230 + len(sel_tower.special) * 2, 410 + ver_dist * 5), sel_tower.specialVal, False, levelTowerFont, stat_col)
    
    elif sel_tower.curLevel < sel_tower.maxLevel:
        stat_col = (0, 0, 100)
        stat_up_col = (0, 125, 50)
        if sel_tower.type == 'turret':
            components.create_text(screen, (disL - 280, 410), '  Dmg:', False, levelTowerFont, (0, 0, 0))
            components.create_text(screen, (disL - 220, 410), str(sel_tower.damage), False, levelTowerFont,
                                   stat_col)
            components.create_text(screen, (disL - 280, 410 + ver_dist), '  Rate:', False, levelTowerFont, (0, 0, 0))
            if sel_tower.rate < sel_tower.preview_rate:
                components.create_text(screen, (disL - 220, 410 + ver_dist), str(round(sel_tower.preview_rate, 2)), False, levelTowerFont, stat_up_col)
            else:
                components.create_text(screen, (disL - 220, 410 + ver_dist), str(round(sel_tower.preview_rate, 2)), False, levelTowerFont, stat_col)
            components.create_text(screen, (disL - 280, 410 + ver_dist * 2), 'Range:', False, levelTowerFont, (0, 0, 0))
            components.create_text(screen, (disL - 220, 410 + ver_dist * 2), str(round(sel_tower.range, 2)), False, levelTowerFont, stat_col)
            if sel_tower.projSpd > 0:
                components.create_text(screen, (disL - 280, 410 + ver_dist * 3), ' P.Spd:', False, levelTowerFont, (0, 0, 0))
                if sel_tower.projSpd < sel_tower.preview_projSpd:
                    components.create_text(screen, (disL - 220, 410 + ver_dist * 3), str(round(sel_tower.preview_projSpd, 2)), False, levelTowerFont, stat_up_col)
                else:
                    components.create_text(screen, (disL - 220, 410 + ver_dist * 3), str(round(sel_tower.preview_projSpd, 2)), False, levelTowerFont, stat_col)
        if sel_tower.targeting != 'projectile' and sel_tower.targeting != 'none' and sel_tower.targeting != 'pulse':
            components.create_text(screen, (disL - 265 - len(sel_tower.targeting) * 3, 410 + ver_dist * 4), sel_tower.targeting + ":", False, levelTowerFont, (0, 0, 0))
            if sel_tower.targetingVal < sel_tower.preview_targetingVal:
                components.create_text(screen, (disL - 230 + len(sel_tower.targeting) * 2, 410 + ver_dist * 4), sel_tower.preview_targetingVal, False, levelTowerFont, stat_up_col)
            else:
                components.create_text(screen, (disL - 230 + len(sel_tower.targeting) * 2, 410 + ver_dist * 4), sel_tower.preview_targetingVal, False, levelTowerFont, stat_col)
        if sel_tower.special != 'none':
            components.create_text(screen, (disL - 265 - len(sel_tower.special) * 3, 410 + ver_dist * 5), sel_tower.special + ":", False, levelTowerFont, (0, 0, 0))
            if sel_tower.specialVal < sel_tower.preview_specialVal:
                components.create_text(screen, (disL - 230 + len(sel_tower.special) * 2, 410 + ver_dist * 5), sel_tower.preview_specialVal, False, levelTowerFont, stat_up_col)
            else:
                components.create_text(screen, (disL - 230 + len(sel_tower.special) * 2, 410 + ver_dist * 5), sel_tower.preview_specialVal, False, levelTowerFont, stat_col)



pygame.mixer.pre_init(22050, -16, 8, 512)
pygame.init()
pygame.font.init()
pygame.mixer.init()
time.sleep(0.5)

clock = pygame.time.Clock()
fps = 60
disL = 1300
disH = 750
screen = pygame.display.set_mode((disL, disH))
pygame.display.set_caption("Tower Defense")

intro = True
isInfoOnScreen = False

msLevelSelectFont = pygame.font.SysFont('Trebuchet MS', 32, False)
msMenuButFont = pygame.font.SysFont('Trebuchet MS', 45, True)
msHeaderFont = pygame.font.SysFont('Trebuchet MS', 40, True)
msHeaderFont.set_underline(True)
creditHeaderFont = pygame.font.SysFont('Trebuchet MS', 24, True)
creditBodyFont = pygame.font.SysFont('Trebuchet MS', 18, False)

levelInfoFont = pygame.font.SysFont('Trebuchet MS', 28, False)
levelSmallInfoFont = pygame.font.SysFont('Trebuchet MS',18, False)
levelTowerTitleFont = pygame.font.SysFont('Trebuchet MS', 24, True)
levelTowerTitleFont.set_underline(True)
levelTowerFont = pygame.font.SysFont('Trebuchet MS', 18, False)
levelTowerFont2 = pygame.font.SysFont('Trebuchet MS', 20, True)
levelTowerDescriptionFont = pygame.font.SysFont('Trebuchet MS', 15, False)
levelNextWaveFont = pygame.font.SysFont('Trebuchet MS', 38, True)
levelFastFont = pygame.font.SysFont('Trebuchet MS', 14, False)

mapList = ["1", "2"]
selectedMap = "none"

colBackground = [200, 200, 255]
colPurchaseMenu = [120, 220, 240]

levelBut = []
levelButCol = []

mapInfo = []
for i in range(len(mapList)):
    mapInfo.append(map.Map(mapList[i]))
    levelButCol.append([mapInfo[i].colBackground, mapInfo[i].colObs])
    if i % 3 == 0:
        levelBut.append(pygame.Rect(420, 360 + (i // 3) * 100, 80, 80))
    elif i % 3 == 1:
        levelBut.append(pygame.Rect(510, 360 + (i // 3) * 100, 80, 80))
    else:
        levelBut.append(pygame.Rect(600, 360 + (i // 3) * 100, 80, 80))

menuButText = ["PLAY"]
menuButCol = [[100, 240, 100], [240, 230, 120], [240, 230, 120]]
menuBut = [pygame.Rect(90, 310 + i * 115, 250, 100) for i in range(len(menuButText))]
butPressed = 'none'

circleX = [0, 425, 850, 1275]
shapesX = [-425, 0, 425, 850]
picSpawnArrow = load_pics("images/UI/", "arrow")
picExitArrow = load_pics("images/UI/", "arrow2")
picTowerLevel = [load_pics("images/UI/", "level" + str(i + 1)) for i in range(1)]

moneyPic = load_pics("images/UI/", "symbol_money")
lifePic = load_pics("images/UI/", "symbol_life")

towerNames = ['Basic Turret']

towerList = []
butListTowers = []

for i in range(len(towerNames)):
    towerList.append(tower.Turret(towerNames[i]))
    towerList[i].rotate(90)

for i in range(6):
    if i % 3 == 0:
        butListTowers.append(pygame.Rect(disL - 270, 155 + (i // 3) * 80, 70, 70))
    elif i % 3 == 1:
        butListTowers.append(pygame.Rect(disL - 185, 155 + (i // 3) * 80, 70, 70))
    elif i % 3 == 2:
        butListTowers.append(pygame.Rect(disL - 100, 155 + (i // 3) * 80, 70, 70))

explosionImgList = {}
for i in range(len(towerList)):
    nextImgName = towerList[i].stats['sprite_proj'][0] + "-hit"
    explosionImgList[nextImgName] = []
    curImg = 0
    while True:
        explosionImgList[nextImgName].append(load_pics("images/hit_effects/", nextImgName + str(curImg)))
        if os.path.isfile("images/hit_effects/" + nextImgName + str(curImg + 1) + ".png"):
            curImg += 1
        else:
            break


butUpgrade = pygame.Rect(disL - 115, 430, 90, 55)

butSell = pygame.Rect(disL - 115, 455, 90, 55)
butNextWave = pygame.Rect(disL - 290, disH - 65, 280, 58)
butStopGame = pygame.Rect(disL - 290, 590, 280, 58)
butShowWaveInfo = pygame.Rect(disL - 290, 520, 280, 58)
colNextWaveBut = [[175, 175, 175], [15, 215, 110], [3, 132, 252], [192, 207, 126]]

butOverlay = pygame.Rect(disL - 220, disH - 87, 140, 18)
colOverlayBut = [240, 150, 50]

butUpgradeTower = [pygame.Rect(disL - 140, 400 + i * 30, 20, 20) for i in range(6)]
del(butUpgradeTower[3])


while True:
    outro = -1
    while intro:
        dt = clock.tick(fps) / 1000
        if dt > 0.05:
            dt = 0.05
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(colBackground)
        for i in range(len(menuButText)):
            pygame.draw.rect(screen, menuButCol[i], menuBut[i])
            components.create_text(screen, (int(menuBut[i][0] + menuBut[i][2] / 2),
                                            int(menuBut[i][1] + menuBut[i][3] / 2)),
                                   menuButText[i], True, msMenuButFont, (0, 0, 0))
        mousePos = pygame.mouse.get_pos()
        for i in range(len(menuBut)):
            if menuBut[i].collidepoint(mousePos[0], mousePos[1]):
                pygame.draw.rect(screen, (0, 0, 0), menuBut[i], 3)
                if pygame.mouse.get_pressed()[0] == 1 and butPressed != menuButText[i]:
                    butPressed = menuButText[i]
            if butPressed == menuButText[i]:
                pygame.draw.rect(screen, (150, 25, 25), menuBut[i], 3)
            else:
                pygame.draw.rect(screen, (0, 0, 0), menuBut[i], 1)

        if butPressed == "PLAY":
            for i in range(len(levelBut)):
                if levelBut[i].collidepoint(mousePos[0], mousePos[1]):
                    pygame.draw.rect(screen, (0, 0, 0), levelBut[i], 3)
                    if pygame.mouse.get_pressed()[0] == 1 and outro < 0:
                        selectedMap = mapInfo[i]
                        outro = 45

            for i in range(len(levelBut)):
                pygame.draw.rect(screen, levelButCol[i][0], levelBut[i])
                pygame.draw.rect(screen, (0, 0, 0), levelBut[i], 1)
                components.create_text(screen,
                                       (levelBut[i][0] + levelBut[i][2] // 2, levelBut[i][1] + levelBut[i][3] // 2),
                                       i + 1, True, msLevelSelectFont, (15, 15, 15))

            components.create_text(screen, (int(levelBut[1][0] + levelBut[1][2] / 2), 315),
                                   "Choose a level", True, msHeaderFont, (0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, disL, disH), 3)

        if outro > 0:
            outro -= 1
        elif outro == 0:
            intro = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()
        
    curWave = -1
    money = 600
    energy = [4, 4]
    income = 100
    life = 100
    currentlyInWave = False
    deathTimer = -10000

    curPurchasePage = 0

    cheatVal = 0
    cheatList = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN,
                 pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_b]

    mousePressed = pygame.mouse.get_pressed()
    selectedTower = 'none'
    selectedXY = [0, 0]
    selectedPos = [0, 0]

    viewedTower = -1

    msgTimer = -1
    msgText = ""

    wallConnect = []
    placedTowers = []
    placedTowersLoc = []


    waveInfo = waveParse.parse_wave_info("waveData")
    masterWaveTimer = 0

    curSpawnPoint = 0
    spawnerList = []

    enemyInfo = enemyParse.get_data('enemyData')
    enemyList = []

    projList = []

    projExplosionList = []

    introScreen = 45

    updatePath = False
    path = selectedMap.find_path(placedTowersLoc)
    pathRect = [pygame.Rect(path[i][1][0] * 50 - 50, path[i][1][1] * 50 - 50, 50, 50) for i in range(len(path))]
    pathRect2 = [pygame.Rect(path[i][-2][0] * 50 - 50, path[i][-2][1] * 50 - 50, 50, 50) for i in range(len(path))]
    arrowPics = []
    for i in path:
        rot = [0, 0]
        if i[0][0] < i[1][0]:
            rot[0] = 0
        elif i[0][1] < i[1][1]:
            rot[0] = 270
        elif i[0][0] > i[1][0]:
            rot[0] = 180
        else:
            rot[0] = 90
        if i[-1][0] > i[-2][0]:
            rot[1] = 0
        elif i[-1][1] > i[-2][1]:
            rot[1] = 270
        elif i[-1][0] < i[-2][0]:
            rot[1] = 180
        else:
            rot[1] = 90

        arrowPics.append([components.rot_center(picSpawnArrow, rot[0]), components.rot_center(picExitArrow, rot[1])])

    fastForward = False
    ffCounter = 1
    toggleUiOverlay = True

    while not intro:
        dt = clock.tick(fps) / 1000
        if dt > 0.04:
            dt = 0.04

        mousePressed = [0, 0, 0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = pygame.mouse.get_pressed()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE and currentlyInWave:
                    fastForward = not fastForward
                else:
                    cheatVal = 0

        mousePos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        hovered = False

        if fastForward:
            fps = 120
            dt *= 3 
            ffCounter = 1/3
        else:
            fps = 60
            dt *= 1
            ffCounter = 1

        if deathTimer >= 0:
            deathTimer -= dt * ffCounter
        msgTimer -= dt * ffCounter
        if msgTimer < 0:
            msgTimer = -1

        if currentlyInWave:
            masterWaveTimer += dt
        else:
            masterWaveTimer = 0

        i = 0
        while i < len(projExplosionList):
            projExplosionList[i].show(screen, dt)
            if projExplosionList[i].stopped:
                del(projExplosionList[i])
            else:
                i += 1

        screen.fill(selectedMap.colBackground)
        components.draw_grid(screen, 0, 0, disL - 300, disH, 50, selectedMap.colGrid, False)
        selectedMap.draw_obstacles(screen)

        for i in range(len(path)):
            lines = [[path[i][a][0] * 50 - 25, path[i][a][1] * 50 - 25] for a in range(len(path[i]))]
            pygame.draw.lines(screen, (50, 50, 50), False, lines, 1)

        for i in range(len(pathRect)):
            if pathRect[i].collidepoint(mousePos[0], mousePos[1]) \
                    or pathRect2[i].collidepoint(mousePos[0], mousePos[1]):
                lines = [[path[i][a][0] * 50 - 26, path[i][a][1] * 50 - 26] for a in range(len(path[i]))]
                pygame.draw.lines(screen, (200, 50, 50), False, lines, 5)

        for i in range(len(arrowPics)):
            screen.blit(arrowPics[i][0], (path[i][1][0] * 50 - 50, path[i][1][1] * 50 - 50))
            screen.blit(arrowPics[i][1], (path[i][-2][0] * 50 - 50, path[i][-2][1] * 50 - 50))

        if curWave >= len(waveInfo):
            intro = True
            break
        if currentlyInWave:
            i = 0
            while i < len(waveInfo[curWave]):
                if waveInfo[curWave][i][2] <= masterWaveTimer:
                    spawnerList.append(spawner.Spawner(waveInfo[curWave][i],
                                                       enemyInfo[waveInfo[curWave][i][0]]))
                    del(waveInfo[curWave][i])
                    i -= 1

                i += 1

            i = 0
            while i < len(spawnerList):
                spawnerList[i].timer += dt
                if spawnerList[i].timer >= spawnerList[i].interval:
                    spawnerList[i].timer -= spawnerList[i].interval
                    enemyList.append(spawnerList[i].spawn_enemy(selectedMap.spawnList[curSpawnPoint], curSpawnPoint, curWave))
                    curSpawnPoint += 1
                    if curSpawnPoint >= len(selectedMap.spawnList):
                        curSpawnPoint = 0
                    if spawnerList[i].amount == 0:
                        del(spawnerList[i])
                        i -= 1

                i += 1

            i = 0
            while i < len(enemyList):
                if enemyList[i].movetype == "GROUND":
                    enemyList[i].move(path[enemyList[i].path_number], dt)
                    if enemyList[i].reachedEnd and enemyList[i].endTimer <= 0:
                        life -= enemyList[i].dmg
                        del (enemyList[i])
                    else:
                        if enemyList[i].movetype == "GROUND":
                            screen.blit(enemyList[i].sprite, (enemyList[i].posPx[0] - 35, enemyList[i].posPx[1] - 35))
                            i += 1
                else:
                    i += 1

        if len(enemyList) == 0 and len(spawnerList) == 0 and len(waveInfo[curWave]) == 0 and currentlyInWave:
            currentlyInWave = False
            money += income

        for i in placedTowers:
            i.draw_tower_base(screen, [i.pos[0] * 50 - 25, i.pos[1] * 50 - 25])
        
        for i in wallConnect:
            pygame.draw.rect(screen, (140, 140, 140), (i[0][0] * 50 - 46, i[0][1] * 50 - 46, 
                    i[1][0] * 50 - i[0][0] * 50 + 42, i[1][1] * 50 - i[0][1] * 50 + 42))
        
        if viewedTower >= 0:
            outlineMask = (pygame.mask.from_surface(placedTowers[viewedTower].spriteBase)).outline()
            ptList = []
            for i in outlineMask:
                ptList.append([i[0] + placedTowers[viewedTower].pos[0] * 50 - 50, i[1] + placedTowers[viewedTower].pos[1] * 50 - 50])
            pygame.draw.lines(screen, (240, 25, 25), False, ptList, 2)

        for i in range(len(placedTowers)):
            placedTowers[i].draw_tower_gun(screen, [placedTowers[i].pos[0] * 50 - 25,
                                                    placedTowers[i].pos[1] * 50 - 25])

        if (mousePos[0] > disL - 300 and mousePressed[0] == 1 or keys[pygame.K_ESCAPE] or mousePressed[2] == 1) \
                    and selectedTower != 'none':    
            mousePressed = [0, 0]
            selectedTower = 'none' 

        if selectedTower != 'none':

            valid = False
            if 10 <= mousePos[0] <= disL - 310 and 10 <= mousePos[1] <= disH - 10 and selectedMap.calc_valid(mousePos)\
                    and components.xy_to_pos(mousePos) not in placedTowersLoc:
                valid = True

            if valid:
                gridLoc = components.xy_to_pos(mousePos)
                selectedTower.pos = [gridLoc[0], gridLoc[1]]
                selectedTower.draw_tower_full(screen, (selectedTower.pos[0] * 50 - 25,
                                                       selectedTower.pos[1] * 50 - 25))
                if selectedTower.type == "turret":
                    selectedTower.draw_range(screen, valid)
                elif selectedTower.type == "booster":
                    selectedTower.draw_boost_range(screen, valid)
                if mousePressed[0] == 1:
                    placedTowersLoc.append(selectedTower.pos)
                    if money < selectedTower.cost:
                        del(placedTowersLoc[-1])
                        msgTimer = 0.5
                        msgText = "Can't afford this tower!"
                    elif energy[0] - selectedTower.energy < 0:
                        del (placedTowersLoc[-1])
                        msgTimer = 0.5
                        msgText = "Insufficient energy!"
                    elif selectedMap.find_path(placedTowersLoc) == -1:
                        del (placedTowersLoc[-1])
                        msgTimer = 0.5
                        msgText = "Tower blocks path!"
                    else:
                        placedTowers.append(tower.Turret(selectedTower.name))
                        if selectedTower.energy < 0:
                            energy[1] -= selectedTower.energy
                            energy[0] -= selectedTower.energy
                        else:
                            energy[0] -= selectedTower.energy
                        if placedTowers[-1].special == 'income':
                            income += int(placedTowers[-1].specialVal)
                        placedTowers[-1].pos = selectedTower.pos
                        placedTowers[-1].placed = True
                        money -= selectedTower.cost
                        updatePath = True

                        adjacentTowerList = []
                        for i in placedTowers:
                            if abs(placedTowers[-1].pos[0] - i.pos[0]) + abs(placedTowers[-1].pos[1] - i.pos[1]) == 1:
                                adjacentTowerList.append(i)
                        
                        for i in adjacentTowerList:
                            if placedTowers[-1].type == "wall" and i.type == "wall":
                                wallConnect.append([placedTowers[-1].pos, i.pos])

                        if placedTowers[-1].type == "turret":
                            placedTowers[-1].calc_boost(adjacentTowerList)

                        elif placedTowers[-1].type == "booster":
                            for i in adjacentTowerList:
                                secAdjTowerList = []
                                for j in placedTowers:
                                    if abs(i.pos[0] - j.pos[0]) + abs(i.pos[1] - j.pos[1]) == 1:
                                        secAdjTowerList.append(j)

                                i.calc_boost(secAdjTowerList)

            elif not valid:
                selectedTower.draw_tower_full(screen, [mousePos[0], mousePos[1]])
                if selectedTower.type == "turret":
                    selectedTower.draw_range(screen, valid, xy=[mousePos[0], mousePos[1]])
                if mousePressed[0] == 1:
                    print("")

        if currentlyInWave:
            i = 0
            while i < len(enemyList):
                if enemyList[i].movetype == "AIR":
                    enemyList[i].move(path[enemyList[i].path_number], dt)
                    if enemyList[i].reachedEnd and enemyList[i].endTimer <= 0:
                        life -= enemyList[i].dmg
                        del (enemyList[i])
                    else:
                        screen.blit(enemyList[i].rot_sprite, (enemyList[i].posPx[0] - enemyList[i].rot_sprite.get_rect()[2] // 2, 
                                                                enemyList[i].posPx[1] - enemyList[i].rot_sprite.get_rect()[3] // 2))
                        i += 1
                        
                else:
                    i += 1

        if currentlyInWave:
            for i in range(len(placedTowers)):
                if placedTowers[i].type == "turret": 
                    placedTowers[i].calc_rotation(enemyList, dt)
                    if placedTowers[i].canFire:
                        projList.append(placedTowers[i].fire_projectile())
        else:
            for i in range(len(placedTowers)):
                if placedTowers[i].type == "turret":
                    placedTowers[i].rotate(90)

        i = 0
        while i < len(projList):
            enemyHit = projList[i].update(dt, screen, enemyList)
            if enemyHit != []:
                j = 0
                for j in range(len(enemyHit)):
                    damage_dealt = enemyHit[j].inflict_damage(projList[i].damage, projList[i].special)
                    projList[i].source_tower.total_damage_dealt += damage_dealt
                    if enemyHit[j].curHP <= 0:
                        money += enemyHit[j].bounty
                        if enemyHit[j].stats["death_spawn_enemy"] != "none":
                            spawnedEnemy = enemyInfo[enemyHit[j].stats["death_spawn_enemy"]]
                            for k in range(int(enemyHit[j].stats["death_spawn_val"])):
                                enemyList.append(enemy.Enemy(spawnedEnemy, enemyHit[j].tileLoc, enemyHit[j].path_number, curWave))
                                enemyList[-1].posPx[0] += random.randint(-4, 4)
                                enemyList[-1].posPx[1] += random.randint(-4, 4)
                                enemyList[-1].status.append(['slow', 1.0, k*0.1 + random.uniform(0,0.05)])
                        del(enemyList[enemyList.index(enemyHit[j])])

                if projList[i].targeting[0] == 'splash' or projList[i].targeting[0] == 'pulse':
                    projExplosionList.append(explosion.Explosion(projList[i].posXYPx,
                                                                 explosionImgList[projList[i].exp], float(projList[i].targeting[1]) * 100, projList[i].angle))
                    del (projList[i])
                    i -= 1

                elif projList[i].targeting[0] == 'pierce' and len(projList[i].hitlist) <= projList[i].targeting[1]:
                    pass
                else:
                    projExplosionList.append(explosion.Explosion(projList[i].posXYPx,
                                                                 explosionImgList[projList[i].exp], -1, projList[i].angle))
                    del (projList[i])
                    i -= 1

            elif projList[i].distance[0] > projList[i].distance[1]:
                del(projList[i])
                i -= 1

            i += 1

        i = 0
        while i < len(projExplosionList):
            projExplosionList[i].show(screen, dt)
            if projExplosionList[i].stopped:
                del projExplosionList[i]
            else:
                i += 1

        if viewedTower >= 0:
            if placedTowers[viewedTower].type == "turret":
                placedTowers[viewedTower].draw_range(screen, True)
            elif placedTowers[viewedTower].type == "booster":
                placedTowers[viewedTower].draw_boost_range(screen, True)


        for i in placedTowers:
            if i.maxLevel > 1:
                if i.curLevel < i.maxLevel:
                    screen.blit(picTowerLevel[i.curLevel - 1], [i.pos[0] * 50 - 35, i.pos[1] * 50 - 14])
                else:
                    screen.blit(picTowerLevel[4], [i.pos[0] * 50 - 35, i.pos[1] * 50 - 14])

        pygame.draw.rect(screen, colPurchaseMenu, (disL - 300, 0, 300, disH), 0)

        pygame.draw.rect(screen, selectedMap.colObs, (0, 0, disL, disH), 4)
        pygame.draw.line(screen, selectedMap.colObs, (disL - 300, 0), (disL - 300, disH), 3)

        pygame.draw.line(screen, (70, 70, 70), (disL - 300, butListTowers[0][1] - 18), (disL, butListTowers[0][1] - 18))
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, butListTowers[0][1] + 185),
                         (disL, butListTowers[0][1] + 185))
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, disH - 90),
                         (disL, disH - 90))


        colNextWaveText = [0, 0, 0]
        if currentlyInWave:
            pygame.draw.rect(screen, colNextWaveBut[0], butStopGame)
            pygame.draw.rect(screen, (0, 0, 0), butStopGame, 1)
            pygame.draw.rect(screen, colNextWaveBut[0], butShowWaveInfo)
            pygame.draw.rect(screen, (0, 0, 0), butShowWaveInfo, 1)
            pygame.draw.rect(screen, colNextWaveBut[0], butNextWave)
            pygame.draw.rect(screen, (0, 0, 0), butNextWave, 1)


            colNextWaveText = [55, 55, 55]
            components.create_text(screen, (butStopGame[0] + butStopGame[2] // 2, butStopGame[1] + butStopGame[3] // 2 - 5),
                        "STOP GAME", True, levelNextWaveFont, colNextWaveText)
            components.create_text(screen, (butShowWaveInfo[0] + butShowWaveInfo[2] // 2, butShowWaveInfo[1] + butShowWaveInfo[3] // 2 - 5),
                        "WAVE INFO", True, levelNextWaveFont, colNextWaveText)
            components.create_text(screen, (butNextWave[0] + butNextWave[2] // 2, butNextWave[1] + butNextWave[3] // 2 - 5),
                        "NEXT WAVE", True, levelNextWaveFont, colNextWaveText)
            components.create_text(screen, (disL - 150, disH - 18), 'spacebar to fast forward',
                                   True, levelFastFont, (0, 0, 0))
        elif not currentlyInWave:
            pygame.draw.rect(screen, colNextWaveBut[3], butStopGame)
            pygame.draw.rect(screen, (0, 0, 0), butStopGame, 1)
            pygame.draw.rect(screen, colNextWaveBut[2], butShowWaveInfo)
            pygame.draw.rect(screen, (0, 0, 0), butShowWaveInfo, 1)
            pygame.draw.rect(screen, colNextWaveBut[1], butNextWave)
            pygame.draw.rect(screen, (0, 0, 0), butNextWave, 1)

            components.create_text(screen, (butNextWave[0] + butNextWave[2] // 2, butNextWave[1] + butNextWave[3] // 2),
                        "NEXT WAVE", True, levelNextWaveFont, colNextWaveText)
            components.create_text(screen, (butShowWaveInfo[0] + butShowWaveInfo[2] // 2, butShowWaveInfo[1] + butShowWaveInfo[3] // 2 - 5),
                        "WAVE INFO", True, levelNextWaveFont, colNextWaveText)
            components.create_text(screen, (butStopGame[0] + butStopGame[2] // 2, butStopGame[1] + butStopGame[3] // 2),
                                   "STOP GAME", True, levelNextWaveFont, colNextWaveText)
            if butShowWaveInfo.collidepoint(mousePos[0], mousePos[1]):
                pygame.draw.rect(screen, (0, 0, 0), butShowWaveInfo, 3)
                if not hovered and selectedTower == 'none' and viewedTower <= 0:
                    display_wave_info(waveInfo, enemyInfo, curWave)

            if butStopGame.collidepoint(mousePos[0], mousePos[1]):
                pygame.draw.rect(screen, (0, 0, 0), butStopGame, 3)
                if mousePressed[0] == 1:
                    intro = True
                    break
            if butNextWave.collidepoint(mousePos[0], mousePos[1]) or keys[pygame.K_SPACE]:
                pygame.draw.rect(screen, (0, 0, 0), butNextWave, 3)
                if mousePressed[0] == 1 or keys[pygame.K_SPACE]:
                    curWave += 1
                    currentlyInWave = True
                    curSpawnPoint = random.randint(0, len(selectedMap.spawnList) - 1)
                    selectedTower = 'none'
                    for i in placedTowers:
                        i.reload = 0.05
                        i.sellPrice = i.totalCost // 2
                    if curWave >= 40:
                        waveInfo.append(waveGenerator.generate(curWave + 1))

        mul6 = curPurchasePage * 6
        for i in range(6):
            if i + mul6 < len(towerList):
                pygame.draw.rect(screen, (230, 230, 250), (butListTowers[i]))
                if butListTowers[i].collidepoint(mousePos[0], mousePos[1]) and selectedTower == 'none' \
                        and not currentlyInWave:
                    hovered = True
                    display_stats(towerList[i + mul6])
                    if towerList[i + mul6].cost <= money and energy[0] - towerList[i + mul6].energy >= 0:
                        pygame.draw.rect(screen, (255, 255, 255), (butListTowers[i]), 2)
                        if mousePressed[0] == 1:
                            selectedTower = towerList[i + mul6]
                    else:
                        if mousePressed[0] == 1:
                            selectedTower = 'none'
                            if towerList[i + mul6].cost > money:
                                msgText = "Can't afford this tower!"
                                msgTimer = 0.5

                elif butListTowers[i].collidepoint(mousePos[0], mousePos[1]) \
                        and mousePressed[0] == 1 and currentlyInWave:
                    msgText = "Cannot buy towers during a wave"
                    msgTimer = 0.75

        for i in range(mul6, mul6 + 6, 1):
            if i < len(towerList):
                towerList[i].draw_tower_full(screen, [butListTowers[i - mul6][0] + butListTowers[i - mul6][2] // 2,
                                                      butListTowers[i - mul6][1] + butListTowers[i - mul6][3] // 2])

        if selectedTower != 'none':
            display_stats(selectedTower)
            viewedTower = -1
        else:
            if mousePressed[0] == 1:
                if components.xy_to_pos(mousePos) in placedTowersLoc and mousePos[0] < 1000:
                    viewedTower = placedTowersLoc.index(components.xy_to_pos(mousePos))
                elif mousePos[0] < 1000:
                    viewedTower = -1
            # draw range of da tower
            if viewedTower >= 0:
                if not hovered:
                    # stats
                    display_stats(placedTowers[viewedTower])

                    # sell button
                    pygame.draw.rect(screen, (225, 100, 100), butSell)
                    # text of sell button
                    components.create_text(screen, (butSell[0] + butSell[2] // 2, butSell[1] + butSell[3] // 2 - 13),
                                           'SELL FOR', True, levelTowerFont, (0, 0, 0))
                    components.create_text(screen, (butSell[0] + butSell[2] // 2, butSell[1] + butSell[3] // 2 + 11),
                                           "$" + str(int(placedTowers[viewedTower].sellPrice)), True, levelTowerFont2,
                                           (0, 0, 0))

                    # interact with sell button
                    if butSell.collidepoint(mousePos[0], mousePos[1]) and not currentlyInWave:
                        pygame.draw.rect(screen, (0, 0, 0), butSell, 3)
                        if mousePressed[0] == 1:  # on click, sell the tower
                            # energy check
                            if energy[0] < 0 - placedTowers[viewedTower].energy:
                                msgText = 'Energy too low!'
                                msgTimer = 0.75
                            else:  # passes energy check
                                if placedTowers[viewedTower].energy < 0:
                                    energy[1] += placedTowers[viewedTower].energy
                                    energy[0] += placedTowers[viewedTower].energy
                                else:  # remove da tower
                                    energy[0] += placedTowers[viewedTower].energy
                                # update monies
                                money += int(placedTowers[viewedTower].sellPrice)
                                if placedTowers[viewedTower].special == 'income':  # update income on sell
                                    income -= placedTowers[viewedTower].specialVal

                                # check boosts
                                placedTowers[viewedTower].specialVal = 0
                                adjacentTowerList = []
                                for i in placedTowers:
                                    # calculate distance to tower and check if it equals one
                                    if abs(placedTowers[viewedTower].pos[0] - i.pos[0]) + abs(
                                            placedTowers[viewedTower].pos[1] - i.pos[1]) == 1:
                                        adjacentTowerList.append(i)
                                # update wall connections
                                i = 0
                                while i < len(adjacentTowerList):
                                    if placedTowers[viewedTower].type == "wall" and adjacentTowerList[i].type == "wall":
                                        if [placedTowers[viewedTower].pos, adjacentTowerList[i].pos] in wallConnect:
                                            del (wallConnect[wallConnect.index(
                                                [placedTowers[viewedTower].pos, adjacentTowerList[i].pos])])
                                            i -= 1
                                        if [adjacentTowerList[i].pos, placedTowers[viewedTower].pos] in wallConnect:
                                            del (wallConnect[wallConnect.index(
                                                [adjacentTowerList[i].pos, placedTowers[viewedTower].pos])])
                                            i -= 1
                                    i += 1
                                # update each adjacent tower if booster
                                if placedTowers[viewedTower].type == "booster":
                                    for i in adjacentTowerList:
                                        secAdjTowerList = []
                                        for j in placedTowers:
                                            # calculate distance to tower and check if it equals one
                                            if abs(i.pos[0] - j.pos[0]) + abs(i.pos[1] - j.pos[1]) == 1:
                                                secAdjTowerList.append(j)

                                        i.calc_boost(secAdjTowerList)

                                del placedTowers[viewedTower]
                                del placedTowersLoc[viewedTower]
                                updatePath = True  # reset path
                                viewedTower = -1  # reset viewed tower
                    elif mousePressed[0] == 1 and butSell.collidepoint(mousePos[0], mousePos[1]) and currentlyInWave:
                        msgText = 'Cannot sell towers during a wave'
                        msgTimer = 0.75
                    else:
                        pygame.draw.rect(screen, (0, 0, 0), butSell, 1)

        if money > 50000:
            money = 50000

        screen.blit(lifePic, (disL - 280, 20))
        components.create_text(screen, (disL - 230, 40), str(life), False, levelInfoFont, (0, 0, 0))
        components.create_text(screen, (disL - 140, 40), "wave  " + str(curWave + 1), False, levelInfoFont, (0, 0, 0))
        screen.blit(moneyPic, (disL - 280, 70))
        components.create_text(screen, (disL - 230, 90), str(int(money)), False, levelInfoFont, (0, 0, 0))
        components.create_text(screen, (disL - 225, 112), "+" + str(int(income)), False, levelSmallInfoFont, (0, 0, 0))
        if life <= 0 and deathTimer < -100:
            msgTimer = 2
            msgText = "You died!"
            deathTimer = 2
        if msgTimer >= 0:
            components.create_text(screen, (500, disH - 100), msgText, True, levelInfoFont, (150, 25, 25))
        if updatePath:
            path = selectedMap.find_path(placedTowersLoc)
            updatePath = False
        pygame.display.update()
        if -100 < deathTimer < 0:
            intro = True
            fps = 60
