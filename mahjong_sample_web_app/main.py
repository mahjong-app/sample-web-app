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

    round_wind_str = request.args.get("ba")
    if round_wind_str == "ton-ba":
        round_wind = EAST
    elif round_wind_str == "nan-ba":
        round_wind = SOUTH
    else:
        errors.append(f"No ba: {round_wind_str}")
    player_wind_str = request.args.get("kaze")
    if player_wind_str == "ton":
        player_wind = EAST
    elif player_wind_str == "nan":
        player_wind = SOUTH
    elif player_wind_str == "sha":
        player_wind = WEST
    elif player_wind_str == "pei":
        player_wind = NORTH
    else:
        errors.append(f"No kaze: {player_wind}")
    ron = request.args.get("ron")
    tsumo = request.args.get("tsumo")
    if tsumo == "1":
        is_tsumo = True
    elif ron == "1":
        is_tsumo = False
    else:
        errors.append(f"No Ron or Tsumo")
    riichi = request.args.get("riichi")

    if errors:
        app.logger.error("pi error: %s", repr(errors))
        return redirect(url_for("index"))
    pies_obj = pies_to_group(pies)
    attr = {
        "round_wind": round_wind,
        "player_wind": player_wind,
        "is_tsumo": is_tsumo,
        # "opened": False,  # TODO
        "is_riichi": riichi,
        # "is_ippatsu": False,
        # "is_rinshan": False,
        # "is_chankan": False,
        # "is_haitei": False,
        # "is_houtei": False,
        # "is_daburu_riichi": False,
        # "is_nagashi_mangan": False,
        # "is_tenhou": False,
        # "is_renhou": False,
        # "is_chiihou": False,
    }
    result = do_calculator(pies_obj, agari_obj, dora_objs, attr)
    app.logger.debug(result)
    tiles = [(i, pi) for i, pi in enumerate(pies)]
    tiles_attr = {
        "agari_pi": agari_pi,
        "is_tsumo": is_tsumo,
        "is_riichi": riichi,
        "round_wind_str": round_wind_str,
        "player_wind_str": player_wind_str,
    }
    app.logger.debug("tiles_attr, %s", tiles_attr)
    return render_template(
        "index.html", tiles=tiles, result=result, tiles_attr=tiles_attr
    )


def pies_to_group(pies):
    man = []
    pin = []
    sou = []
    honors = []
    for pi in pies:
        pi_obj = str_to_pi_obj(pi)
        if pi_obj[0] == "man":
            man.append(pi_obj[1])
        elif pi_obj[0] == "pin":
            pin.append(pi_obj[1])
        elif pi_obj[0] == "sou":
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
    if not pi:
        return None, None
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


def do_calculator(pies_obj, agari_obj, dora_objs, attr):
    options = rule.copy()
    app.logger.debug("%s, %s", options, attr)
    calculator = HandCalculator()
    app.logger.debug(pies_obj)
    tiles = TilesConverter.string_to_136_array(**pies_obj)
    win_tile = TilesConverter.string_to_136_array(**dict([agari_obj]))[0]
    dora_tiles = []
    for dora_obj in dora_objs:  # ドラ取得の所は変更が必要かも知れない
        app.logger.debug(dora_obj)
        dora_tiles.append(TilesConverter.string_to_136_array(**dict([dora_obj]))[0])
    app.logger.debug("%s, %s, %s", tiles, win_tile, dora_tiles)

    hans_config = HandConfig(options=OptionalRules(**options), **attr)
    result = calculator.estimate_hand_value(
        tiles, win_tile, dora_indicators=dora_tiles, config=hans_config
    )

    result_error = result.error
    if result_error:
        return result_error
    yaku = result.yaku
    yaku_ja = ", ".join(yaku_ja_map.get(y.name, y.name) for y in yaku)
    data = dict(
        fu=result.fu,
        han=result.han,
        cost_main=result.cost["main"],
        cost_additional=None,
        yaku=yaku_ja,
        dora_len=len(dora_tiles),
    )
    if attr.get("is_tsumo"):
        data["cost_additional"] = result.cost["additional"]
    # if opened:
    #     pass

    return data
