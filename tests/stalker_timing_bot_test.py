import unittest

from importlib import reload
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../protoss")

from protoss import stalker_timing_bot
from sc2.player import Bot, Computer
from sc2 import run_game, maps, Race, Difficulty, main


class TestStalkerTimingBot(unittest.TestCase):
    def test_against_blizz_ai(self):
        player_config = [
            Bot(Race.Protoss, stalker_timing_bot.StalkerTimingBot()),
            Computer(Race.Terran, Difficulty.Easy)
        ]

        gen = main._host_game_iter(
            maps.get("AcropolisLE"),
            player_config,
            realtime=False
        )

        for i in range(30):
            r = next(gen)

            input("Press enter to reload ")

            reload(stalker_timing_bot)
            player_config[0].ai = stalker_timing_bot.StalkerTimingBot()
            gen.send(player_config)


if __name__ == "__main__":
    unittest.main()
