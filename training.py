from HuyAI import HuyAI
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
import os

os.environ["SC2PATH"] = 'E:/StarCraft II/'

for _ in range(10):
    run_game(maps.get("AbyssalReefLE"), [
        Bot(Race.Protoss, HuyAI()),
        Computer(Race.Terran, Difficulty.Hard)
    ], realtime=False)
