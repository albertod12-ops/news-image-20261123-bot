#!/usr/bin/env python3
"""Front page for Monday 23 November 2026 — v3.

Rebuilt on the sum-22 top-1 (bagarte, final #1) layout, exactly:
oversized serif date masthead with a "THE WORLD IN ONE DAY" strip,
red italic kicker, coloured region bar, single-line UTC timeline,
three numbered hero stories beside a dark-navy THE DAY IN NUMBERS
box (six big figures), ten small stories in two rows of five with
big-number anchors (pandya's device), an ALSO list and a dotted
world map, a red DATE CHECK box, and a HOW SURE footer.

Renders entry.png (1024x1024, byte-stable) from world.geo.json.
Usage: python3 draw.py

All 29 items happened, or were first reported, on Monday 23
November 2026, checked live against the wires (Reuters, AP, AFP,
BBC, Al Jazeera, Guardian, Detik, Xinhua, IANS, Yonhap, ABC,
ESPN, UKMTO, WHO and others). Stories that belong to an earlier
day are named in DATE CHECK, not drawn. The pictures are flat
vector shapes drawn here, the words are written here; nothing is
photographed, pasted, or copied in.

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
SEA = (198, 226, 240)
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
    mast = _load("LiberationSerif-Bold.ttf", 120, LIBER)
    kick = _load("NotoSans-Black.ttf", 10, NOTO)
    kicksm = _load("NotoSans-Bold.ttf", 10, NOTO)
    deck = _load("NotoSerif-Italic.ttf", 17, NOTO)
    clock = _load("NotoSans-Bold.ttf", 12, NOTO)
    clocksm = _load("NotoSans-Bold.ttf", 11, NOTO)
    tl = _load("NotoSans-Bold.ttf", 11, NOTO)
    tlev = _load("NotoSans-Regular.ttf", 11, NOTO)
    strip = _load("NotoSans-Bold.ttf", 10, NOTO)
    stripsm = _load("NotoSans-Bold.ttf", 9, NOTO)
    striptn = _load("NotoSans-Bold.ttf", 8, NOTO)
    tag = _load("NotoSans-Bold.ttf", 8, NOTO)
    src = _load("NotoSans-Bold.ttf", 9, NOTO)
    hhead = _load("LiberationSerif-Bold.ttf", 23, LIBER)
    shead = _load("LiberationSerif-Bold.ttf", 15, LIBER)
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
    slab = _load("NotoSans-Black.ttf", 12, NOTO)
    slabssm = _load("NotoSans-Bold.ttf", 8, NOTO)
    also = _load("NotoSans-Bold.ttf", 11, NOTO)
    alsonum = _load("NotoSans-Bold.ttf", 11, NOTO)
    sect = _load("NotoSans-Black.ttf", 13, NOTO)
    chk = _load("NotoSans-Bold.ttf", 11, NOTO)
    foot = _load("NotoSans-Bold.ttf", 10, NOTO)
    numbig = _load("NotoSans-Black.ttf", 26, NOTO)
    numlab = _load("NotoSans-Bold.ttf", 10, NOTO)
    numtitle = _load("NotoSans-Black.ttf", 12, NOTO)
    topic = _load("NotoSans-Black.ttf", 11, NOTO)
    topicsm = _load("NotoSans-Black.ttf", 9, NOTO)
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
CY = 956          # date-check top
FY = 992          # footer top

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
     "BREAK THE BLOCKADE", "25 TANKERS HIT", "gulfwar", "REPORTED"),
    (3, "WASHINGTON", "POLITICS", "AP · REUTERS", "REPORTED",
     "Democrats win 258 House seats",
     "Hubbard flips a North Carolina seat on recount; largest "
     "Democratic majority since 1992.",
     "258 SEATS", "BIGGEST SINCE 1992", "house258", "REPORTED"),
    (4, "SANTA CLARA", "TECH", "REUTERS · AP", "REPORTED",
     "Nvidia brings back Huang; shares jump 31%",
     "Huang returns as CEO 11 days after resigning.",
     "+31%", "HUANG RETURNS", "shares", "REPORTED"),
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
     "Gomez to quit Congress after ethics report",
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

# Also-list: (no, city, one line, outlet). Each line is sized to fit a
# 310px column (288px of text) at 11px bold. All 16 are Monday stories.
ALSO = [
    (14, "Antalya", "COP31 chief blames EU", "REUTERS"),
    (15, "New York", "Global stocks soar on Nvidia's return", "AP"),
    (16, "Tehran", "Singer Parastoo Ahmadi gets 74 lashes", "AP"),
    (17, "Washington", "Trump blasts Newsom", "AP"),
    (18, "Kyiv", "Zelensky urges four-way peace talks", "REUTERS"),
    (19, "Manchester", "Thousands flee concert scare", "AP"),
    (20, "US", "Storms threaten Thanksgiving travel", "AP"),
    (21, "Washington", "Democrats plan 12 debates", "AP"),
    (22, "Dhaka", "Hasina plans return from exile", "REUTERS"),
    (23, "Canberra", "Albanese defends Bowen", "AP"),
    (24, "Juba", "SPLA-IO attack leaves 24 civilians dead", "AP"),
    (25, "Congo", "Fighting disrupts Ebola response", "REUTERS"),
    (26, "Lisbon", "March over living costs", "REUTERS"),
    (27, "Myanmar", "ASEAN decision 'unfair'", "REUTERS"),
    (28, "Warsaw", "Russia 'tried twice to kill rapper'", "AP"),
    (29, "Brussels", "EU keeps €100bn for Ukraine", "REUTERS"),
]

# Six numbers for the dark-navy box — one big figure per top story.
STATS = [
    ("258", "House seats clinched"),
    ("+31%", "Nvidia shares jump"),
    ("24", "dead in Cikande fire"),
    ("7", "drones sank Merkury"),
    ("25", "tankers hit in a week"),
    ("2 DAYS", "COP31 overtime"),
]

# Region tallies, counted from the 29 items by subject:
# EUROPE 6 (8, 18, 19, 26, 28, 29); MIDDLE EAST 2 (2, 16);
# AFRICA 4 (7, 13, 24, 25); ASIA-PACIFIC 5 (5, 6, 12, 22, 27);
# AMERICAS 7 (3, 4, 9, 11, 17, 20, 21); OCEANIA 1 (23);
# WORLD 4 (1, 10, 14, 15). 6+2+4+5+7+1+4 = 29.
REGIONS = [
    ("EUROPE", 6, (16, 62, 150), "white"),
    ("MIDDLE EAST", 2, (200, 60, 30), "white"),
    ("AFRICA", 4, (30, 130, 80), "white"),
    ("ASIA-PACIFIC", 5, (90, 60, 140), "white"),
    ("AMERICAS", 7, (16, 40, 90), "white"),
    ("OCEANIA", 1, (0, 120, 180), "white"),
    ("WORLD", 4, (90, 90, 90), "white"),
]

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
        box(d, 0, 0, w, h, (11, 110, 110))
        disc(d, 51, 53, 31, (30, 120, 200), outline=(20, 20, 20), width=2)
        for a, b, c, e in ((30, 34, 52, 48), (52, 50, 74, 66),
                           (30, 54, 44, 66)):
            d.ellipse((a, b, c, e), fill=(60, 180, 90))
        seg(d, [(22, 53), (80, 53)], "white", 1)
        box(d, 132, 14, 142, 62, "white")
        d.rectangle((132, 14, 142, 62), outline=(20, 20, 20))
        box(d, 134, 16, 140, 62, (220, 30, 40))
        disc(d, 137, 66, 11, (220, 30, 40), outline=(20, 20, 20), width=2)
        for ty in (20, 28, 36, 44, 52):
            seg(d, [(142, ty), (147, ty)], (20, 20, 20))
        txt(d, (154, 16), "+1.5°C", TY.amid, "white")
        txt(d, (154, 38), "LIMIT", TY.amidsm, "white")
        txt(d, (154, 50), "PASSED", TY.amidsm, "white")
        box(d, 228, 22, 256, 78, "white")
        d.rectangle((228, 22, 256, 78), outline=(20, 20, 20), width=2)
        for ly in (32, 42, 52):
            seg(d, [(236, ly), (248, ly)], (60, 60, 60), 2)
        seg(d, [(228, 22), (222, 40), (230, 56), (224, 78)], SCARLET, 3)
        txt(d, (212, 64), "NO", TY.amidsm, SCARLET, anchor="ma")
        box(d, 150, 80, 262, 102, WINE)
        txt(d, (206, 91), "NO DEAL", TY.amid, "white", anchor="mm")
    elif key == "gulfwar":
        # Lead 2: the Gulf at war, as a map. Iran coast on top,
        # Arabian coast below, Bahrain with two base bursts, dashed
        # missile arcs, a burning tanker, a 5th Fleet destroyer.
        box(d, 0, 0, w, h, (14, 48, 96))
        poly(d, [(0, 0), (w, 0), (w, 14), (240, 16), (180, 12),
                 (120, 16), (60, 14), (0, 18)], (214, 196, 150))
        txt(d, (14, 4), "IRAN", TY.amidsm, BLACK)
        poly(d, [(0, h), (0, 82), (70, 74), (140, 82), (210, 76),
                 (260, 82), (w, 72), (w, h)], (214, 196, 150))
        txt(d, (w - 8, 90), "SAUDI ARABIA", TY.amidsm, BLACK, anchor="ra")
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
    elif key == "house258":
        # Lead 3: the US House flips. Navy hall, white Capitol dome
        # with columns and a gold cupola, seat bar bottom-right:
        # 258 blue against 177 red.
        box(d, 0, 0, w, h, MIDNIGHT)
        for sx, sy in ((22, 30), (70, 30), (210, 30), (280, 30),
                       (340, 30), (378, 30)):
            disc(d, sx, sy, 1, "white")
        d.ellipse((99, 20, 195, 68), fill="white")
        box(d, 97, 48, 197, 66, "white")
        for cx in (112, 132, 152, 172, 192):
            seg(d, [(cx, 48), (cx, 66)], MIDNIGHT, 2)
        box(d, 87, 66, 207, 70, "white")
        box(d, 123, 12, 171, 26, "white")
        disc(d, 147, 11, 12, GILT)
        box(d, 130, 82, 207, 96, (40, 90, 200))
        box(d, 207, 82, 284, 96, (200, 40, 50))
        txt(d, (168, 89), "258", TY.amidsm, "white", anchor="mm")
        txt(d, (245, 89), "177", TY.amidsm, "white", anchor="mm")
        txt(d, (10, 8), "THE HOUSE", TY.amidsm, GILT)
        txt(d, (284, 8), "SINCE 1992", TY.amidsm, GILT, anchor="ra")
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
        d.ellipse((60, 20, 70, 26), fill=(90, 95, 105))
        seg(d, [(52, 18), (68, 18)], (200, 200, 210), 2)
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
    elif key == "shares":
        # Nvidia shares jump on Huang's return: dark board, a steep
        # rising chart line, green arrow, the gain as the picture.
        box(d, 0, 0, w, h, (16, 24, 44))
        for gy in range(14, h, 12):
            seg(d, [(0, gy), (w, gy)], (30, 40, 60))
        for gx in range(14, w, 18):
            seg(d, [(gx, 0), (gx, h)], (30, 40, 60))
        pts = [(10, 66), (40, 60), (70, 64), (100, 46), (130, 50),
               (160, 28), (186, 16)]
        for i in range(len(pts) - 1):
            seg(d, [pts[i], pts[i + 1]], (60, 200, 90), 3)
        for px, py in pts:
            disc(d, px, py, 3, (60, 200, 90))
        poly(d, [(186, 16), (176, 14), (176, 22)], (60, 200, 90))
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
        box(d, 30, 22, 90, 60, (90, 60, 40))
        d.rectangle((30, 22, 90, 60), outline=(60, 40, 20), width=2)
        disc(d, 78, 41, 4, GILT)
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
        poly(d, [(92, 20), (104, 20), (108, 48), (88, 48)], "white")
        poly(d, [(98, 8), (104, 20), (92, 20)], SCARLET)
        poly(d, [(88, 48), (80, 60), (88, 54)], (200, 200, 210))
        poly(d, [(108, 48), (116, 60), (108, 54)], (200, 200, 210))
        burst(d, 98, 62, 8, 3, (255, 180, 60))
        ring(d, 140, 30, 180, 62, GILT, 2)
        disc(d, 160, 46, 6, GILT)
        txt(d, (160, 46), "24", TY.slabssm, BLACK, anchor="mm")
    elif key == "handshake":
        # Kenya and DR Congo restore ties: two flags on poles, two
        # hands meeting in the middle.
        box(d, 0, 0, w, h, (200, 220, 235))
        box(d, 0, 58, w, h, (90, 90, 98))
        for fx, cols in ((20, ((0, 0, 0), (200, 30, 40), (0, 130, 60))),
                         (150, ((0, 60, 160), (255, 210, 31), (200, 30, 40)))):
            seg(d, [(fx, 22), (fx, 58)], (60, 60, 60), 2)
            box(d, fx, 22, fx + 24, 30, cols[0])
            box(d, fx, 30, fx + 24, 38, cols[1])
            box(d, fx, 38, fx + 24, 46, cols[2])
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


def topbar(d, x, y, w, num, place, vtag):
    """Bagarte's number+place bar across the top of a picture:
    dark strip, circled number left, place in caps, status pill
    right. Text shrinks until it fits."""
    box(d, x, y, x + w, y + 18, (10, 10, 14))
    disc(d, x + 11, y + 9, 7, "white")
    txt(d, (x + 11, y + 9), str(num), TY.tag, BLACK, anchor="mm")
    label = "%s" % place
    fb = TY.slab
    while d.textlength(label, font=fb) > w - 52 and fb.size > 8:
        fb = ImageFont.truetype(
            os.path.join(NOTO, "NotoSans-Black.ttf"), fb.size - 1)
    txt(d, (x + 22, y + 9), label, fb, "white", anchor="lm")
    pw = int(d.textlength(vtag, font=TY.tag)) + 10
    d.rounded_rectangle((x + w - 4 - pw, y + 3, x + w - 4, y + 15),
                        radius=2, fill=PILL[vtag])
    txt(d, (x + w + 1 - pw, y + 9), vtag, TY.tag, "white", anchor="lm")


def hero_card(img, d, story, x, y, w):
    """A lead card, 252 tall (bagarte): 105px art with a number+place
    bar and a status pill, a topic line, a 2–3 line 23px serif
    headline, a 2–3 line 12px serif deck, and a 9px source line,
    all inside a 1px ink box."""
    num, place, topic, src, _st, head, deck, big, small, key, vtag = story
    box(d, x, y, x + w, y + HH, PANEL)
    pic = heropic(key, w)
    img.paste(pic, (x, y))
    d2 = ImageDraw.Draw(img)
    topbar(d2, x, y, w, num, place, vtag)
    ty = y + HA + 6
    txt(d, (x + 8, ty), topic, TY.topic, BLACK)
    hl = wrap(d, head, TY.hhead, w - 16, 3)
    dl = wrap(d, deck, TY.hdeck, w - 16, 3)
    hy = ty + 16
    for j, ln in enumerate(hl):
        txt(d, (x + 8, hy + j * 26), ln, TY.hhead, BLACK)
    dy = hy + len(hl) * 26 + 2
    for j, ln in enumerate(dl):
        txt(d, (x + 8, dy + j * 14), ln, TY.hdeck, (60, 60, 60))
    txt(d, (x + 8, y + HH - 14), src, TY.src, ASH)
    d.rectangle((x, y, x + w, y + HH), outline=BLACK, width=1)


def small_card(img, d, story, x, y):
    """A small card, 146 tall (bagarte + pandya): 60px art with a
    number+place bar, a status pill, and a big-number badge (the
    story's big label, white on black, centred in the art), a topic
    line, a 2-line 15px serif headline and a 2-line 11px serif deck
    with its source, inside a 1px ink box."""
    num, place, topic, src, _st, head, deck, big, small, key, vtag = story
    w = SW
    box(d, x, y, x + w, y + SH, PANEL)
    pic = minipic(key)
    img.paste(pic, (x, y))
    d2 = ImageDraw.Draw(img)
    topbar(d2, x, y, w, num, place, vtag)
    # big-number badge, centred in the art below the top bar
    fb = TY.bignum
    while d.textlength(big, font=fb) > w - 24 and fb.size > 14:
        fb = ImageFont.truetype(
            os.path.join(NOTO, "NotoSans-Black.ttf"), fb.size - 1)
    bw = int(d.textlength(big, font=fb)) + 16
    bx0 = x + (w - bw) // 2
    by0 = y + 24
    d2.rounded_rectangle((bx0, by0, bx0 + bw, by0 + 30), radius=3,
                         fill=(10, 10, 14))
    txt(d2, (bx0 + bw // 2, by0 + 15), big, fb, "white", anchor="mm")
    ty = y + SA + 5
    txt(d, (x + 8, ty), topic, TY.topicsm, BLACK)
    hl = wrap(d, head, TY.shead, w - 16, 2)
    for j, ln in enumerate(hl):
        txt(d, (x + 8, ty + 14 + j * 17), ln, TY.shead, BLACK)
    dl = wrap(d, deck + " — " + src, TY.sdeck, w - 16, 2)
    for j, ln in enumerate(dl):
        txt(d, (x + 8, ty + 15 + len(hl) * 17 + j * 12), ln,
            TY.sdeck, (60, 60, 60))
    d.rectangle((x, y, x + w, y + SH), outline=BLACK, width=1)


def numbers_box(d, x, y):
    """Bagarte's dark-navy THE DAY IN NUMBERS box: title plus six
    big figures, each a 26px number over a 10px label."""
    box(d, x, y, x + NW, y + HH, MIDNIGHT)
    txt(d, (x + 10, y + 8), "THE DAY IN NUMBERS", TY.numtitle, "white")
    seg(d, [(x + 10, y + 26), (x + NW - 10, y + 26)], (80, 100, 140), 1)
    ey = y + 34
    for value, label in STATS:
        fv = TY.numbig
        while d.textlength(value, font=fv) > NW - 20 and fv.size > 18:
            fv = ImageFont.truetype(
                os.path.join(NOTO, "NotoSans-Black.ttf"), fv.size - 1)
        txt(d, (x + 10, ey), value, fv, "white")
        txt(d, (x + 10, ey + 28), label, TY.numlab, (200, 210, 230))
        ey += 38
    d.rectangle((x, y, x + NW, y + HH), outline=BLACK, width=1)


def _inside(lon, lat, polys):
    """Ray-casting point-in-polygon for one lon/lat against a list
    of rings (each a list of (lon, lat))."""
    for ring in polys:
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
            polys.append(poly_ring[0])

    def px(lon):
        return x0 + (lon + 180.0) / 360.0 * w

    def py(lat):
        return y0 + (90.0 - lat) / 180.0 * h

    box(d, x0, y0, x0 + w, y0 + h, SEA)
    # dotted land: 3px grid, 1.5px dots where inside a land polygon
    step = 3
    for gy in range(2, h, step):
        lat = 90.0 - (gy / h) * 180.0
        for gx in range(2, w, step):
            lon = (gx / w) * 360.0 - 180.0
            if _inside(lon, lat, polys):
                disc(d, x0 + gx, y0 + gy, 1.5, (50, 50, 50))
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
            seg(d, [(tx, ty), (tx + ox, ty + oy)], SCARLET, 1)
        cx, cy = tx + ox, ty + oy
        disc(d, cx, cy, 7, SCARLET, outline="white", width=1)
        fp = TY.pin if num < 10 else TY.pinsm
        txt(d, (cx, cy), str(num), fp, "white", anchor="mm")

def build():
    img, d = fresh(W, H)
    box(d, 0, 0, W - 1, H - 1, BG)
    # ---- top strip 0-14: the paper's name left, the count right. ----
    txt(d, (MX, 7), "THE WORLD IN ONE DAY", TY.kick, BLACK)
    txt(d, (RX, 7),
        "29 STORIES · 7 REGIONS · ALL FROM THIS ONE DAY", TY.kick,
        BLACK, anchor="ra")
    # ---- masthead 16-128: the date at 120px on its own layer,
    # squeezed horizontally to 996px so its ink top sits at 19
    # (ink 19-127, 109px tall). ----
    title = "Monday 23 November 2026"
    lw = int(d.textlength(title, font=TY.mast)) + 8
    layer = Image.new("RGBA", (lw, 150), (0, 0, 0, 0))
    lt = ImageDraw.Draw(layer)
    lt.text((4, 0), title, font=TY.mast, fill=BLACK + (255,))
    ink_top = layer.getbbox()[1]
    layer = layer.resize((996, 150), Image.LANCZOS)
    img.paste(layer, (MX, 19 - ink_top), layer)
    # ---- red kicker 130-148: the three leads, italic serif. ----
    txt(d, (MX, 130),
        "COP31 ends without a climate pact · Iran vows to break the "
        "blockade · Democrats win 258 seats", TY.deck, SCARLET)
    # ---- region bar 150-164: seven equal segments, count after
    # the name, white 9px bold centred in each segment. ----
    bx, by, bw, bh = MX, 150, 1000, 14
    segw = bw / len(REGIONS)
    for i, (label, count, fill, ink) in enumerate(REGIONS):
        sx = bx + i * segw
        box(d, sx, by, sx + segw - 1, by + bh, fill)
        txt(d, (sx + segw / 2, by + 7), "%s %d" % (label, count),
            TY.src, ink, anchor="mm")
    # ---- UTC timeline 168-192: a black UTC box at the left, then
    # six time+event pairs in one line (red bold time, black event),
    # separated by middots. ----
    tl_y = 168
    box(d, MX, tl_y, 58, tl_y + 20, BLACK)
    txt(d, (35, tl_y + 10), "UTC", TY.src, "white", anchor="mm")
    timeline = [("05:30", "Modi meets Shah"),
                ("06:00", "COP31 ends, no deal"),
                ("09:00", "Iran vows blockade break"),
                ("11:00", "Cikande toll at 24"),
                ("14:30", "Huang reinstated"),
                ("19:00", "Democrats clinch 258")]
    tx = 66
    for i, (tt, ev) in enumerate(timeline):
        txt(d, (tx, tl_y + 10), tt, TY.tl, SCARLET, anchor="lm")
        tx += int(d.textlength(tt, font=TY.tl)) + 4
        txt(d, (tx, tl_y + 10), ev, TY.tlev, BLACK, anchor="lm")
        tx += int(d.textlength(ev, font=TY.tlev))
        if i < len(timeline) - 1:
            txt(d, (tx, tl_y + 10), "  ·  ", TY.tl, ASH, anchor="lm")
            tx += int(d.textlength("  ·  ", font=TY.tl))
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
    # ---- also-list (left) + map (right) 768-948. ----
    txt(d, (MX, MY), "ALSO ON MONDAY 23 NOVEMBER", TY.sect, BLACK)
    txt(d, (652, MY), "16 MORE STORIES", TY.sect, BLACK, anchor="ra")
    seg(d, [(MX, MY + 16), (652, MY + 16)], BLACK, 1)
    col_w, rows = 310, 8
    for i, (num, city, line, src) in enumerate(ALSO):
        col_i = 0 if i < rows else 1
        row = i if i < rows else i - rows
        x = MX + col_i * (col_w + 18)
        y = MY + 22 + row * 13
        txt(d, (x, y), "%d." % num, TY.alsonum, SCARLET)
        full = "%s: %s (%s)" % (city, line, src)
        lines = wrap(d, full, TY.also, col_w - 22, 1)
        txt(d, (x + 20, y), lines[0] if lines else "", TY.also, BLACK)
    map_x, map_w, map_h = 680, 332, 148
    txt(d, (map_x, MY), "WHERE IT HAPPENED", TY.sect, BLACK)
    txt(d, (RX, MY), "pins = story numbers", TY.src, ASH, anchor="ra")
    seg(d, [(map_x, MY + 16), (RX, MY + 16)], BLACK, 1)
    box(d, map_x, MY + 22, map_x + map_w, MY + 22 + map_h, SEA)
    d.rectangle((map_x, MY + 22, map_x + map_w, MY + 22 + map_h),
                outline=EDGE, width=1)
    draw_map(d, map_x, MY + 22, map_w, map_h)
    # ---- date check 956-986: the red box naming the big stories
    # deliberately left out because they are not Monday, and what
    # is not yet confirmed. ----
    d.rectangle((MX, CY, RX, CY + 30), outline=SCARLET, width=2)
    chk = ("DATE CHECK — Every story here happened or was first "
           "reported on Monday 23 November 2026 (UTC). Left out "
           "(earlier day): 'Chapo Isidro' 20–21 Nov · Liverpool–Man "
           "Utd, Verstappen GP, Dymer hit, India 720/9, Seoul "
           "minister — all Sun 22 Nov · FBI breach Fri 20 Nov. Not "
           "yet confirmed: Iran's radar/drone claims · Cikande "
           "missing count.")
    chk_lines = wrap(d, chk, TY.chk, 976, 2)
    for j, ln in enumerate(chk_lines):
        txt(d, (20, CY + 4 + j * 11), ln, TY.chk, BLACK)
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
