from HuyAI import HuyAI
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
import os
import msvcrt
import time

os.environ["SC2PATH"] = 'E:/StarCraft II/'

while True:
    os.system('cls')
    run_game(maps.get("AbyssalReefLE"), [
        Bot(Race.Protoss, HuyAI()),
        Computer(Race.Terran, Difficulty.Hard)
    ], realtime=False)
    print('Press Enter to quit:...')
    time.sleep(2)
    if msvcrt.kbhit():
            if (msvcrt.getwch()=='\r'):
                break
