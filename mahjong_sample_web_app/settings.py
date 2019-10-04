from mahjong.hand_calculating.hand_config import HandConstants


jihai_numbers = {"h": "5", "f": "6", "c": "7", "e": "1", "s": "2", "w": "3", "n": "4"}

yaku_ja_map = {"Tanyao": "タンヤオ", "Sanshoku Dojun": "三色同順"}

rule = {
    "has_open_tanyao": True,
    # "has_aka_dora": True,
    "has_double_yakuman": False,
    "kazoe_limit": HandConstants.KAZOE_LIMITED,
}
