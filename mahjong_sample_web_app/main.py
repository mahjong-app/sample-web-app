from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld
from flask import jsonify, request, render_template, redirect, url_for
from . import app


@app.route("/", methods=["GET"])
def index():
    pies = [
        "2m",
        "3m",
        "4m",
        "4m",
        "4m",
        "3s",
        "4s",
        "5s",
        "6s",
        "6s",
        "6s",
        "2p",
        "3p",
        "4p",
    ]
    tiles = [(i, pi) for i, pi in enumerate(pies)]
    data = {"tiles": tiles}
    return render_template("index.html", data=data)


@app.route("/calc", methods=["GET"])
def calc():
    errors = []
    pies = []
    agari_pi = ""
    for i in range(18):
        # breakpoint()
        pi = request.args.get(f"pi-{i}")
        if pi:
            pies.append(pi)
        is_agari = request.args.get(f"agari-{i}", None)
        if is_agari:
            agari_pi = pi
    if len(pies) < 14:
        errors.append(f"Less pi obj: {len(pies)}")
    if not agari_pi:
        errors.append(f"No agari pi obj")
    app.logger.debug(agari_pi)
    agari_obj = _str_to_pi_obj(agari_pi)
    if agari_obj is None:
        errors.append(f"Can't make obj: {agari_obj}")
    if errors:
        app.logger.error("pi error: %s", repr(errors))
        return redirect(url_for("index"))
    pies_obj = _pies_to_group(pies)
    # breakpoint()
    calculator = HandCalculator()
    app.logger.debug(pies_obj)
    tiles = TilesConverter.string_to_136_array(**pies_obj)
    win_tile = TilesConverter.string_to_136_array(**dict([agari_obj]))[0]
    result = calculator.estimate_hand_value(tiles, win_tile)
    data = dict(
        tiles=[],
        fu=result.fu,
        han=result.han,
        cost_main=result.cost["main"],
        cost_additional=result.cost["additional"],
        yaku=result.yaku,
    )
    app.logger.debug(data)
    return render_template("index.html", data=data)


def _pies_to_group(pies):
    man = []
    pin = []
    sou = []
    honors = []
    for pi in pies:
        pi_obj = _str_to_pi_obj(pi)
        if pi_obj[0] == "man":
            man.append(pi[0])
        elif pi_obj[0] == "sou":
            pin.append(pi[0])
        elif pi_obj[0] == "pin":
            sou.append(pi[0])
        elif pi_obj[0] == "honor":
            honors.append(pi[0])
            honors = []  # TODO: ツールへの与え方がわからないので空にしている
    return {
        "man": "".join(man) if man else None,
        "pin": "".join(pin) if pin else None,
        "sou": "".join(sou) if sou else None,
        "honors": "".join(honors) if honors else None,
    }


def _str_to_pi_obj(pi):
    if len(pi) == 2:
        if pi.endswith("m"):
            return "man", pi[0]
        elif pi.endswith("p"):
            return "pin", pi[0]
        elif pi.endswith("s"):
            return "sou", pi[0]
    else:
        if pi == "h":
            return "honor", None
        elif pi == "f":
            return "honor", None
        elif pi == "c":
            return "honor", None
        elif pi == "e":
            return "honor", None
        elif pi == "s":
            return "honor", None
        elif pi == "w":
            return "honor", None
        elif pi == "n":
            return "honor", None
