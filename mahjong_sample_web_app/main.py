from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import (
    HandConfig,
    HandConstants,
    OptionalRules,
)
from mahjong.constants import EAST, NORTH, SOUTH, WEST
from mahjong.meld import Meld
from flask import jsonify, request, render_template, redirect, url_for
from . import app
from .settings import jihai_numbers, yaku_ja_map, rule


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    image = request.form.get("image")
    pies = [
        "2m",
        "3m",
        "4m",
        "4m",
        "4m",
        "2s",
        "3s",
        "4s",
        "e",
        "e",
        "e",
        "2p",
        "3p",
        "4p",
    ]
    tiles = [(i, pi) for i, pi in enumerate(pies)]
    return render_template("index.html", tiles=tiles)


@app.route("/calc", methods=["GET"])
def calc():
    errors = []
    pies = []
    agari_pi = ""
    dora_pies = []
    dora_objs = []
    for i in range(18):
        # breakpoint()
        pi = request.args.get(f"pi-{i}")
        if pi:
            pies.append(pi)
        is_dora = request.args.get(f"dora-{i}", None)
        if is_dora == "1":
            dora_pies.append(pi)
    if len(pies) < 14:
        errors.append(f"Less pi obj: {len(pies)}")
    agari_pi = request.args.get(f"agari", None)
    if not agari_pi:
        errors.append(f"No agari pi obj")
    app.logger.debug(agari_pi)
    agari_obj = str_to_pi_obj(agari_pi)
    if agari_obj is None:
        errors.append(f"Can't make obj: {agari_obj}")
    app.logger.debug("Doras: %s", ",".join(dora_pies))
    for dora_pi in dora_pies:
        dora_objs.append(str_to_pi_obj(dora_pi))

    player_wind_str = request.args.get("ba")
    if player_wind_str == "ton-ba":
        player_wind = EAST
    elif player_wind_str == "nan-ba":
        player_wind = SOUTH
    else:
        errors.append(f"No ba: {player_wind_str}")
    round_wind_str = request.args.get("kaze")
    if round_wind_str == "ton":
        round_wind = EAST
    elif round_wind_str == "nan":
        round_wind = SOUTH
    elif round_wind_str == "sha":
        round_wind = WEST
    elif round_wind_str == "pei":
        round_wind = NORTH
    else:
        errors.append(f"No kaze: {round_wind_str}")

    if errors:
        app.logger.error("pi error: %s", repr(errors))
        return redirect(url_for("index"))
    pies_obj = pies_to_group(pies)
    result = do_calculator(pies_obj, agari_obj, dora_objs, player_wind, round_wind)
    app.logger.debug(result)
    tiles = []
    return render_template("index.html", tiles=tiles, result=result)


def pies_to_group(pies):
    man = []
    pin = []
    sou = []
    honors = []
    for pi in pies:
        pi_obj = str_to_pi_obj(pi)
        if pi_obj[0] == "man":
            man.append(pi_obj[1])
        elif pi_obj[0] == "sou":
            pin.append(pi_obj[1])
        elif pi_obj[0] == "pin":
            sou.append(pi_obj[1])
        elif pi_obj[0] == "honors":
            honors.append(pi_obj[1])
    return {
        "man": "".join(man) if man else None,
        "pin": "".join(pin) if pin else None,
        "sou": "".join(sou) if sou else None,
        "honors": "".join(honors) if honors else None,
    }


def str_to_pi_obj(pi):
    if len(pi) == 2:
        if pi.endswith("m"):
            return "man", pi[0]
        elif pi.endswith("p"):
            return "pin", pi[0]
        elif pi.endswith("s"):
            return "sou", pi[0]
    elif len(pi) == 1:
        jihai_number = jihai_numbers.get(pi)
        return "honors", jihai_number
    else:
        return None, None


def do_calculator(pies_obj, agari_obj, dora_objs, player_wind, round_wind):
    options = rule.copy()
    winds = {"player_wind": player_wind, "round_wind": round_wind}
    app.logger.debug("%s, %s", options, winds)
    calculator = HandCalculator()
    app.logger.debug(pies_obj)
    tiles = TilesConverter.string_to_136_array(**pies_obj)
    win_tile = TilesConverter.string_to_136_array(**dict([agari_obj]))[0]
    dora_tiles = []
    for dora_obj in dora_objs:  # ドラ取得の所は変更が必要かも知れない
        app.logger.debug(dora_obj)
        dora_tiles.append(TilesConverter.string_to_136_array(**dict([dora_obj]))[0])
    app.logger.debug(
        "%s, %s, %s, %s, %s", tiles, win_tile, dora_tiles, player_wind, round_wind
    )

    hans_config = HandConfig(options=OptionalRules(**options), **winds)
    result = calculator.estimate_hand_value(
        tiles, win_tile, dora_indicators=dora_tiles, config=hans_config
    )

    result_error = result.error
    if result_error:
        return result_error
    yaku = result.yaku
    yaku_ja = ", ".join(yaku_ja_map.get(y.name, y.name) for y in yaku)
    return dict(
        fu=result.fu,
        han=result.han,
        cost_main=result.cost["main"],
        cost_additional=result.cost["additional"],
        yaku=yaku_ja,
        dora_len=len(dora_tiles),
    )
