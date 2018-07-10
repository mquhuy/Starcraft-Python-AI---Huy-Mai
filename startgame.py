from HuyAI import HuyAI
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, HuyAI()),
    Computer(Race.Terran, Difficulty.Medium)
], realtime=False)
