import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.ids.buff_id import BuffId
from sc2.ids.ability_id import AbilityId
from sc2.player import Bot, Computer
from sc2.constants import PROBE, PYLON, NEXUS, ASSIMILATOR, GATEWAY, CYBERNETICSCORE, STALKER

import random

class CheeseBot(sc2.BotAI):
    async def on_step(self, iteration: int):
        await self.defend()
        await self.distribute_workers()
        await self.handle_chrono()
        await self.build_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.build_gateways()
        await self.build_units()
        await self.expand()
        await self.attack()
    
    async def on_start(self):
        await self.chat_send('glhf')

    async def handle_chrono(self):
        for i in range(self.townhalls.amount):
            chrono_nexus = self.townhalls[i]
            for j in range(i, self.townhalls.amount):
                if chrono_nexus.energy < 50:
                    break 
                nexus = self.townhalls[j]
                if not nexus.is_idle and not nexus.has_buff(BuffId.CHRONOBOOSTENERGYCOST):
                    self.do(chrono_nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus))
            
            for gateway in self.structures(GATEWAY).ready:
                if chrono_nexus.energy < 50:
                    break 
                if not gateway.is_idle and not gateway.has_buff(BuffId.CHRONOBOOSTENERGYCOST):
                    self.do(chrono_nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, gateway))

    async def build_workers(self):
        if self.supply_workers < (22 * len(self.townhalls)):
            for nexus in self.townhalls:
                if nexus.is_idle and self.can_afford(PROBE):
                    self.do(nexus.train(PROBE))
    
    async def build_pylons(self):
        nexus = self.townhalls.random
        if (
            self.supply_left < 2
            and not self.already_pending(PYLON)
            or self.supply_used > 15
            and self.supply_left < 4
            and self.already_pending(PYLON) < 2
        ):
            if self.can_afford(PYLON):
                await self.build(PYLON, near=nexus.position.towards(self.game_info.map_center, 5))
    
    async def build_assimilators(self):
        for nexus in self.structures(NEXUS).ready:
            geysers = self.vespene_geyser.closer_than(10.0, nexus)
            for geyser in geysers:
                if not self.can_afford(ASSIMILATOR):
                    break
                if not self.structures(ASSIMILATOR).closer_than(1.0, geyser).exists:
                    worker = self.select_build_worker(geyser.position)
                    if worker is None:
                        break
                    self.do(worker.build(ASSIMILATOR, geyser))
    
    async def expand(self):
        if self.townhalls.ready.amount + self.already_pending(NEXUS) < 2:
            if self.can_afford(NEXUS):
                await self.expand_now()
    
    async def build_gateways(self):
        if self.structures(PYLON).ready.exists:
            pylon = self.structures(PYLON).ready.random
            if self.structures(GATEWAY).ready.exists:
                if not self.structures(CYBERNETICSCORE):
                    if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                        await self.build(CYBERNETICSCORE, near=pylon)
            if (
                self.can_afford(GATEWAY)
                and not self.already_pending(GATEWAY) 
                and len(self.structures(GATEWAY)) < self.townhalls.ready.amount * 3
                or self.minerals > 600
            ):
                await self.build(GATEWAY, near=pylon)
    
    async def build_units(self):
        if self.structures(GATEWAY).ready.idle:
            for gateway in self.structures(GATEWAY).ready:
                if (
                    self.structures(CYBERNETICSCORE).ready
                    and self.can_afford(STALKER)
                    and self.supply_left > 0 
                    and gateway.is_idle
                ):
                    self.do(gateway.train(STALKER))
    
    async def defend(self):
        if self.units(STALKER).amount > 2:
            for stalker in self.units(STALKER).idle:
                if self.enemy_units:
                    self.do(stalker.attack(random.choice(self.enemy_units)))
    
    async def attack(self):
        for stalker in self.units(STALKER).idle:
            if self.units(STALKER).amount > 20:
                self.do(stalker.attack(self.find_target(self.state)))
            else:
                self.do(stalker.move(self.game_info.map_center))
    
    def find_target(self, state):
        if self.enemy_units:
            return random.choice(self.enemy_units)
        elif self.enemy_structures:
            return random.choice(self.enemy_structures)
        else:
            return self.enemy_start_locations[0]

run_game(maps.get("AcropolisLE"), [
    Bot(Race.Protoss, CheeseBot()),
    Computer(Race.Terran, Difficulty.VeryHard)
], realtime=False)