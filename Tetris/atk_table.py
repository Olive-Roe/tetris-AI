from math import floor, log1p
import storage

# credit to chouhy/Tetrio-Attack-Table on github
# https://github.com/chouhy/Tetrio-Attack-Table/blob/main/src/tetrioatk.js


def _b2b_bonus(b2b: int, table="tetrio"):
    "Calculate tetrio b2b bonus attack"
    return floor(1+log1p(0.8*b2b)) + (0 if b2b == 1 else (1+(log1p(0.8*b2b) % 1)))/3


def attack_table(lines_cleared, b2b, combo, tspin, pc, table="tetrio"):
    "Calculate lines sent given certain conditions"
    # get initial attack given tspin
    if tspin == "False":
        atk = storage.tetrio_atk[str(lines_cleared)]
    elif tspin == "t-spin":
        atk = storage.tetrio_tspin[str(lines_cleared)]
    elif tspin == "t-spin mini":
        atk = storage.tetrio_tspin_mini[str(lines_cleared)]
    # add b2b bonus
    if b2b > 0:
        atk += _b2b_bonus(b2b)
    # combo multiplier
    atk *= 1 + 0.25*combo
    # combo minifier (no broken combo table)
    atk = max(log1p(combo*1.25), atk)
    # perfect clear bonus
    if pc == "pc":
        atk += 10
    return floor(atk)
