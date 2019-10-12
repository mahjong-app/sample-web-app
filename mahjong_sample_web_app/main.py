# from dataclasses import dataclass
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


class ParamError(Exception):
    pass


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
    pies_str = "|".join(pies)
    return redirect(url_for("confirm", pies=pies_str))


@app.route("/confirm", methods=["GET"])
def confirm():
    pies_str = request.args.get("pies", [])
    tiles = [(i, pi) for i, pi in enumerate(pies_str.split("|"))]
    return render_template("index.html", tiles=tiles)


def _get_pi_objs():
    errors = []
    pies = []
    agari_pi_num = None
    agari_pi = None
    naki_pi_dict = {}
    naki_1 = []
    naki_2 = []
    naki_3 = []
    naki_4 = []
    dora_pies = []
    dora_objs = []
    for i in range(18):
        pi = request.args.get(f"pi-{i}")
        if pi:
            pies.append(pi)

        agari_pi_req = request.args.get(f"agari-{i}")
        if agari_pi_req:
            agari_pi = pi
            agari_pi_num = str(i)

        naki_num = request.args.get(f"naki-{i}")
        if naki_num:
            naki_pi_dict.update({f"naki-{i}": naki_num})
            if naki_num == "1":
                naki_1.append(pi)
            elif naki_num == "2":
                naki_2.append(pi)
            elif naki_num == "3":
                naki_3.append(pi)
            elif naki_num == "4":
                naki_4.append(pi)
        is_dora = request.args.get(f"dora-{i}")
        if is_dora == "1":
            dora_pies.append(pi)
    if len(pies) < 14:
        errors.append(f"Less pi obj: {len(pies)}")
    pies_obj = pies_to_group(pies)
    app.logger.debug(agari_pi)
    if not agari_pi:
        errors.append(f"No agari pi obj")
    else:
        agari_obj = str_to_pi_obj(agari_pi)
        if agari_obj is None:
            errors.append(f"Can't make obj: {agari_obj}")

    app.logger.debug("Melds: %s, %s, %s, %s", naki_1, naki_2, naki_3, naki_4)
    melds = _get_meld_pies(naki_1, naki_2, naki_3, naki_4)
    naki_pies = [naki_1, naki_2, naki_3, naki_4]
    app.logger.debug("Doras: %s", ",".join(dora_pies))
    for dora_pi in dora_pies:
        dora_objs.append(str_to_pi_obj(dora_pi))
    if errors:
        raise ParamError(errors)
    return (
        pies,
        pies_obj,
        agari_pi,
        agari_obj,
        agari_pi_num,
        naki_pies,
        naki_pi_dict,
        melds,
        dora_objs,
    )


def _meld_obj(pies, is_open):
    """1メンツの鳴き牌を扱う"""
    if len(pies) < 3:
        return None
    elif len(pies) == 4:
        meld_type = Meld.KAN
    elif len(set(pies)) == 1:
        meld_type = Meld.PON
    else:
        meld_type = Meld.CHI
    pies_obj = pies_to_group(pies)
    meld = Meld(
        meld_type=meld_type,
        tiles=TilesConverter.string_to_136_array(**pies_obj),
        opened=is_open,
    )
    return meld


def _get_meld_pies(naki_1, naki_2, naki_3, naki_4):
    """鳴き牌の4つのグループをオブジェクトにし、リストにまとめる"""
    melds = []
    if naki_1:
        melds.append(_meld_obj(naki_1, is_open=True))
    if naki_2:
        melds.append(_meld_obj(naki_2, is_open=True))
    if naki_3:
        melds.append(_meld_obj(naki_3, is_open=True))
    if naki_4:
        melds.append(_meld_obj(naki_4, is_open=False))
    app.logger.debug("melds obj, %s", melds)
    return melds


def _get_attr_setting():
    round_wind_str = request.args.get("ba")
    if round_wind_str == "ton-ba":
        round_wind = EAST
    elif round_wind_str == "nan-ba":
        round_wind = SOUTH
    else:
        raise ParamError(f"No ba: {round_wind_str}")
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
        raise ParamError(f"No kaze: {player_wind}")
    ron = request.args.get("ron")
    tsumo = request.args.get("tsumo")
    if tsumo == "1":
        is_tsumo = True
        is_ron = False
    elif ron == "1":
        is_tsumo = False
        is_ron = True
    else:
        raise ParamError(f"No Ron or Tsumo")
    riichi = request.args.get("riichi")
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
    tiles_attr = {
        "is_tsumo": is_tsumo,
        "is_ron": is_ron,
        "is_riichi": riichi,
        "round_wind_str": round_wind_str,
        "player_wind_str": player_wind_str,
    }

    return attr, tiles_attr


@app.route("/calc", methods=["GET"])
def calc():
    errors = []

    # 牌の取得
    try:
        pies, pies_obj, agari_pi, agari_obj, agari_pi_num, naki_pies, naki_pi_dict, melds, dora_objs = (
            _get_pi_objs()
        )
    except ParamError as errs:
        errors.extend(errs.args)
    except ValueError as err:
        errors.append(err.args[0])

    # 状態の取得
    try:
        attr, tiles_attr = _get_attr_setting()
    except ParamError as errs:
        errors.extend(errs.args)
    except Exception as err:
        errors.append(err.args[0])

    if errors:
        app.logger.error("pi error: %s", repr(errors))
        return redirect(url_for("index"))

    # 計算の実行
    result = do_calculator(pies_obj, agari_obj, melds, dora_objs, attr)
    app.logger.debug(result)

    # 表示用の設定
    tiles = [(str(i), pi) for i, pi in enumerate(pies)]
    tiles_attr.update(
        {
            "agari_pi": agari_pi,
            "agari_pi_num": agari_pi_num,
            "naki_pi_dict": naki_pi_dict,
        }
    )
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


def do_calculator(pies_obj, agari_obj, melds, dora_objs, attr):
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
        tiles, win_tile, melds=melds, dora_indicators=dora_tiles, config=hans_config
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
