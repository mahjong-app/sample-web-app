from mahjong.constants import EAST, NORTH, SOUTH, WEST

calc_tests = []

# マンズオンリー
calc_tests.append(
    [
        {"fu": 30, "han": 10, "cost_main": 16000, "cost_additional": None},  #  result
        [
            "1m",
            "2m",
            "3m",
            "1m",
            "2m",
            "3m",
            "4m",
            "5m",
            "6m",
            "7m",
            "8m",
            "9m",
            "9m",
            "9m",
        ],  #  pies
        "1m",  # agari
        [],  # dora_pies
        {
            "round_wind": EAST,
            "player_wind": WEST,
            "is_tsumo": False,
            "is_riichi": False,
        },  # attr
    ]
)

