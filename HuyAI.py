import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, CYBERNETICSCORE, STALKER, STARGATE, VOIDRAY
import random
import cv2
import numpy as np

class HuyAI(sc2.BotAI):
    async def on_step(self, iteration):
        self.iteration = iteration
        await self.distribute_workers()
        await self.build_workers()
        await self.build_houses()
        await self.expand()
        await self.build_assimilators()
        await self.offensive_force_buildings()
        await self.build_offensive_force()
        await self.attack()
        await self.intel()

    async def build_workers(self):
        # nexus is the main house
        # Build workers means to build probes
        if (len(self.units(NEXUS))*16 > len(self.units(PROBE))) and len(self.units(PROBE)) < self.MAX_WORKERS:
            for nexus in self.units(NEXUS).ready.noqueue:
                if self.can_afford(PROBE):
                    await self.do(nexus.train(PROBE))

    async def build_houses(self):
        # Build houses means to build Pylons
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near=nexuses.first)

    async def expand(self):
        if self.units(NEXUS).amount < (self.iteration / self.ITERATIONS_PER_MINUTE) and self.can_afford(NEXUS):
            await self.expand_now()

    async def build_assimilators(self):
        for nexus in self.units(NEXUS).ready:
            vaspenes = self.state.vespene_geyser.closer_than(25.0, nexus)
            for vaspene in vaspenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vaspene.position)
                if worker is None:
                    break
                if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                    await self.do(worker.build(ASSIMILATOR, vaspene))

    async def offensive_force_buildings(self):
        if self.units(PYLON).ready.exists:

            pylon = self.units(PYLON).ready.random

            if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE):
                if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                    await self.build(CYBERNETICSCORE, near=pylon)
            elif len(self.units(GATEWAY)) < 1:
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon)

            if self.units(CYBERNETICSCORE).ready.exists:
                if len(self.units(STARGATE)) < (self.iteration/self.ITERATIONS_PER_MINUTE):
                    if self.can_afford(STARGATE) and not self.already_pending(STARGATE):
                        await self.build(STARGATE, near=pylon)

    async def build_offensive_force(self):
        # for gw in self.units(GATEWAY).ready.noqueue:
        #     if not self.units(STALKER).amount > self.units(VOIDRAY).amount*2:
        #         if self.can_afford(STALKER) and self.supply_left > 0:
        #             await self.do(gw.train(STALKER))

        for sg in self.units(STARGATE).ready.noqueue:
            if self.can_afford(VOIDRAY) and self.supply_left > 0:
                await self.do(sg.train(VOIDRAY))

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]

    async def attack(self):
        aggressive_units = {
                            #STALKER: [15, 5],
                            VOIDRAY: [8, 3]
                            }
        for UNIT in aggressive_units:
            for s in self.units(STALKER).idle:
                await self.do(s.attack(self.find_target(self.state)))

    async def intel(self):
        draw_dict = {
             NEXUS: [15, (0, 255, 0)],
             PYLON: [3, (20, 235, 0)],
             PROBE: [1, (55, 200, 0)],
             ASSIMILATOR: [2, (55, 200, 0)],
             GATEWAY: [3, (200, 100, 0)],
             CYBERNETICSCORE: [3, (150, 150, 0)],
             STARGATE: [5, (255, 0, 0)],
             VOIDRAY: [3, (255, 100, 0)],
            }
        print(self.game_info.map_size)
        game_data = np.zeros((self.game_info.map_size[1], self.game_info.map_size[0], 3), np.uint8)
        for unit_type in draw_dict:
            for UNIT in self.units(unit_type):
                unit_pos = UNIT.position
                print(unit_pos)
                cv2.circle(game_data, (int(unit_pos[0]), int(unit_pos[1])), draw_dict[unit_type][0], draw_dict[unit_type][1], -1)  # draw a circle where the nexus is

        # Enemy structures
        main_base_names = ['nexus', 'commandcenter', 'hatchery']
        for enemy_building in self.known_enemy_structures:
            pos = enemy_building.position
            if enemy_building.name.lower() not in main_base_names:
                cv2.circle(game_data, (int(pos[0]), int(pos[1])), 5, (200, 50, 212), -1)
            else:
                cv2.circle(game_data, (int(pos[0]), int(pos[1])), 15, (0, 0, 255), -1)

        # Enemy units
        for enemy_unit in self.known_enemy_units:
            if not enemy_unit.is_structure:
                worker_names = ['probe',
                                'scv',
                                'drone']
                pos = enemy_unit.position
                if enemy_unit.name.lower() in worker_names:
                    cv2.circle(game_data, (int(pos[0]), int(pos[1])), 1, (55, 0, 155), -1)
                else:
                    cv2.circle(game_data, (int(pos[0]), int(pos[1])), 3, (50, 0, 215), -1)
        flipped = cv2.flip(game_data, 0)  # flipping because cv2 counts from top supply_left
        resized = cv2.resize(flipped, dsize=None, fx=2, fy=2)  # Largen the image
        cv2.imshow('Intel', resized)
        cv2.waitKey(1)


    def __init__(self):
        self.ITERATIONS_PER_MINUTE = 165
        self.MAX_WORKERS = 50
