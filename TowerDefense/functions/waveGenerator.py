import random

valueList = {}
with open("data/enemyCost", "r") as f:
    for line in f:
        if len(line.strip()) != 0:
            newLine = line.strip().split()
            cost = float(newLine[-1])
            del(newLine[-1])
            name = ' '.join(map(str, newLine))
            valueList[name] = cost

def generate(wave):
    powerRandom = random.uniform(-3,3)
    powerTotal = (wave * 17) ** 1.04 + powerRandom * 50
    powerRate = 1.5 + wave * 0.6 - powerRandom * 1.0
    numEnemies = random.randint(2, 4)

    if wave % 5 == 0:
        numEnemies += 1
        powerTotal *= 1.25
    
    formation = random.randint(1, 3)
    
    outputWave = [[random.choice(list(valueList))] for i in range(numEnemies)]
    totalTime = 0
    for i in range(numEnemies):
        strength = powerTotal / numEnemies
    
        if formation == 0:
            pass
        if formation == 1:
            num = round(strength/valueList[outputWave[i][0]], 0)
            delay = random.uniform(0, 1) + totalTime
            interval = valueList[outputWave[i][0]] / (powerRate * 2.5/numEnemies)
            totalTime += (interval * (num -1)) + 3
        else:
            num = round(strength/valueList[outputWave[i][0]], 0)
            delay = random.uniform(0, 1)
            interval = valueList[outputWave[i][0]] / (powerRate/numEnemies)
        
        outputWave[i] = [outputWave[i][0], num, delay, interval]

    return outputWave
    
