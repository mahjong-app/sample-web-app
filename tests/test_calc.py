import pytest
from mahjong_sample_web_app.main import pies_to_group, str_to_pi_obj, do_calculator
from mahjong.constants import EAST, NORTH, SOUTH, WEST
from .calc_parametrize import calc_tests


def test_str_to_pi_obj(base):
    pi = "2m"
    result = "man", "2"
    pi_obj = str_to_pi_obj(pi)
    assert result[0] == pi_obj[0]
    assert result[1] == pi_obj[1]

    pi = "e"
    result = "honors", "1"
    pi_obj = str_to_pi_obj(pi)
    assert result[0] == pi_obj[0]
    assert result[1] == pi_obj[1]

    pi = None
    pi_obj = str_to_pi_obj(pi)
    assert pi_obj[0] is None
    assert pi_obj[1] is None


def test_pies_to_group(base):
    pies = ["1m", "9m", "2s", "6s", "4p", "e", "c"]
    result = {"man": "19", "pin": "4", "sou": "26", "honors": "17"}
    assert result == pies_to_group(pies)

    pies = ["e", "s", "w", "n", "h", "f", "c"]
    result = {"man": None, "pin": None, "sou": None, "honors": "1234567"}
    assert result == pies_to_group(pies)

    pies = ["9m", "1m", "6s", "4p", "2s", "3m", "2m"]
    result = {"man": "9132", "pin": "4", "sou": "62", "honors": None}
    assert result == pies_to_group(pies)


def test_calc1(base):
    result = {"fu": 30, "han": 10, "cost_main": 16000, "cost_additional": None}
    pies = [
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
    ]
    agari = "1m"
    dora_pies = []
    attr = {
        "round_wind": EAST,
        "player_wind": WEST,
        "is_tsumo": False,
        # "opened": False,  # TODO
        "is_riichi": False,
    }
    pies_obj = pies_to_group(pies)
    agari_obj = str_to_pi_obj(agari)
    dora_objs = []
    for dora_pi in dora_pies:
        dora_objs.append(str_to_pi_obj(dora_pi))
    data = do_calculator(pies_obj, agari_obj, dora_objs, attr)
    assert result["fu"] == data["fu"]
    assert result["han"] == data["han"]
    assert result["cost_main"] == data["cost_main"]
    assert result["cost_additional"] == data["cost_additional"]


@pytest.mark.parametrize(
    ("result", "pies", "agari", "dora_pies", "attr"),
    [
        (esult, pies, agari, dora_pies, attr)
        for esult, pies, agari, dora_pies, attr in calc_tests
    ],
)
def test_calc_parametrize(base, result, pies, agari, dora_pies, attr):
    pies_obj = pies_to_group(pies)
    agari_obj = str_to_pi_obj(agari)
    dora_objs = []
    for dora_pi in dora_pies:
        dora_objs.append(str_to_pi_obj(dora_pi))
    data = do_calculator(pies_obj, agari_obj, dora_objs, attr)
    assert result["fu"] == data["fu"]
    assert result["han"] == data["han"]
    assert result["cost_main"] == data["cost_main"]
    assert result["cost_additional"] == data["cost_additional"]

