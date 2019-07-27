import random
import yaml

from . import mana

# ----------------------------------------------------------------------

with open("data/cards.yaml") as handle:
    CARDS = yaml.safe_load(handle)

def is_colorless(card):
    return CARDS[card].get("is_colorless")

def is_creature(card):
    return CARDS[card].get("is_creature")

def is_green(card):
    return CARDS[card].get("is_green")

def is_land(card):
    return CARDS[card].get("is_land")

def get_cost(card):
    return mana.Mana(CARDS[card].get("cost"))

def taps_for(card):
    return mana.Mana(CARDS[card].get("taps_for"))

def enters_tapped(card):
    return CARDS[card].get("enters_tapped")

# ----------------------------------------------------------------------

def slug(card):
    return rmchars(card, "'-").lower().replace(" ", "_")

def display(*cards):
    blurbs = []
    for card in sorted(set(cards)):
        if cards.count(card) > 1:
            blurbs.append(str(cards.count(card)) + "*" + disp(card))
        else:
            blurbs.append(disp(card))
    return " ".join(blurbs)

def disp(card):
    try:
        return CARDS[card]["display"]
    except KeyError:
        return rmchars(card, "-' ")

def rmchars(text, chars):
    for c in chars:
        text = text.replace(c, "")
    return text

# ----------------------------------------------------------------------

def load(name):
    cards = []
    with open(name, "r") as handle:
        for line in handle:
            n, name = line.rstrip().split(None, 1)
            cards += int(n) * [name]
    random.shuffle(cards)
    return cards
