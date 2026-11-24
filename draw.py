#!/usr/bin/env python3
"""Front page for Monday 23 November 2026 — v3.5.

Exact-detail revision of v3.4 on the sum-22 top-1 (bagarte,
final #1) layout, two points, following the user's order
literally (it reverses the v3.4 bold pass):
(1) BOLD only on the "Monday 23 November 2026" masthead
(Didone Black + 2px stroke) and on the RED kicker line —
every other text is NOT bold: the v3.4 1px stroke is removed
from the hero/small headlines, the place+country labels and
the "REGION · TOPIC" labels are back to NotoSans-Bold (not
Black), and the headline wrap widths are restored;
(2) the red kicker is moved UP close under the masthead
(ink top y=114, the masthead ink ends at 110) and enlarged
to fill the full width left-to-right (LiberationSerif-Bold
23, stretched to exactly 1000px, MX..RX, one line).
The pictures are flat vector shapes drawn here, the words
are written here; nothing is photographed, pasted, or
copied in.

Renders entry.png (1024x1024, byte-stable) from world.geo.json.
Usage: python3 draw.py

All 29 items happened, or were first reported, on Monday 23
November 2026, checked live against the wires (Reuters, AP, AFP,
BBC, Al Jazeera, Guardian, Detik, Xinhua, IANS, Yonhap, ABC,
ESPN, UKMTO, WHO and others). Stories that belong to an earlier
day are named in DATE CHECK, not drawn.

No clock, no dice, no network: repeated runs emit identical bytes.
Pillow is needed only to draw; the graded entrypoint (main.py) is a
stdlib-only copy of the finished PNG.
"""
import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# --- colours: cream sheet, ink, navy, red, gold --------------------------
BG = (247, 242, 231)
PANEL = (253, 250, 242)
BLACK = (17, 17, 17)
BLUE = (16, 62, 150)
MIDNIGHT = (12, 28, 58)
SCARLET = (220, 28, 60)
WINE = (179, 34, 44)
GILT = (232, 178, 36)
ASH = (90, 90, 90)
EDGE = (180, 170, 150)
SEA = (235, 240, 243)
SHORE = (238, 220, 165)
LEAF = (16, 165, 90)
TANGERINE = (230, 150, 0)
AZURE = (20, 110, 230)
TEAL = (0, 110, 160)
DOTGREY = (70, 70, 70)

PILL = {
    "CONFIRMED": LEAF,
    "REPORTED": LEAF,
    "FORECAST": AZURE,
    "CLAIM": TANGERINE,
    "OFFICIAL": TEAL,
    "ONGOING": TANGERINE,
}

# --- type ------------------------------------------------------------------
DEJAVU = "/usr/share/fonts/truetype/dejavu"
NOTO = "/usr/share/fonts/truetype/noto"
LIBER = "/usr/share/fonts/truetype/liberation"


def _load(name, size, folder):
    return ImageFont.truetype(os.path.join(folder, name), size)


class TY:
    """All faces, loaded once."""
    # Masthead: bagarte's date is a high-contrast Didone (Playfair /
    # Didot family). Noto Serif Display Black is the closest face on
    # this system; size 88 gives an 86px ink height, matching
    # bagarte's masthead (86px), when squeezed to 996 wide.
    mast = _load("NotoSerifDisplay-Black.ttf", 88, NOTO)
    kick = _load("NotoSans-Black.ttf", 10, NOTO)
    # v3.5: the red kicker is the ONLY bold serif besides the
    # masthead — LiberationSerif-Bold 23, stretched to fill the
    # full 1000px width (natural width 975px at 23px).
    kickbold = _load("LiberationSerif-Bold.ttf", 23, LIBER)
    clock = _load("NotoSans-Bold.ttf", 12, NOTO)
    clocksm = _load("NotoSans-Bold.ttf", 11, NOTO)
    tl = _load("NotoSans-Bold.ttf", 11, NOTO)
    tlev = _load("NotoSans-Regular.ttf", 11, NOTO)
    strip = _load("NotoSans-Bold.ttf", 12, NOTO)
    stripsm = _load("NotoSans-Bold.ttf", 9, NOTO)
    striptn = _load("NotoSans-Bold.ttf", 8, NOTO)
    tag = _load("NotoSans-Bold.ttf", 8, NOTO)
    src = _load("NotoSans-Bold.ttf", 9, NOTO)
    hhead = _load("LiberationSerif-Bold.ttf", 25, LIBER)
    shead = _load("LiberationSerif-Bold.ttf", 17, LIBER)
    hdeck = _load("LiberationSerif-Regular.ttf", 12, LIBER)
    sdeck = _load("LiberationSerif-Regular.ttf", 11, LIBER)
    pin = _load("NotoSans-Bold.ttf", 11, NOTO)
    pinsm = _load("NotoSans-Bold.ttf", 9, NOTO)
    abig = _load("NotoSans-Black.ttf", 24, NOTO)
    asmall = _load("NotoSans-Bold.ttf", 12, NOTO)
    amid = _load("NotoSans-Black.ttf", 17, NOTO)
    amidsm = _load("NotoSans-Bold.ttf", 11, NOTO)
    hlab = _load("NotoSans-Black.ttf", 16, NOTO)
    hlabsm = _load("NotoSans-Bold.ttf", 9, NOTO)
    slab = _load("NotoSans-Bold.ttf", 12, NOTO)
    slab10 = _load("NotoSans-Bold.ttf", 10, NOTO)
    slabssm = _load("NotoSans-Bold.ttf", 8, NOTO)
    also = _load("NotoSans-Bold.ttf", 11, NOTO)
    also10 = _load("NotoSans-Bold.ttf", 10, NOTO)
    alsosub = _load("NotoSans-Regular.ttf", 8, NOTO)
    alsosub7 = _load("NotoSans-Regular.ttf", 7, NOTO)
    alsonum = _load("NotoSans-Bold.ttf", 11, NOTO)
    sect = _load("NotoSans-Black.ttf", 13, NOTO)
    chk = _load("NotoSans-Bold.ttf", 12, NOTO)
    foot = _load("NotoSans-Bold.ttf", 10, NOTO)
    numbig = _load("NotoSans-Black.ttf", 26, NOTO)
    numlab = _load("NotoSans-Bold.ttf", 10, NOTO)
    numtitle = _load("NotoSans-Black.ttf", 12, NOTO)
    topic = _load("NotoSans-Bold.ttf", 11, NOTO)
    topicsm = _load("NotoSans-Bold.ttf", 9, NOTO)
    bignum = _load("NotoSans-Black.ttf", 30, NOTO)


# --- layout (bagarte geometry) ---------------------------------------------
MX = 12
RX = 1012
HY = 200          # heroes + numbers box top
HH = 252          # hero / numbers height
HW = 260          # hero width
NW = 196          # numbers-box width
HA = 105          # hero art height
SY = 460          # smalls row 1 top
SR = 154          # small row pitch
SW = 196          # small width
SA = 60           # small art height
SH = 146          # small card height
MY = 768          # map + also top
CY = 942          # date-check top (box 942-992, 3 lines at 14px)
FY = 996          # footer top

ISSUES = []

# --- the 29 stories --------------------------------------------------------
# Drawn item: (no, place, topic, source, status, headline, deck,
# art big label, art small label, art key, pill).
# Hero headlines at most 3 lines (23px); hero decks at most 3 lines
# (12px). Small headlines at most 2 lines (15px); small decks at
# most 2 lines (11px, deck + " — source").
# CONFIRMED = two named sources agree; REPORTED = one named source;
# CLAIM = one side's claim, unverified; ONGOING = still unfolding.
FRONT = [
    (1, "ANTALYA", "CLIMATE", "UN NEWS · REUTERS", "REPORTED",
     "COP31 ends without a climate pact",
     "Closing plenary rejects the draft 'Antalya Pact', which named "
     "no fossil fuels; first COP without a deal in 17 years.",
     "NO DEAL", "FOSSIL FUELS CUT", "copcollapse", "REPORTED"),
    (2, "THE GULF", "WAR", "AP · REUTERS · AL JAZEERA", "REPORTED",
     "Iran vows to break the US blockade",
     "Tehran vows to end the blockade 'by all means'; IRGC claims "
     "radar hits in Bahrain; Houthis claim a refinery strike.",
     "BREAK THE BLOCKADE", "2 TANKERS HIT", "gulfwar", "REPORTED"),
    (3, "WASHINGTON", "POLITICS", "AP · REUTERS", "REPORTED",
     "Democrats win 258 House seats",
     "Hubbard flips a North Carolina seat on recount; largest "
     "Democratic majority since 1992.",
     "258 SEATS", "BIGGEST SINCE 1992", "house258", "REPORTED"),
    (4, "SANTA CLARA", "TECH", "REUTERS · AP", "REPORTED",
     "Nvidia pressed on chips diverted to China",
     "Bessent seeks answers on chips sent to China.",
     "CHIP PROBE", "CHINA DIVERSION", "chip", "REPORTED"),
    (5, "CIKANDE", "DISASTER", "XINHUA · DETIK", "REPORTED",
     "Factory fire toll climbs to 24 dead",
     "24 bodies found, about 30 still missing.",
     "24 DEAD", "BANTEN PLANT", "factoryfire", "REPORTED"),
    (6, "NEW DELHI", "DIPLOMACY", "IANS · MEA", "REPORTED",
     "Nepal PM Shah holds talks with Modi",
     "First foreign trip; $2bn package on the table.",
     "$2BN", "STATE VISIT", "statevisit", "REPORTED"),
    (7, "BENGHAZI", "WAR", "REUTERS · AP", "REPORTED",
     "Zelensky: Ukraine sank warship in Libya",
     "Seven naval drones sank the corvette at berth.",
     "7 DRONES", "SUNK AT BERTH", "sinking", "REPORTED"),
    (8, "GULF OF FINLAND", "SEA", "REUTERS", "REPORTED",
     "Sparta II still burning off Finland",
     "Fire rages on the drone-hit ship; 16 crew safe.",
     "16 SAFE", "SHIP ABLAZE", "shipfire", "REPORTED"),
    (9, "WASHINGTON", "SANCTIONS", "AP", "REPORTED",
     "US sanctions Iranian 'shadow banking'",
     "Treasury sanctions 8 people and 22 entities.",
     "30 TARGETS", "SHADOW BANKING", "sanctions", "REPORTED"),
    (10, "THE GULF", "ENERGY", "REUTERS · AP", "REPORTED",
     "Oil slides 4% as Gulf attacks continue",
     "Brent down nearly 4% Monday as supply returns.",
     "–4%", "BRENT SLIDES", "oil", "REPORTED"),
    (11, "WASHINGTON", "POLITICS", "AP", "REPORTED",
     "Gomez quits Congress after ethics report",
     "Democrat to resign after a House panel finds misconduct "
     "toward a staffer.",
     "TO QUIT", "ETHICS REPORT", "resign", "REPORTED"),
    (12, "BEIJING", "SPACE", "XINHUA", "REPORTED",
     "China names Shenzhou-24 crew",
     "First foreign astronaut aboard the station.",
     "SHENZHOU-24", "FIRST FOREIGN CREW", "space", "REPORTED"),
    (13, "NAIROBI", "DIPLOMACY", "AP", "REPORTED",
     "Kenya and DR Congo restore full ties",
     "Nairobi and Kinshasa agree to restore full diplomatic ties "
     "after a rift.",
     "FULL TIES", "NAIROBI–KINSHASA", "handshake", "REPORTED"),
]

# Also-list: (no, city, one line, outlet). THREE columns (bagarte),
# each 200px wide (160px of text) at 10px bold, so every main line
# is shortened to fit 160px (measured, all <=158px). All 16 are
# Monday stories.
ALSO = [
    (14, "Antalya", "COP31 chief blames EU", "REUTERS"),
    (15, "Riyadh", "Houthi missile downed", "REUTERS"),
    (16, "Tehran", "Ahmadi gets 74 lashes", "AP"),
    (17, "Washington", "Trump vs Newsom", "AP"),
    (18, "Kyiv", "Zelensky urges talks", "REUTERS"),
    (19, "Manchester", "Thousands flee", "AP"),
    (20, "US", "Storms hit Thanksgiving", "AP"),
    (21, "Washington", "Dems plan debate", "AP"),
    (22, "Dhaka", "Hasina plans return", "REUTERS"),
    (23, "Canberra", "PM defends Bowen", "AP"),
    (24, "Juba", "Attack kills 24 civilians", "AP"),
    (25, "Congo", "Ebola response hit", "REUTERS"),
    (26, "Lisbon", "March over living costs", "REUTERS"),
    (27, "Myanmar", "ASEAN move 'unfair'", "REUTERS"),
    (28, "Warsaw", "Russia targets rapper", "AP"),
    (29, "Brussels", "EU keeps Ukraine aid", "REUTERS"),
]

# Six numbers for the dark-navy box — one big figure per top story.
# Colours are the user's exact specification (v3.3), overriding the
# region-colour scheme: 258 light blue, $2BN green, 24 red, 7 dark
# blue, 2 (tankers) green, 2 DAYS white.
STATS = [
    ("258", "House seats clinched", "AMERICAS", (110, 170, 230)),
    ("$2BN", "Nepal aid package", "ASIA-PACIFIC", (80, 200, 120)),
    ("24", "dead in Cikande fire", "ASIA-PACIFIC", (240, 90, 90)),
    ("7", "drones sank Merkury", "AFRICA", (90, 130, 230)),
    ("2", "tankers hit in Hormuz", "WORLD", (80, 200, 120)),
    ("2 DAYS", "COP31 overtime", "WORLD", (255, 255, 255)),
]

# Region tallies, counted from the 29 items by subject:
# EUROPE 6 (8, 18, 19, 26, 28, 29); MIDDLE EAST 2 (2, 16);
# AFRICA 4 (7, 13, 24, 25); ASIA-PACIFIC 5 (5, 6, 12, 22, 27);
# AMERICAS 7 (3, 4, 9, 11, 17, 20, 21); OCEANIA 1 (23);
# WORLD 4 (1, 10, 14, 15). 6+2+4+5+7+1+4 = 29.
# Fills sampled from bagarte (sum-22 final #1) region bar, pure fill
# at each box edge: EUROPE blue, MIDDLE EAST red, AFRICA green,
# ASIA orange, AMERICAS purple, OCEANIA teal, WORLD dark grey.
REGIONS = [
    ("EUROPE", 6, (36, 100, 198), "white"),
    ("MIDDLE EAST", 2, (198, 52, 38), "white"),
    ("AFRICA", 4, (39, 136, 63), "white"),
    ("ASIA-PACIFIC", 5, (225, 118, 23), "white"),
    ("AMERICAS", 7, (116, 82, 189), "white"),
    ("OCEANIA", 1, (20, 136, 140), "white"),
    ("WORLD", 4, (72, 72, 84), "white"),
]

# Region and filing country for each drawn story (1-13), from the
# region tallies above. Used for the "REGION · TOPIC" label, the
# top-bar number circle, the numbers-box figure colour and the
# map-pin colour. WORLD reads as white on the navy numbers box.
REGION_OF = {1: "WORLD", 2: "MIDDLE EAST", 3: "AMERICAS",
             4: "AMERICAS", 5: "ASIA-PACIFIC", 6: "ASIA-PACIFIC",
             7: "AFRICA", 8: "EUROPE", 9: "AMERICAS", 10: "WORLD",
             11: "AMERICAS", 12: "ASIA-PACIFIC", 13: "AFRICA"}
COUNTRY_OF = {1: "TÜRKIYE", 2: "BAHRAIN", 3: "USA", 4: "USA",
              5: "INDONESIA", 6: "INDIA", 7: "LIBYA", 8: None,
              9: "USA", 10: None, 11: "USA", 12: "CHINA",
              13: "KENYA"}
REGION_COLOUR = {label: fill for label, _c, fill, _i in REGIONS}
REGION_SHORT = {"ASIA-PACIFIC": "ASIA"}


def region_label(region):
    """Short region name for the 'REGION · TOPIC' label."""
    return REGION_SHORT.get(region, region)


# Lighter version of each region colour, for big figures on the
# dark-navy numbers box. Sampled from bagarte's box: EUROPE sky
# blue, ASIA light orange, OCEANIA light teal, WORLD white; the
# others are the same lightening of their region fill.
NUM_COLOUR = {
    "EUROPE": (108, 158, 210),
    "MIDDLE EAST": (235, 125, 115),
    "AFRICA": (100, 205, 130),
    "ASIA-PACIFIC": (228, 165, 75),
    "AMERICAS": (175, 150, 230),
    "OCEANIA": (80, 190, 185),
    "WORLD": (255, 255, 255),
}

# Flag country for each also-list item (14-29).
FLAG_OF = {14: "TR", 15: "SA", 16: "IR", 17: "US", 18: "UA",
           19: "GB", 20: "US", 21: "US", 22: "BD", 23: "AU",
           24: "SS", 25: "CD", 26: "PT", 27: "MM", 28: "PL",
           29: "BE"}

# Small sub-line under each also-list item (14-29), like
# bagarte: a short detail plus the source, in small grey text.
# Each follows from its main line (no new claim).
ALSO_SUB = {14: "Chief blames EU for the failed pact",
            15: "Saudi air defence intercepts missile",
            16: "Singer lashed in Tehran",
            17: "Trump attacks California governor",
            18: "President pushes for negotiations",
            19: "Crowd flees in panic",
            20: "Holiday travel hit by storms",
            21: "Party plans primary debates",
            22: "Ex-PM eyes return to Bangladesh",
            23: "PM backs energy minister",
            24: "Rebels blamed for civilian deaths",
            25: "Outbreak response hit by fighting",
            26: "Protesters demand relief",
            27: "Junta criticises ASEAN move",
            28: "Rapper targeted, Poland says",
            29: "Brussels holds Ukraine funding"}

# Region for each also-list item (14-29), from the region tallies:
# WORLD 14, 15; MIDDLE EAST 16; AMERICAS 17, 20, 21; EUROPE 18, 19,
# 26, 28, 29; ASIA-PACIFIC 22, 27; OCEANIA 23; AFRICA 24, 25.
# The also-list number is coloured by its region (bagarte).
ALSO_REGION = {14: "WORLD", 15: "WORLD", 16: "MIDDLE EAST",
               17: "AMERICAS", 18: "EUROPE", 19: "EUROPE",
               20: "AMERICAS", 21: "AMERICAS", 22: "ASIA-PACIFIC",
               23: "OCEANIA", 24: "AFRICA", 25: "AFRICA",
               26: "EUROPE", 27: "ASIA-PACIFIC", 28: "EUROPE",
               29: "EUROPE"}

# --- the map ---------------------------------------------------------------
# Red numbered pins for the 13 drawn items; navy dots for the 16
# also-list lines. Values are (longitude, latitude).
PINS = {
    1: (30.7, 36.9), 2: (56.0, 26.5), 3: (-77.0, 38.9),
    4: (-121.9, 37.4), 5: (106.1, -6.0), 6: (77.2, 28.6),
    7: (20.1, 32.1), 8: (24.5, 59.9), 9: (-77.0, 38.9),
    10: (56.0, 26.5), 11: (-77.0, 38.9), 12: (116.4, 39.9),
    13: (36.8, -1.3),
}
DOTS = {
    14: (30.7, 36.9), 15: (-74.0, 40.7), 16: (51.4, 35.7),
    17: (-77.0, 38.9), 18: (30.5, 50.4), 19: (-2.2, 53.5),
    20: (-100.0, 39.0), 21: (-77.0, 38.9), 22: (90.4, 23.8),
    23: (149.1, -35.3), 24: (31.6, 4.85), 25: (29.2, -1.7),
    26: (-9.1, 38.7), 27: (96.2, 19.8), 28: (21.0, 52.2),
    29: (4.4, 50.8),
}
# Markers that would collide are fanned out a few pixels with a thin
# leader back to the true spot. Washington holds pins 3, 9, 11 and
# dots 17, 21; the Gulf holds pins 2 and 10; Antalya holds pin 1
# and dot 14.
PIN_OFF = {3: (0, 0), 9: (15, -9), 11: (-15, 9),
           10: (13, 11), 4: (0, -10), 7: (0, 0), 13: (0, 0)}
DOT_OFF = {14: (13, -9), 17: (15, 11), 21: (-15, -9),
           15: (0, -10), 20: (0, 0), 22: (0, -10), 23: (0, 0),
           24: (-13, -8), 25: (-12, 8), 27: (10, 8), 28: (-10, -10),
           29: (-14, 6), 16: (0, 0), 18: (12, -2), 19: (-12, -6),
           26: (-12, 6)}


# --- drawing helpers ---------------------------------------------------------
def box(d, x0, y0, x1, y1, fill):
    d.rectangle((x0, y0, x1, y1), fill=fill)


def disc(d, cx, cy, r, fill, outline=None, width=1):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill,
              outline=outline, width=width)


def ring(d, x0, y0, x1, y1, outline, width=1):
    d.ellipse((x0, y0, x1, y1), outline=outline, width=width)


def seg(d, pts, fill, width=1):
    d.line(pts, fill=fill, width=width)


def poly(d, pts, fill, outline=None):
    d.polygon(pts, fill=fill, outline=outline)


def flag(d, code, x, y, w=16, h=11):
    """A small flat flag for an also-list item (drawn, no emoji).
    Simplified to the recognisable bands/emblem at 16x11 px."""
    def hband(y0, y1, col):
        d.rectangle((x, y + y0, x + w, y + y1), fill=col)

    def vband(x0, x1, col):
        d.rectangle((x + x0, y, x + x1, y + h), fill=col)

    if code == "TR":  # Turkiye: red, white crescent + star
        d.rectangle((x, y, x + w, y + h), fill=(227, 10, 23))
        disc(d, x + 6, y + h // 2, 3, "white")
        disc(d, x + 7, y + h // 2, 2, (227, 10, 23))
        d.polygon([(x + 11, y + 3), (x + 12, y + 5), (x + 14, y + 5),
                   (x + 12, y + 6), (x + 13, y + 8), (x + 11, y + 7),
                   (x + 9, y + 8), (x + 10, y + 6), (x + 8, y + 5),
                   (x + 10, y + 5)], fill="white")
    elif code == "SA":  # Saudi: green, white shahada + sword lines
        d.rectangle((x, y, x + w, y + h), fill=(0, 106, 68))
        d.rectangle((x + 2, y + 3, x + w - 2, y + 5), fill="white")
        d.rectangle((x + 3, y + 7, x + w - 3, y + 8), fill="white")
    elif code == "IR":  # Iran: green-white-red horizontal
        hband(0, h // 3, (0, 122, 61))
        hband(h // 3, 2 * h // 3, "white")
        hband(2 * h // 3, h, (218, 0, 0))
    elif code == "US":  # USA: stripes + blue canton
        for i in range(7):
            hband(i * h // 7, (i + 1) * h // 7,
                  (178, 34, 52) if i % 2 == 0 else "white")
        d.rectangle((x, y, x + w * 2 // 5, y + h * 4 // 7),
                    fill=(60, 59, 110))
        for sx in (2, 6, 10):
            for sy in (2, 5):
                disc(d, x + sx, y + sy, 1, "white")
    elif code == "UA":  # Ukraine: blue over yellow
        hband(0, h // 2, (0, 91, 187))
        hband(h // 2, h, (255, 213, 0))
    elif code == "GB":  # UK: simplified Union Jack
        d.rectangle((x, y, x + w, y + h), fill=(0, 36, 125))
        d.line([(x, y), (x + w, y + h)], fill="white", width=2)
        d.line([(x + w, y), (x, y + h)], fill="white", width=2)
        d.rectangle((x + w // 2 - 1, y, x + w // 2 + 1, y + h),
                    fill=(200, 16, 46))
        d.rectangle((x, y + h // 2 - 1, x + w, y + h // 2 + 1),
                    fill=(200, 16, 46))
    elif code == "BD":  # Bangladesh: green, red disc
        d.rectangle((x, y, x + w, y + h), fill=(0, 106, 78))
        disc(d, x + w // 2 - 1, y + h // 2, 4, (244, 42, 65))
    elif code == "AU":  # Australia: blue, canton + stars
        d.rectangle((x, y, x + w, y + h), fill=(0, 47, 108))
        d.rectangle((x, y, x + w // 2, y + h // 2), fill=(0, 36, 125))
        d.line([(x, y), (x + w // 2, y + h // 2)], fill="white", width=1)
        d.line([(x + w // 2, y), (x, y + h // 2)], fill="white", width=1)
        d.rectangle((x + w // 4 - 1, y, x + w // 4 + 1, y + h // 2),
                    fill=(200, 16, 46))
        d.rectangle((x, y + h // 4 - 1, x + w // 2, y + h // 4 + 1),
                    fill=(200, 16, 46))
        for sx, sy in ((w * 3 // 4, h // 4), (w * 3 // 4, h * 3 // 4),
                       (w * 7 // 8, h // 2)):
            disc(d, x + sx, y + sy, 1, "white")
    elif code == "SS":  # South Sudan: black-red-green + blue triangle
        hband(0, h // 3, (0, 0, 0))
        hband(h // 3, 2 * h // 3, (218, 41, 28))
        hband(2 * h // 3, h, (0, 122, 61))
        poly(d, [(x, y), (x, y + h), (x + w // 2, y + h // 2)],
             (0, 63, 135))
        disc(d, x + 4, y + h // 2, 1, (255, 210, 0))
    elif code == "CD":  # DR Congo: blue, red diagonal, yellow star
        d.rectangle((x, y, x + w, y + h), fill=(0, 91, 187))
        d.line([(x, y + h), (x + w, y)], fill=(206, 16, 33), width=3)
        disc(d, x + 4, y + 3, 1, (255, 210, 0))
    elif code == "PT":  # Portugal: green | red vertical
        vband(0, w * 2 // 5, (0, 122, 61))
        vband(w * 2 // 5, w, (200, 16, 46))
    elif code == "MM":  # Myanmar: yellow-green-red + white star
        hband(0, h // 3, (254, 203, 0))
        hband(h // 3, 2 * h // 3, (52, 138, 71))
        hband(2 * h // 3, h, (234, 40, 42))
        disc(d, x + w // 2, y + h // 2, 2, "white")
    elif code == "PL":  # Poland: white over red
        hband(0, h // 2, "white")
        hband(h // 2, h, (220, 20, 60))
    elif code == "BE":  # Belgium: black-yellow-red vertical
        vband(0, w // 3, (0, 0, 0))
        vband(w // 3, 2 * w // 3, (253, 218, 0))
        vband(2 * w // 3, w, (237, 41, 57))
    d.rectangle((x, y, x + w, y + h), outline=(120, 120, 120), width=1)


def draw_segs(d, x, y, segs, font):
    """Draw [(text, fill), ...] in sequence on one line; return end x."""
    cx = x
    for text, fill in segs:
        txt(d, (cx, y), text, font, fill)
        cx += int(d.textlength(text, font=font))
    return cx


def txt(d, xy, s, font, fill, anchor=None, stroke=0, stroke_fill=None):
    d.text(xy, s, font=font, fill=fill, anchor=anchor,
           stroke_width=stroke, stroke_fill=stroke_fill)


def wrap(d, text, font, width, cap=None):
    """Greedy wrap to `width` px; records an issue past `cap` lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if cap is not None and len(lines) > cap:
        ISSUES.append("TRUNCATED (%d lines): %s" % (len(lines), text))
        lines = lines[:cap]
    return lines


def burst(d, cx, cy, outer, inner, fill):
    """Five-point starburst for blasts and base hits."""
    pts = []
    for k in range(10):
        r = outer if k % 2 == 0 else inner
        a = math.radians(-90 + k * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def fresh(w, h):
    img = Image.new("RGB", (w, h))
    return img, ImageDraw.Draw(img)


def _fit(d, text, font, maxw, floor):
    """Shrink a bold face until `text` fits `maxw` (not below floor)."""
    f = font
    while d.textlength(text, font=f) > maxw and f.size > floor:
        f = ImageFont.truetype(
            os.path.join(NOTO, "NotoSans-Black.ttf"), f.size - 1)
    return f

def art(key, w, h):
    """One picture, flat vector shapes drawn from scratch.
    Leads paint at h=105; smalls paint at h=80 then shrink to 60.
    A lead's bottom-left stays clear for its tag; a small's top
    18px stays clear for its number+place bar."""
    img, d = fresh(w, h)
    if key == "copcollapse":
        # Lead 1: the climate talks fail. Teal hall, round globe,
        # thermometer past the mark, a torn page, a NO DEAL band.
        # The compact place label now sits top-left inside the
        # picture, so the top is kept clear for it: the globe and
        # the thermometer sit lower (tops at y26+), and the wall
        # clock moved to the top-right, clear of the torn page.
        box(d, 0, 0, w, h, (11, 110, 110))
        disc(d, 51, 58, 31, (30, 120, 200), outline=(20, 20, 20), width=2)
        for a, b, c, e in ((30, 39, 52, 53), (52, 55, 74, 71),
                           (30, 59, 44, 71)):
            d.ellipse((a, b, c, e), fill=(60, 180, 90))
        seg(d, [(22, 58), (80, 58)], "white", 1)
        box(d, 132, 26, 142, 74, "white")
        d.rectangle((132, 26, 142, 74), outline=(20, 20, 20))
        box(d, 134, 28, 140, 74, (220, 30, 40))
        disc(d, 137, 78, 11, (220, 30, 40), outline=(20, 20, 20), width=2)
        for ty in (32, 40, 48, 56, 64):
            seg(d, [(142, ty), (147, ty)], (20, 20, 20))
        txt(d, (154, 28), "+1.5°C", TY.amid, "white")
        txt(d, (154, 50), "LIMIT", TY.amidsm, "white")
        txt(d, (154, 62), "PASSED", TY.amidsm, "white")
        box(d, 228, 22, 256, 78, "white")
        d.rectangle((228, 22, 256, 78), outline=(20, 20, 20), width=2)
        for ly in (32, 42, 52):
            seg(d, [(236, ly), (248, ly)], (60, 60, 60), 2)
        seg(d, [(228, 22), (222, 40), (230, 56), (224, 78)], SCARLET, 3)
        # NO DEAL band moved to the bottom-left so the bottom-right
        # stays clear for the REPORTED pill (bagarte).
        box(d, 8, 84, 108, 102, WINE)
        txt(d, (58, 93), "NO DEAL", TY.amid, "white", anchor="mm")
        # wall clock top-right and delegates lower-right: a scene
        # with people, not just icons. The delegates sit LOW (heads
        # y80, bodies y87-96) so they clear "PASSED" (ends y73),
        # the thermometer bulb (x126-148) and the NO DEAL band
        # (x<108); the rightmost body ends at x196, clear of the
        # REPORTED pill (x198+).
        disc(d, 205, 14, 9, "white", outline=(20, 20, 20), width=1)
        seg(d, [(205, 14), (205, 7)], (20, 20, 20), 1)
        seg(d, [(205, 14), (210, 16)], (20, 20, 20), 1)
        for fx, shirt in ((152, (200, 60, 40)), (168, (40, 90, 160)),
                          (184, (240, 200, 60))):
            disc(d, fx + 6, 80, 5, (220, 180, 140))
            poly(d, [(fx, 96), (fx + 12, 96), (fx + 10, 87),
                     (fx + 2, 87)], shirt)
    elif key == "gulfwar":
        # Lead 2: the Gulf at war, as a map. Iran coast on top,
        # Arabian coast below, Bahrain with two base bursts, dashed
        # missile arcs, a burning tanker, a 5th Fleet destroyer.
        box(d, 0, 0, w, h, (14, 48, 96))
        poly(d, [(0, 0), (w, 0), (w, 14), (240, 16), (180, 12),
                 (120, 16), (60, 14), (0, 18)], (214, 196, 150))
        # "IRAN" moved right so the compact place label (top-left
        # inside the picture) does not cover it.
        txt(d, (170, 4), "IRAN", TY.amidsm, BLACK)
        poly(d, [(0, h), (0, 82), (70, 74), (140, 82), (210, 76),
                 (260, 82), (w, 72), (w, h)], (214, 196, 150))
        # SAUDI ARABIA sits bottom-left now, so the bottom-right
        # stays clear for the REPORTED pill (bagarte).
        txt(d, (8, 90), "SAUDI ARABIA", TY.amidsm, BLACK, anchor="la")
        d.ellipse((120, 30, 152, 52), fill=(214, 196, 150))
        d.ellipse((176, 44, 196, 62), fill=(196, 176, 128))
        for ax0, ay0, ax1, ay1, hump in ((0, 22, 128, 38, 12),
                                         (0, 48, 136, 44, 14)):
            for ti in range(21):
                t = ti / 20
                qx = ax0 + (ax1 - ax0) * t
                qy = ay0 + (ay1 - ay0) * t - hump * math.sin(math.pi * t)
                if ti % 2 == 0:
                    disc(d, qx, qy, 2, "white")
        for bx, by in ((128, 36), (144, 46)):
            burst(d, bx, by, 10, 4, (255, 200, 60))
            burst(d, bx, by, 5, 2, (255, 140, 40))
            disc(d, bx, by, 3, "white")
            ring(d, bx - 8, by - 8, bx + 8, by + 8, "white", 1)
        # burning tanker, right of the island
        poly(d, [(180, 60), (232, 60), (224, 68), (188, 68)], (30, 30, 40))
        box(d, 188, 48, 202, 60, "white")
        burst(d, 212, 44, 9, 4, (255, 140, 40))
        burst(d, 212, 44, 5, 2, (255, 210, 31))
        for lx, ly, s, anch in ((136, 56, "BAHRAIN", "ma"),
                                (170, 28, "THE GULF", "ma")):
            txt(d, (lx, ly), s, TY.amidsm, "white", anchor=anch,
                stroke=1, stroke_fill=(0, 0, 0))
        poly(d, [(200, 34), (248, 34), (240, 42), (208, 42)],
             (120, 125, 135))
        box(d, 214, 26, 226, 34, (120, 125, 135))
        seg(d, [(220, 26), (220, 20)], (120, 125, 135), 2)
        seg(d, [(196, 44), (252, 44)], "white")
        txt(d, (224, 50), "5TH FLEET", TY.amidsm, "white", anchor="ma",
            stroke=1, stroke_fill=(0, 0, 0))
        # sea texture, a second vessel, a radar mast on Bahrain,
        # and smoke over the burning tanker.
        for wx in range(8, 168, 26):
            seg(d, [(wx, 68), (wx + 12, 68)], (180, 200, 220), 1)
        poly(d, [(28, 58), (58, 58), (52, 64), (34, 64)], (90, 95, 105))
        box(d, 38, 50, 48, 58, (120, 125, 135))
        seg(d, [(43, 50), (43, 44)], (120, 125, 135), 2)
        seg(d, [(136, 30), (136, 18)], (60, 60, 60), 2)
        seg(d, [(130, 18), (142, 14)], (60, 60, 60), 2)
        for sx, sy, sr in ((196, 36, 5), (190, 30, 6), (198, 26, 4)):
            disc(d, sx, sy, sr, (120, 120, 126))
    elif key == "house258":
        # Lead 3: the US House flips. Navy hall, white Capitol dome
        # with columns and a gold cupola, seat bar bottom-right:
        # 258 blue against 177 red. The dome assembly sits 20px
        # right of centre so the compact place label (top-left
        # inside the picture) does not cover the cupola; the flag
        # moved down so its top clears the label box.
        box(d, 0, 0, w, h, MIDNIGHT)
        for sx, sy in ((22, 30), (70, 30), (210, 30), (280, 30),
                       (340, 30), (378, 30)):
            disc(d, sx, sy, 1, "white")
        d.ellipse((119, 20, 215, 68), fill="white")
        box(d, 117, 48, 217, 66, "white")
        for cx in (132, 152, 172, 192, 212):
            seg(d, [(cx, 48), (cx, 66)], MIDNIGHT, 2)
        box(d, 107, 66, 227, 70, "white")
        box(d, 143, 12, 191, 26, "white")
        disc(d, 167, 11, 12, GILT)
        # Seat bar moved left and narrowed so the bottom-right stays
        # clear for the REPORTED pill (bagarte): blue 258, red 177.
        box(d, 85, 82, 157, 96, (40, 90, 200))
        box(d, 157, 82, 205, 96, (200, 40, 50))
        txt(d, (121, 89), "258", TY.amidsm, "white", anchor="mm")
        txt(d, (181, 89), "177", TY.amidsm, "white", anchor="mm")
        txt(d, (250, 8), "SINCE 1992", TY.amidsm, GILT, anchor="ra")
        # a flag on the left, steps under the dome, and windows on
        # the dome: a fuller scene.
        seg(d, [(30, 24), (30, 72)], (200, 200, 210), 2)
        box(d, 30, 24, 58, 36, (200, 40, 50))
        for sy in (28, 32):
            seg(d, [(30, sy), (58, sy)], "white", 1)
        box(d, 30, 24, 42, 30, (40, 60, 140))
        disc(d, 36, 27, 1, "white")
        for sy in (73, 77, 81):
            seg(d, [(105, sy), (230, sy)], (180, 180, 190), 2)
        for wx, wy in ((140, 40), (167, 35), (194, 40)):
            disc(d, wx, wy, 2, MIDNIGHT)
    elif key == "shipfire":
        # Sparta II ablaze off Finland: grey sea, dark cargo ship,
        # container stack, white bridge, deck fire, two drones.
        box(d, 0, 0, w, h, (30, 90, 140))
        seg(d, [(0, 56), (w, 56)], (140, 180, 210))
        poly(d, [(28, 56), (168, 56), (158, 68), (38, 68)], (30, 30, 40))
        box(d, 40, 40, 64, 56, "white")
        for cx, col in ((76, (200, 60, 40)), (100, (40, 140, 90)),
                        (124, (230, 180, 40))):
            box(d, cx, 44, cx + 20, 56, col)
        burst(d, 92, 40, 9, 4, (255, 140, 40))
        burst(d, 92, 40, 5, 2, (255, 210, 31))
        for dx, dy in ((60, 26), (140, 24)):
            d.ellipse((dx - 5, dy - 3, dx + 5, dy + 3), fill=(90, 95, 105))
            seg(d, [(dx - 8, dy - 5), (dx + 8, dy - 5)], (200, 200, 210), 2)
            seg(d, [(dx, dy + 3), (dx, dy + 8)], (200, 200, 210))
        seg(d, [(20, 72), (176, 72)], "white")
    elif key == "sinking":
        # Russian warship sinking off Libya: dark sea, grey warship
        # listing hard, bow under, smoke, a drone above.
        box(d, 0, 0, w, h, (20, 60, 110))
        seg(d, [(0, 58), (w, 58)], (140, 180, 210))
        poly(d, [(40, 58), (150, 58), (160, 46), (120, 52), (60, 52)],
             (90, 95, 105))
        box(d, 96, 38, 118, 52, (120, 125, 135))
        seg(d, [(107, 38), (107, 28)], (120, 125, 135), 2)
        for sx, sy, sr in ((128, 30, 8), (140, 22, 10), (152, 16, 7)):
            disc(d, sx, sy, sr, (120, 120, 126))
        burst(d, 84, 48, 8, 3, (255, 140, 40))
        for wx in range(0, w, 24):
            seg(d, [(wx, 66), (wx + 12, 66)], "white")
        # drone moved right so the compact place label (top-left
        # inside the picture) does not cover it.
        d.ellipse((150, 20, 160, 26), fill=(90, 95, 105))
        seg(d, [(142, 18), (158, 18)], (200, 200, 210), 2)
    elif key == "factoryfire":
        # Candy-factory fire in Cikande: sawtooth roof, fire bursting
        # through, smoke drifting right, one glowing window.
        box(d, 0, 0, w, h, (180, 190, 205))
        box(d, 0, 62, w, h, (120, 120, 126))
        box(d, 20, 44, 176, 62, (90, 90, 100))
        for sx in (20, 52, 84, 116, 148):
            poly(d, [(sx, 44), (sx + 16, 32), (sx + 32, 44)], (70, 70, 80))
        box(d, 168, 24, 176, 44, (70, 70, 80))
        disc(d, 98, 36, 20, (255, 140, 40))
        disc(d, 98, 40, 10, (255, 210, 31))
        disc(d, 99, 44, 5, (255, 120, 30))
        for sx, sy, sr in ((98, 16, 7), (112, 10, 9), (130, 8, 8),
                           (146, 12, 6)):
            disc(d, sx, sy, sr, (90, 90, 96))
        for wx in (30, 56, 130, 156):
            box(d, wx, 50, wx + 10, 58, (40, 40, 50))
        box(d, 82, 50, 92, 58, (255, 180, 60))
    elif key == "statevisit":
        # Nepal PM lands on a state visit: plane on the runway,
        # two flags on poles.
        box(d, 0, 0, w, h, (200, 220, 235))
        box(d, 0, 58, w, h, (90, 90, 98))
        for dx in range(6, w, 22):
            seg(d, [(dx, 66), (dx + 11, 66)], "white", 2)
        for fx, cols in ((24, ((255, 150, 0), "white", (0, 130, 60))),
                         (164, ((200, 30, 50), (20, 60, 140), None))):
            seg(d, [(fx, 24), (fx, 58)], (60, 60, 60), 2)
            box(d, fx, 24, fx + 22, 32, cols[0])
            box(d, fx, 32, fx + 22, 40, cols[1])
            if cols[2]:
                box(d, fx, 40, fx + 22, 48, cols[2])
        d.ellipse((70, 44, 132, 54), fill=(40, 90, 160))
        poly(d, [(124, 46), (132, 38), (136, 46)], (40, 90, 160))
        poly(d, [(84, 52), (94, 62), (98, 52)], (40, 90, 160))
        for wx in (84, 118):
            disc(d, wx, 58, 4, (20, 20, 20))
    elif key == "chip":
        # Nvidia pressed on chips diverted to China: dark board, big
        # green AI chip with gold pins, red arrow to a red flag.
        box(d, 0, 0, w, h, (16, 24, 44))
        for ty in range(24, h, 14):
            seg(d, [(0, ty), (w, ty)], (30, 40, 60))
        box(d, 30, 26, 78, 62, (16, 140, 80))
        d.rectangle((30, 26, 78, 62), outline=(60, 200, 120), width=2)
        for px in (36, 48, 60, 72):
            seg(d, [(px, 22), (px, 26)], GILT, 2)
            seg(d, [(px, 62), (px, 66)], GILT, 2)
        for py in (32, 44, 56):
            seg(d, [(26, py), (30, py)], GILT, 2)
            seg(d, [(78, py), (82, py)], GILT, 2)
        txt(d, (54, 44), "AI", TY.amid, "white", anchor="mm")
        seg(d, [(84, 44), (120, 30), (150, 36)], SCARLET, 3)
        poly(d, [(150, 36), (140, 30), (140, 42)], SCARLET)
        box(d, 156, 26, 186, 46, (200, 30, 40))
        burst(d, 171, 36, 6, 2, (255, 210, 31))
        txt(d, (54, 74), "WHERE DID THEY GO?", TY.slabssm, "white",
            anchor="ma")
    elif key == "sanctions":
        # US sanctions Iranian shadow banking: a ledger page, a red
        # stamp, a chain of blocked accounts.
        box(d, 0, 0, w, h, (220, 215, 200))
        box(d, 0, 62, w, h, (90, 85, 70))
        poly(d, [(60, 18), (136, 22), (132, 66), (56, 62)], "white",
             outline=(60, 60, 60))
        for ly in (30, 38, 46, 54):
            seg(d, [(66, ly), (126, ly + 1)], ASH)
        for xx in (120, 108):
            seg(d, [(xx - 4, 30 - 4), (xx + 4, 30 + 4)], SCARLET, 2)
            seg(d, [(xx + 4, 30 - 4), (xx - 4, 30 + 4)], SCARLET, 2)
        d.ellipse((140, 20, 184, 52), outline=SCARLET, width=3)
        txt(d, (162, 36), "BLOCKED", TY.slabssm, SCARLET, anchor="mm")
        for cx in (40, 100, 160):
            disc(d, cx, 56, 5, (40, 40, 50))
            box(d, cx - 3, 61, cx + 3, 74, (40, 40, 50))
        seg(d, [(45, 56), (95, 56)], (40, 40, 50), 2)
        seg(d, [(105, 56), (155, 56)], (40, 40, 50), 2)
    elif key == "oil":
        # Oil slides as Gulf attacks continue: a dark barrel, a red
        # falling arrow, a price line dropping.
        box(d, 0, 0, w, h, (20, 30, 50))
        for gy in range(14, h, 12):
            seg(d, [(0, gy), (w, gy)], (35, 45, 65))
        d.ellipse((24, 26, 76, 74), fill=(30, 35, 45),
                  outline=(120, 125, 135), width=2)
        seg(d, [(24, 38), (76, 38)], (120, 125, 135), 2)
        seg(d, [(24, 56), (76, 56)], (120, 125, 135), 2)
        txt(d, (50, 50), "OIL", TY.amid, "white", anchor="mm")
        seg(d, [(96, 22), (130, 40), (160, 34), (188, 58)], SCARLET, 3)
        poly(d, [(188, 58), (178, 56), (184, 66)], SCARLET)
    elif key == "resign":
        # Gomez to quit after an ethics report: an empty chair, a
        # closing door, a gavel on the desk.
        box(d, 0, 0, w, h, (200, 200, 210))
        box(d, 0, 60, w, h, (120, 110, 100))
        # door moved down so its top clears the compact place
        # label (top-left inside the picture).
        box(d, 30, 26, 90, 60, (90, 60, 40))
        d.rectangle((30, 26, 90, 60), outline=(60, 40, 20), width=2)
        disc(d, 78, 43, 4, GILT)
        box(d, 110, 26, 170, 60, (150, 140, 130))
        d.rectangle((110, 26, 170, 60), outline=(90, 80, 70), width=2)
        box(d, 118, 34, 140, 52, (200, 200, 210))
        seg(d, [(118, 43), (140, 43)], (60, 60, 60), 2)
        seg(d, [(150, 30), (150, 56)], (60, 60, 60), 2)
        poly(d, [(60, 62), (76, 62), (72, 76), (64, 76)], (60, 40, 20))
        box(d, 56, 76, 80, 79, (60, 40, 20))
    elif key == "space":
        # China names the Shenzhou-24 crew: night sky, a rocket
        # climbing, a station ring, stars.
        box(d, 0, 0, w, h, (8, 12, 30))
        for sx, sy in ((20, 14), (60, 10), (110, 16), (160, 12),
                       (185, 20), (40, 30), (140, 28)):
            disc(d, sx, sy, 1, "white")
        # rocket + station shifted down 6px so the rocket tip
        # clears the compact place label (top-left inside the
        # picture).
        poly(d, [(92, 26), (104, 26), (108, 54), (88, 54)], "white")
        poly(d, [(98, 14), (104, 26), (92, 26)], SCARLET)
        poly(d, [(88, 54), (80, 66), (88, 60)], (200, 200, 210))
        poly(d, [(108, 54), (116, 66), (108, 60)], (200, 200, 210))
        burst(d, 98, 68, 8, 3, (255, 180, 60))
        ring(d, 140, 36, 180, 68, GILT, 2)
        disc(d, 160, 52, 6, GILT)
        txt(d, (160, 52), "24", TY.slabssm, BLACK, anchor="mm")
    elif key == "handshake":
        # Kenya and DR Congo restore ties: two flags on poles, two
        # hands meeting in the middle.
        box(d, 0, 0, w, h, (200, 220, 235))
        box(d, 0, 58, w, h, (90, 90, 98))
        # flags moved down so their tops clear the compact place
        # label (top-left inside the picture).
        for fx, cols in ((20, ((0, 0, 0), (200, 30, 40), (0, 130, 60))),
                         (150, ((0, 60, 160), (255, 210, 31), (200, 30, 40)))):
            seg(d, [(fx, 26), (fx, 58)], (60, 60, 60), 2)
            box(d, fx, 26, fx + 24, 34, cols[0])
            box(d, fx, 34, fx + 24, 42, cols[1])
            box(d, fx, 42, fx + 24, 50, cols[2])
        poly(d, [(70, 40), (98, 34), (104, 40), (98, 46), (76, 48)],
             (200, 170, 140), outline=(120, 90, 60))
        poly(d, [(126, 40), (98, 34), (92, 40), (98, 46), (120, 48)],
             (220, 190, 160), outline=(120, 90, 60))
        seg(d, [(70, 40), (126, 40)], (120, 90, 60), 2)
    else:
        raise ValueError("unknown art: %s" % key)
    return img.resize((w, h), Image.LANCZOS)


# --- assembly ----------------------------------------------------------------
def heropic(key, w):
    """A lead picture: painted 105 tall, returned at 105."""
    return art(key, w, HA)


def minipic(key):
    """A small picture: painted 196x80, shrunk to 196x60."""
    return art(key, SW, 80).resize((SW, SA), Image.LANCZOS)


def topbar(d, x, y, w, num, place, country, region, vtag, font,
           boxh, discr, pad):
    """Bagarte's compact number+place label: a WHITE box fitted to
    the text length only (never full width), placed at the top-left
    INSIDE the picture, with a thin ink outline. The number sits
    in a disc coloured by the story's region, place + country in
    black bold caps. The art's top-left is kept clear for it (see
    the art functions). Text shrinks until it fits."""
    label = place + (", " + country if country else "")
    f = font
    while d.textlength(label, font=f) > w - 40 and f.size > 8:
        f = ImageFont.truetype(
            os.path.join(NOTO, "NotoSans-Bold.ttf"), f.size - 1)
    tw = int(d.textlength(label, font=f))
    bw = pad + discr * 2 + 4 + tw + pad
    bx, by = x + pad, y + pad
    d.rectangle((bx, by, bx + bw, by + boxh), fill="white",
                outline=BLACK, width=1)
    disc(d, bx + pad + discr, by + boxh // 2, discr,
         REGION_COLOUR[region])
    txt(d, (bx + pad + discr, by + boxh // 2), str(num), TY.tag,
        "white", anchor="mm")
    txt(d, (bx + pad + discr * 2 + 4, by + boxh // 2), label, f,
        BLACK, anchor="lm")


def pill_br(d, x, y, w, h, vtag):
    """A status pill at the bottom-right corner of a picture
    (bagarte): green REPORTED, amber CLAIM / ONGOING. Sits inside
    the picture's bottom-right corner, 4px off the right edge and
    3px off the bottom. The art's bottom-right is kept clear for
    it (see the art functions)."""
    pw = int(d.textlength(vtag, font=TY.tag)) + 10
    x1 = x + w - 4
    y1 = y + h - 3
    d.rounded_rectangle((x1 - pw, y1 - 12, x1, y1), radius=2,
                        fill=PILL[vtag])
    txt(d, (x1 - pw + 5, y1 - 6), vtag, TY.tag, "white", anchor="lm")


def hero_card(img, d, story, x, y, w):
    """A lead card, 252 tall (bagarte): 105px art with a number+place
    bar, the status pill at the art's bottom-right corner, a topic
    line, a 2–3 line 25px serif headline, a 2–3 line 12px serif
    deck, and a 9px source line, all inside a 1px ink box."""
    num, place, topic, src, _st, head, deck, big, small, key, vtag = story
    box(d, x, y, x + w, y + HH, PANEL)
    pic = heropic(key, w)
    img.paste(pic, (x, y))
    d2 = ImageDraw.Draw(img)
    topbar(d2, x, y, w, num, place, COUNTRY_OF[num], REGION_OF[num],
           vtag, TY.slab, 18, 7, 4)
    pill_br(d2, x, y, w, HA, vtag)
    ty = y + HA + 6
    region = REGION_OF[num]
    txt(d, (x + 8, ty),
        "%s · %s" % (region_label(region), topic), TY.topic,
        REGION_COLOUR[region])
    hl = wrap(d, head, TY.hhead, w - 16, 3)
    dl = wrap(d, deck, TY.hdeck, w - 16, 3)
    hy = ty + 16
    for j, ln in enumerate(hl):
        txt(d, (x + 8, hy + j * 29), ln, TY.hhead, BLACK)
    dy = hy + len(hl) * 29 + 2
    for j, ln in enumerate(dl):
        txt(d, (x + 8, dy + j * 14), ln, TY.hdeck, (60, 60, 60))
    txt(d, (x + 8, y + HH - 14), src, TY.src, ASH)
    d.rectangle((x, y, x + w, y + HH), outline=BLACK, width=1)


def small_card(img, d, story, x, y):
    """A small card, 146 tall (bagarte): 60px mini scene illustration
    with a number+place bar and the status pill at the art's
    bottom-right corner, a topic line, a 2-line 17px serif headline
    and a 2-line 11px serif deck with its source, inside a 1px ink
    box. No badge: the scene shows fully, as in bagarte's smalls."""
    num, place, topic, src, _st, head, deck, big, small, key, vtag = story
    w = SW
    box(d, x, y, x + w, y + SH, PANEL)
    pic = minipic(key)
    img.paste(pic, (x, y))
    d2 = ImageDraw.Draw(img)
    topbar(d2, x, y, w, num, place, COUNTRY_OF[num], REGION_OF[num],
           vtag, TY.slab10, 15, 6, 3)
    pill_br(d2, x, y, w, SA, vtag)
    ty = y + SA + 5
    region = REGION_OF[num]
    txt(d, (x + 8, ty),
        "%s · %s" % (region_label(region), topic), TY.topicsm,
        REGION_COLOUR[region])
    hl = wrap(d, head, TY.shead, w - 16, 2)
    for j, ln in enumerate(hl):
        txt(d, (x + 8, ty + 14 + j * 20), ln, TY.shead, BLACK)
    dl = wrap(d, deck + " — " + src, TY.sdeck, w - 16, 2)
    for j, ln in enumerate(dl):
        txt(d, (x + 8, ty + 15 + len(hl) * 20 + j * 12), ln,
            TY.sdeck, (60, 60, 60))
    d.rectangle((x, y, x + w, y + SH), outline=BLACK, width=1)


def numbers_box(d, x, y):
    """Bagarte's dark-navy THE DAY IN NUMBERS box: title plus six
    big figures, each a 26px number over a 10px label. Each figure
    wears the user's exact colour (v3.3): 258 light blue, $2BN
    green, 24 red, 7 dark blue, 2 (tankers) green, 2 DAYS white."""
    box(d, x, y, x + NW, y + HH, MIDNIGHT)
    txt(d, (x + 10, y + 8), "THE DAY IN NUMBERS", TY.numtitle, "white")
    seg(d, [(x + 10, y + 26), (x + NW - 10, y + 26)], (80, 100, 140), 1)
    ey = y + 30
    for value, label, region, colour in STATS:
        fv = TY.numbig
        while d.textlength(value, font=fv) > NW - 20 and fv.size > 18:
            fv = ImageFont.truetype(
                os.path.join(NOTO, "NotoSans-Black.ttf"), fv.size - 1)
        txt(d, (x + 10, ey), value, fv, colour)
        txt(d, (x + 10, ey + 26), label, TY.numlab, (200, 210, 230))
        ey += 36
    d.rectangle((x, y, x + NW, y + HH), outline=BLACK, width=1)


def _inside(lon, lat, polys):
    """Ray-casting point-in-polygon for one lon/lat against a list
    of (ring, bbox) pairs; the bbox skips rings far from the point
    so the denser dot grid stays fast."""
    for ring, (x0, x1, y0, y1) in polys:
        if not (x0 <= lon <= x1 and y0 <= lat <= y1):
            continue
        inside = False
        n = len(ring)
        j = n - 1
        for i in range(n):
            xi, yi = ring[i]
            xj, yj = ring[j]
            if ((yi > lat) != (yj > lat)):
                xint = (xj - xi) * (lat - yi) / (yj - yi) + xi
                if lon < xint:
                    inside = not inside
            j = i
        if inside:
            return True
    return False


def draw_map(d, x0, y0, w, h):
    """Bagarte's dotted world map: pale blue sea, land as a grid of
    dark dots (from world.geo.json), navy dots for the also-list
    stories, numbered red pins for the drawn stories. Pins and dots
    that would collide are fanned out with a thin leader back to
    their true spot."""
    with open(os.path.join(HERE, "world.geo.json")) as fh:
        geo = json.load(fh)
    polys = []
    for feat in geo["features"]:
        geom = feat["geometry"]
        rings = []
        if geom["type"] == "Polygon":
            rings = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            rings = geom["coordinates"]
        for poly_ring in rings:
            ring = poly_ring[0]
            xs = [p[0] for p in ring]
            ys = [p[1] for p in ring]
            polys.append((ring, (min(xs), max(xs), min(ys), max(ys))))

    def px(lon):
        return x0 + (lon + 180.0) / 360.0 * w

    def py(lat):
        return y0 + (90.0 - lat) / 180.0 * h

    box(d, x0, y0, x0 + w, y0 + h, SEA)
    # dotted land: a denser, slightly darker dot grid than v3.2 so
    # the continents read clearly and solidly like bagarte's
    # (airy but unmistakable). Pins stay region-coloured.
    step = 3
    for gy in range(2, h, step):
        lat = 90.0 - (gy / h) * 180.0
        for gx in range(2, w, step):
            lon = (gx / w) * 360.0 - 180.0
            if _inside(lon, lat, polys):
                disc(d, x0 + gx, y0 + gy, 1.2, (150, 150, 150))
    for num, (lon, lat) in DOTS.items():
        tx, ty = px(lon), py(lat)
        ox, oy = DOT_OFF.get(num, (0, 0))
        if (ox, oy) != (0, 0):
            seg(d, [(tx, ty), (tx + ox, ty + oy)], BLACK, 1)
        disc(d, tx + ox, ty + oy, 2, MIDNIGHT)
    for num, (lon, lat) in PINS.items():
        tx, ty = px(lon), py(lat)
        ox, oy = PIN_OFF.get(num, (0, 0))
        if (ox, oy) != (0, 0):
            seg(d, [(tx, ty), (tx + ox, ty + oy)],
                REGION_COLOUR[REGION_OF[num]], 1)
        cx, cy = tx + ox, ty + oy
        disc(d, cx, cy, 7, REGION_COLOUR[REGION_OF[num]],
             outline="white", width=1)
        fp = TY.pin if num < 10 else TY.pinsm
        txt(d, (cx, cy), str(num), fp, "white", anchor="mm")

def build():
    img, d = fresh(W, H)
    box(d, 0, 0, W - 1, H - 1, BG)
    # ---- top bar 0-18: one line in a solid dark-navy bar across
    # the full width — white name left, gold count right (bagarte).
    # Gold sampled from bagarte's right-hand text.
    box(d, 0, 0, W, 18, MIDNIGHT)
    txt(d, (MX, 9), "THE WORLD IN ONE DAY", TY.kick, "white",
        anchor="lm")
    txt(d, (RX, 9),
        "29 STORIES · 7 REGIONS · ALL FROM THIS ONE DAY", TY.kick,
        (238, 198, 110), anchor="rm")
    # ---- masthead 16-128: the date in a Didone at 88px, squeezed
    # horizontally to 996px so its ink top sits at 24 (ink 24-110,
    # 86px tall, matching bagarte). ----
    title = "Monday 23 November 2026"
    lw = int(d.textlength(title, font=TY.mast)) + 12
    layer = Image.new("RGBA", (lw, 150), (0, 0, 0, 0))
    lt = ImageDraw.Draw(layer)
    # BOLD: a 2px stroke on the Didone Black so the masthead reads
    # as heavy as bagarte's (the thin Didone strokes are thickened).
    lt.text((4, 0), title, font=TY.mast, fill=BLACK + (255,),
            stroke_width=2, stroke_fill=BLACK + (255,))
    ink_top = layer.getbbox()[1]
    layer = layer.resize((996, 150), Image.LANCZOS)
    img.paste(layer, (MX, 24 - ink_top), layer)
    # ---- red kicker: BOLD (the only bold serif besides the
    # masthead), moved UP close under the masthead and enlarged
    # to fill the full width left-to-right (MX..RX, 1000px).
    # Rendered on a layer at LiberationSerif-Bold 23 (natural
    # width 975px), cropped to its ink, then stretched to exactly
    # 1000px wide and pasted so the ink top sits at y=114 (the
    # masthead ink ends at 110; the region bar is at 150).
    kicker = ("COP31 ends without a climate pact · Iran vows to "
              "break the blockade · Democrats win 258 seats")
    klayer = Image.new("RGBA", (1100, 60), (0, 0, 0, 0))
    kd = ImageDraw.Draw(klayer)
    kd.text((0, 0), kicker, font=TY.kickbold, fill=SCARLET + (255,))
    kb = klayer.getbbox()
    kcrop = klayer.crop(kb).resize((1000, kb[3] - kb[1]), Image.LANCZOS)
    img.paste(kcrop, (MX, 114), kcrop)
    # ---- region bar 150-168: seven SEPARATE boxes, 18px tall with
    # 12px text (bagarte's size), each sized to its text with
    # wider padding, ~7px white gaps, the whole row centred
    # (bagarte). Colours are the sampled region fills.
    bx, by, bh = MX, 150, 18
    gap = 7
    widths = []
    for label, count, fill, ink in REGIONS:
        widths.append(int(d.textlength("%s %d" % (label, count),
                                       font=TY.strip)) + 20)
    total = sum(widths) + gap * (len(widths) - 1)
    sx = (W - total) // 2
    for (label, count, fill, ink), w in zip(REGIONS, widths):
        box(d, sx, by, sx + w, by + bh, fill)
        txt(d, (sx + w / 2, by + 9), "%s %d" % (label, count),
            TY.strip, ink, anchor="mm")
        sx += w + gap
    # ---- UTC timeline 172-192: a DARK NAVY band (bagarte) — the
    # timeline reads as a distinct horizontal LINE. Pixel sampling
    # proved bagarte's UTC row is a dark-navy band (25,41,111) and
    # our light row had NO band at all (plain cream 247,242,231),
    # which is why it read as "just a red UTC box". A small RED box
    # for "UTC" at the left, then the six time+event pairs (gold
    # bold times, white events, middot separators) spread across
    # the band. The band runs MX..1000 and never touches the right
    # grey border line (RX=1012).
    tl_y = 172
    tl_h = 20
    box(d, MX, tl_y, 1000, tl_y + tl_h, MIDNIGHT)
    box(d, MX, tl_y, MX + 34, tl_y + tl_h, SCARLET)
    txt(d, (MX + 17, tl_y + tl_h // 2), "UTC", TY.src, "white",
        anchor="mm")
    timeline = [("05:30", "Modi meets Shah"),
                ("06:00", "COP31 ends, no deal"),
                ("09:00", "Iran vows blockade break"),
                ("11:00", "Cikande toll at 24"),
                ("14:30", "Nvidia chip probe"),
                ("19:00", "Democrats clinch 258")]
    # Natural width of all items + separators; the slack is spread
    # evenly into the five gaps (remainder to the first gaps) so
    # the last item ends exactly at x=1000.
    sep = "  ·  "
    sepw = int(d.textlength(sep, font=TY.tl))
    nat = 0
    for tt, ev in timeline:
        nat += int(d.textlength(tt, font=TY.tl))
        nat += int(d.textlength(" " + ev, font=TY.tlev))
    nat += sepw * (len(timeline) - 1)
    extra = (1000 - (MX + 42)) - nat
    ngap = len(timeline) - 1
    gap = extra // ngap if ngap else 0
    rem = extra % ngap if ngap else 0
    tx = MX + 42
    for i, (tt, ev) in enumerate(timeline):
        txt(d, (tx, tl_y + tl_h // 2), tt, TY.tl, GILT, anchor="lm")
        tx += int(d.textlength(tt, font=TY.tl))
        txt(d, (tx, tl_y + tl_h // 2), " " + ev, TY.tlev, "white",
            anchor="lm")
        tx += int(d.textlength(" " + ev, font=TY.tlev))
        if i < len(timeline) - 1:
            txt(d, (tx, tl_y + tl_h // 2), sep, TY.tl, GILT,
                anchor="lm")
            tx += sepw + gap + (1 if i < rem else 0)
    # ---- heroes 200-452: three 260px leads, then the numbers box. ----
    hx = MX
    for i, story in enumerate(FRONT[:3]):
        hero_card(img, d, story, hx, HY, HW)
        hx += HW + 8
    numbers_box(d, hx, HY)
    # ---- smalls 460-760: two rows of five, 196 wide, 204 pitch,
    # 154 row pitch. ----
    for r in range(2):
        for c in range(5):
            k = 3 + r * 5 + c
            small_card(img, d, FRONT[k], MX + c * 204,
                       SY + r * SR)
    # ---- also-list (left) + map (right) 768-948. THREE columns
    # (bagarte): col 1 = 14-19, col 2 = 20-24, col 3 = 25-29.
    # Each also item is TWO lines (bagarte): the main line, then a
    # small grey sub-line (detail + source) below it. The two lines
    # share a 24px row (main 10px, sub 7px), so the tallest column
    # (6 items) ends near the map bottom without overflowing into
    # DATE CHECK.
    txt(d, (MX, MY), "ALSO ON MONDAY 23 NOVEMBER", TY.sect, BLACK)
    # Status legend pills (bagarte) at the top-right of the
    # also-list header: REPORTED green, CLAIM orange, ONGOING blue
    # (ONGOING is blue in bagarte, not the amber of the card-pill
    # table). Drawn right-to-left so they read REPORTED, CLAIM,
    # ONGOING left to right. The "16 MORE STORIES" count sits just
    # left of the pills.
    _px = 652
    for _lab, _fill in (("ONGOING", AZURE), ("CLAIM", TANGERINE),
                        ("REPORTED", LEAF)):
        _tw = int(d.textlength(_lab, font=TY.tag))
        _pw = _tw + 12
        _x0 = _px - _pw
        d.rounded_rectangle((_x0, MY - 1, _px, MY + 13), radius=2,
                            fill=_fill)
        txt(d, (_x0 + _pw / 2, MY + 6), _lab, TY.tag, "white",
            anchor="mm")
        _px = _x0 - 6
    txt(d, (_px - 6, MY), "16 MORE STORIES", TY.sect, BLACK,
        anchor="ra")
    seg(d, [(MX, MY + 16), (652, MY + 16)], BLACK, 1)
    col_w, col_gap, pitch = 200, 20, 24
    for i, (num, city, line, src) in enumerate(ALSO):
        if num <= 19:
            col_i, row = 0, num - 14
        elif num <= 24:
            col_i, row = 1, num - 20
        else:
            col_i, row = 2, num - 25
        x = MX + col_i * (col_w + col_gap)
        y = MY + 18 + row * pitch
        txt(d, (x, y), "%d." % num, TY.alsonum,
            REGION_COLOUR[ALSO_REGION[num]])
        # Bagarte gives each also item a small flag of its country
        # before the text; the text stays on one line. The source
        # moved to the sub-line below (bagarte).
        flag(d, FLAG_OF[num], x + 20, y, 16, 11)
        full = "%s: %s" % (city, line)
        lines = wrap(d, full, TY.also10, col_w - 40, 1)
        txt(d, (x + 40, y), lines[0] if lines else "", TY.also10,
            BLACK)
        sub = "%s · %s" % (ALSO_SUB[num], src)
        txt(d, (x + 40, y + 11), sub, TY.alsosub7, ASH)
    map_x, map_w, map_h = 680, 332, 148
    # WHERE IT HAPPENED now sits INSIDE the map panel (bagarte):
    # the map box spans MY..MY+170, the label at the top inside
    # it, and the dotted map fills the lower part (MY+22..).
    box(d, map_x, MY, map_x + map_w, MY + 170, SEA)
    d.rectangle((map_x, MY, map_x + map_w, MY + 170), outline=EDGE,
                width=1)
    draw_map(d, map_x, MY + 22, map_w, map_h)
    txt(d, (map_x + 8, MY + 8), "WHERE IT HAPPENED", TY.sect, BLACK)
    txt(d, (RX - 8, MY + 8), "pins = story numbers", TY.src, ASH,
        anchor="ra")
    # ---- date check 942-992: a strong red box (bagarte) — the
    # DATE CHECK label in a solid red box with white bold text,
    # the lead sentence in larger bold black, the "Left out" and
    # "Not yet confirmed" lead-ins and every date in bold red.
    # Lines are 14px apart so the 12px bold text never overlaps.
    d.rectangle((MX, CY, RX, CY + 50), outline=SCARLET, width=2)
    d.rectangle((20, CY + 3, 115, CY + 17), fill=SCARLET)
    txt(d, (67, CY + 10), "DATE CHECK", TY.src, "white", anchor="mm")
    draw_segs(d, 123, CY + 4, [
        ("Every story here happened or was first reported on "
         "Monday 23 November 2026 (UTC). ", BLACK),
        ("Left out because they happened on an earlier day:",
         SCARLET),
    ], TY.chk)
    draw_segs(d, 20, CY + 18, [
        ("'Chapo Isidro' ", BLACK), ("20–21 Nov", SCARLET),
        (" · Liverpool–Man Utd, Verstappen GP, Dymer hit, "
         "India 720/9, Seoul minister — all ", BLACK),
        ("Sun 22 Nov", SCARLET), (" · FBI breach ", BLACK),
        ("Fri 20 Nov", SCARLET), (".", BLACK),
    ], TY.chk)
    draw_segs(d, 20, CY + 32, [
        ("Not yet confirmed: ", SCARLET),
        ("Iran's radar/drone claims · Cikande missing count.",
         BLACK),
    ], TY.chk)
    # ---- footer 992-1018: a centred sources line, then the HOW
    # SURE legend as one line. ----
    txt(d, (512, FY),
        "Sources: Reuters · AP · AFP · SCMP · Al Jazeera · BBC · "
        "Guardian · Detik · Xinhua · IANS · Yonhap · ABC · ESPN · "
        "UKMTO · WHO · Corrections: none", TY.foot, ASH, anchor="ma")
    hx = 20 + int(d.textlength("HOW SURE: ", font=TY.foot))
    txt(d, (20, FY + 11), "HOW SURE: ", TY.foot, SCARLET)
    txt(d, (hx, FY + 11),
        "REPORTED = carried by the day's wires or officials · CLAIM "
        "= one side's account, labelled as such · ONGOING = still "
        "unfolding · Scenes are drawn illustrations, not photographs.",
        TY.foot, BLACK)
    return img


def main():
    img = build()
    out_path = os.path.join(HERE, "entry.png")
    img.save(out_path)
    print("saved", out_path, os.path.getsize(out_path), "bytes")
    if ISSUES:
        print("ISSUES:")
        for problem in ISSUES:
            print(" -", problem)
    else:
        print("no truncation")


if __name__ == "__main__":
    main()
