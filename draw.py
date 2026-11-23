#!/usr/bin/env python3
"""Front page for Monday 23 November 2026.

Renders entry.png (1024x1024, byte-stable) from world.geo.json.
Usage: python3 draw.py

A broadsheet: oversized serif date masthead, red deck, numbers strip,
region bar, UTC timeline, three lead stories, fifteen small cards in
three rows of five, a light world map next to an 18-item also-list, a
red date-check box, and a sources footer with a verification legend.

All 36 items happened, or were first reported, on Monday 23 November
2026, checked live against the wires (Reuters, AP, AFP, BBC, Al
Jazeera, Guardian, Detik, Xinhua, IANS, Yonhap, ABC and others). The
pictures are flat vector shapes drawn here, the words are written here;
nothing is photographed, pasted, or copied in.

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

PILL = {
    "CONFIRMED": LEAF,
    "REPORTED": LEAF,
    "FORECAST": AZURE,
    "CLAIM": TANGERINE,
    "OFFICIAL": TEAL,
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
    kick = _load("NotoSans-Black.ttf", 15, NOTO)
    deck = _load("NotoSerif-Italic.ttf", 17, NOTO)
    clock = _load("NotoSans-Bold.ttf", 12, NOTO)
    clocksm = _load("NotoSans-Bold.ttf", 10, NOTO)
    strip = _load("NotoSans-Bold.ttf", 10, NOTO)
    stripsm = _load("NotoSans-Bold.ttf", 9, NOTO)
    striptn = _load("NotoSans-Bold.ttf", 8, NOTO)
    tag = _load("NotoSans-Bold.ttf", 8, NOTO)
    src = _load("NotoSans-Bold.ttf", 9, NOTO)
    hhead = _load("LiberationSerif-Bold.ttf", 27, LIBER)
    shead = _load("LiberationSerif-Bold.ttf", 16, LIBER)
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


# --- layout ----------------------------------------------------------------
MX = 12
RX = 1012
HY = 205
HA = 100
HK = 14
HT = 88
HH = HA + HK + HT
SY = 415
SR = 126
SA = 48
SK = 14
SH = SA + 76
MY = 801
MW, MH = 336, 140
CY = 969
FY = 999

ISSUES = []

# --- the 36 stories --------------------------------------------------------
# Drawn item: (no, place, topic, source, status, headline, deck,
# art big label, art small label, art key, pill).
# Headlines at most two lines (27px lead, 16px small); decks at most
# two lines (12px lead, 11px small, deck + " — source" on smalls).
# CONFIRMED = two named sources agree; REPORTED = one named source;
# CLAIM = one side's claim, unverified.
FRONT = [
    (1, "ANTALYA", "CLIMATE", "REUTERS · BBC", "REPORTED",
     "Climate talks collapse with no deal",
     "Turkiye's final draft drops fossil fuels; talks end with no overarching agreement. 1.5°C overshoot admitted.",
     "NO DEAL", "FOSSIL FUELS CUT", "copcollapse", "CONFIRMED"),
    (2, "THE GULF", "WAR", "UKMTO · IRGC · AP", "REPORTED",
     "Missiles rain on the Gulf as war widens",
     "Iran hits a US base in Bahrain, Houthis fire on Saudi Arabia, two tankers struck in the Strait of Hormuz.",
     "2 TANKERS HIT", "BASE STRUCK", "gulfwar", "CONFIRMED"),
    (3, "WASHINGTON", "POLITICS", "AP · REUTERS", "REPORTED",
     "Democrats sweep the House",
     "At least 258 seats clinched — the largest Democratic majority in 34 years. A check on the Trump era.",
     "258 SEATS", "BIGGEST SINCE 1992", "house258", "CONFIRMED"),
    (4, "GULF OF FINLAND", "SEA", "REUTERS", "REPORTED",
     "Russian cargo ship Sparta II still burning",
     "Hit by drones Saturday; fire rages off Finland, 16 crew safe.",
     "SHIP ABLAZE", "16 CREW SAFE", "shipfire", "CONFIRMED"),
    (5, "LIBYA", "WAR", "REUTERS · AP", "REPORTED",
     "Russian warship sunk in Libya by drone",
     "A second Russian vessel was struck in the same attack.",
     "WARSHIP SUNK", "DRONE STRIKE", "sinking", "REPORTED"),
    (6, "CIKANDE", "FIRE", "DETIK", "REPORTED",
     "Factory fire toll climbs in Cikande",
     "Seven bodies found, 50 workers missing in Banten.",
     "7 DEAD, 50 MISSING", "BANTEN PLANT", "factoryfire", "REPORTED"),
    (7, "SINALOA", "CRIME", "REUTERS", "REPORTED",
     "Mexico arrests 'Chapo Isidro' in Sinaloa raid",
     "Alleged kingpin held in a major Sinaloa operation.",
     "KINGPIN HELD", "SINALOA RAID", "arrest", "CONFIRMED"),
    (8, "SEOUL", "POLITICS", "REUTERS", "REPORTED",
     "Minister quits over AI exam cheating",
     "Education minister resigns in an AI cheating scandal.",
     "EXAM CHEATING", "SEOUL", "exam", "CONFIRMED"),
    (9, "NEW DELHI", "DIPLOMACY", "IANS", "REPORTED",
     "Nepal PM Shah holds talks with Modi",
     "First foreign trip: state visit, meets Modi Monday.",
     "STATE VISIT", "NEW DELHI", "statevisit", "CONFIRMED"),
    (10, "WELLINGTON", "CRICKET", "REUTERS", "REPORTED",
     "India declare on 720/9, a record in New Zealand",
     "Rahul 136, Gill 98; hosts 119/2, trailing by 233.",
     "720/9 DECLARED", "INDIA'S RECORD", "cricket", "CONFIRMED"),
    (11, "WASHINGTON", "TECH", "REUTERS · AP", "REPORTED",
     "Nvidia pressed on chips diverted to China",
     "Bessent seeks answers on chips sent to China.",
     "CHIP PROBE", "CHINA DIVERSION", "chip", "REPORTED"),
    (12, "WASHINGTON", "CYBER", "AP", "REPORTED",
     "FBI probes apparent hack of its crime database",
     "Gun checks paused; Trump confirms the breach.",
     "FBI PROBE", "CRIME DATABASE", "servers", "REPORTED"),
    (13, "LIVERPOOL", "FOOTBALL", "REUTERS", "REPORTED",
     "Liverpool thrash 10-man Man Utd",
     "Pochettino's debut ends in a rout; United down to ten.",
     "ROUT AT ANFIELD", "POCHETTINO'S DEBUT", "football", "CONFIRMED"),
    (14, "LAS VEGAS", "FORMULA 1", "FIA · AP", "REPORTED",
     "Verstappen wins chaotic Las Vegas GP",
     "Wins from pole in the night race; Ferraris clash.",
     "VERSTAPPEN WINS", "LAS VEGAS GP", "f1night", "CONFIRMED"),
    (15, "KYIV REGION", "WAR", "REUTERS", "REPORTED",
     "14 missing after drone hits Kyiv-region block",
     "Drone hits a home; Zelenskiy: 14 unaccounted for.",
     "14 MISSING", "DRONE STRIKE", "drones", "REPORTED"),
    (16, "JUBA", "CONFLICT", "AP", "REPORTED",
     "SPLA-IO attack leaves 24 civilians dead",
     "24 civilians killed in the latest flare-up.",
     "24 CIVILIANS DEAD", "SOUTH SUDAN", "africa", "REPORTED"),
    (17, "CONGO", "HEALTH", "REUTERS", "REPORTED",
     "Fighting disrupts Ebola response",
     "WHO: battle hampers the Ebola effort.",
     "EBOLA RESPONSE HIT", "FIGHTING NEARBY", "ebola", "REPORTED"),
    (18, "LISBON", "PROTEST", "REUTERS", "REPORTED",
     "Thousands march in Lisbon over living costs",
     "Crowds fill the streets over rising prices.",
     "COST-OF-LIVING MARCH", "LISBON", "march", "CONFIRMED"),
]

# Also-list: (no, city, one line, outlet). Each line is sized to fit a
# 320px column (298px of text) at 11px bold. All 18 are Monday stories.
ALSO = [
    (19, "Los Angeles", "Miley Cyrus marries Maxx Morando", "AP"),
    (20, "Atlanta", "Delta delays after automation fault", "AP"),
    (21, "Myanmar", "ASEAN decision 'unfair'", "REUTERS"),
    (22, "Warsaw", "Russia 'tried twice to kill rapper'", "AP"),
    (23, "Brussels", "EU keeps €100bn for Ukraine", "REUTERS"),
    (24, "Denver", "Tom Jackson, Broncos star, dies at 75", "ESPN"),
    (25, "Hormuz", "Briton swims strait for the planet", "REUTERS"),
    (26, "Olympia", "Governor: ICE 'out of control'", "AP"),
    (27, "West Bank", "Eisenkot slams settler attacks", "REUTERS"),
    (28, "London", "May tells Burnham: accept Brexit", "BBC"),
    (29, "Riyadh", "Coalition intercepts Houthi missile", "REUTERS"),
    (30, "Gulf of Oman", "tanker in military incident", "UKMTO"),
    (31, "Islamabad", "Pakistan FM hopeful on US-Iran deal", "AP"),
    (32, "Dnipro", "Russian strikes kill 1, injure 9", "REUTERS"),
    (33, "Mumbai", "Tata Steel in ₹28,000cr Apollo deal", "REUTERS"),
    (34, "Itanagar", "Shah's ₹4,000cr Arunachal push", "IANS"),
    (35, "Goa", "IFFI hosts BRICS film roundtable", "IANS"),
    (36, "London", "NHS 'wasting billions'", "GUARDIAN"),
]

# Six numbers for the strip — one per lead story, all Monday.
STATS = [
    ("258", "House seats"),
    ("2", "tankers hit"),
    ("50", "factory missing"),
    ("24", "dead in South Sudan"),
    ("€100bn", "EU Ukraine fund"),
    ("14", "missing in Kyiv region"),
]

# Region tallies, counted from the 36 items by subject:
# EUROPE 9 (4, 13, 15, 18, 22, 23, 28, 32, 36); MIDDLE EAST 5
# (2, 25, 27, 29, 30); AFRICA 3 (5, 16, 17); ASIA-PACIFIC 8
# (6, 8, 9, 21, 31, 33, 34, 35); AMERICAS 9 (3, 7, 11, 12, 14, 19,
# 20, 24, 26); OCEANIA 1 (10, Wellington venue); WORLD 1 (1, COP31).
# 9+5+3+8+9+1+1 = 36.
REGIONS = [
    ("EUROPE", 9, (16, 62, 150), "white"),
    ("MIDDLE EAST", 5, (200, 60, 30), "white"),
    ("AFRICA", 3, (30, 130, 80), "white"),
    ("ASIA-PACIFIC", 8, (90, 60, 140), "white"),
    ("AMERICAS", 9, (16, 40, 90), "white"),
    ("OCEANIA", 1, (0, 120, 180), "white"),
    ("WORLD", 1, (90, 90, 90), "white"),
]

# --- the map ---------------------------------------------------------------
# Red numbered pins for the 18 drawn items; navy dots for the 18
# also-list lines. Values are (longitude, latitude).
PINS = {
    1: (30.7, 36.9), 2: (56.0, 26.5), 3: (-77.0, 38.9),
    4: (24.5, 59.9), 5: (13.2, 32.9), 6: (106.1, -6.0),
    7: (-107.4, 24.8), 8: (127.0, 37.5), 9: (77.2, 28.6),
    10: (174.8, -41.3), 11: (-77.0, 38.9), 12: (-77.0, 38.9),
    13: (-3.0, 53.4), 14: (-115.1, 36.2), 15: (30.5, 50.4),
    16: (31.6, 4.85), 17: (29.2, -1.7), 18: (-9.1, 38.7),
}
DOTS = {
    19: (-118.2, 34.0), 20: (-84.4, 33.7), 21: (96.2, 19.8),
    22: (21.0, 52.2), 23: (4.4, 50.8), 24: (-105.0, 39.7),
    25: (56.5, 26.6), 26: (-122.3, 47.6), 27: (35.2, 31.9),
    28: (-0.1, 51.5), 29: (46.7, 24.7), 30: (58.5, 24.0),
    31: (73.1, 33.7), 32: (35.0, 48.5), 33: (72.9, 19.1),
    34: (93.6, 27.1), 35: (74.1, 15.3), 36: (-0.1, 51.5),
}
# Map is 336x140 equirectangular. Markers that would collide are nudged
# a few pixels with a thin leader back to the true spot; Washington
# holds pins 3, 11, 12 in one spot, London holds dots 28 and 36.
PIN_OFF = {3: (-14, -10), 4: (12, -10), 10: (-8, 0),
           11: (12, 8), 12: (-2, 12), 13: (-24, -6), 14: (0, -12),
           15: (12, -2), 16: (-14, -8), 17: (-12, 8), 18: (-12, 6)}
DOT_OFF = {20: (-6, 10), 21: (10, 8), 22: (-10, -10), 23: (-16, 2),
           25: (-8, 10), 26: (-8, -6), 27: (8, 6), 28: (16, 0),
           29: (14, 10), 30: (12, 8), 31: (-10, -8), 32: (16, -12),
           33: (8, 8), 35: (10, 10), 36: (-14, -8)}


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


def banner(d, w, big, small, fill):
    """Solid bar across the top of a small picture, two white labels.
    Sizes step down until the pair fits."""
    box(d, 0, 0, w, 18, fill)
    fb, fs = TY.slab, TY.slabssm
    while (d.textlength(big, font=fb) + d.textlength(small, font=fs)
           + 14 > w):
        if fb.size > 9:
            fb = ImageFont.truetype(
                os.path.join(NOTO, "NotoSans-Black.ttf"), fb.size - 1)
        elif fs.size > 7:
            fs = ImageFont.truetype(
                os.path.join(NOTO, "NotoSans-Bold.ttf"), fs.size - 1)
        else:
            break
    txt(d, (6, 9), big, fb, "white", anchor="lm")
    txt(d, (w - 6, 9), small, fs, "white", anchor="rm")


def tag(d, w, h, big, small):
    """Bottom-left label block on a hero picture; big over small."""
    fb = TY.hlab
    while d.textlength(big, font=fb) > w - 16 and fb.size > 10:
        fb = ImageFont.truetype(
            os.path.join(NOTO, "NotoSans-Black.ttf"), fb.size - 1)
    bw = d.textlength(big, font=fb)
    sw = d.textlength(small, font=TY.hlabsm)
    bw2 = int(max(bw, sw)) + 16
    box(d, 0, h - 34, bw2, h, (10, 10, 14))
    txt(d, (8, h - 30), big, fb, "white")
    txt(d, (8, h - 15), small, TY.hlabsm, "white")


def art(key, w, h):
    """One picture, flat vector shapes drawn from scratch.
    Leads paint at h=105 then shrink to 100; smalls at h=80 then
    shrink to 48. A lead's bottom-left stays clear for its tag;
    a small's top 18px stays clear for its banner."""
    img, d = fresh(w, h)
    if key == "copcollapse":
        # Lead 1: the climate talks fail. Teal hall, round globe,
        # thermometer past the mark, a torn page, a NO DEAL band.
        box(d, 0, 0, w, h, (11, 110, 110))
        disc(d, 51, 53, 31, (30, 120, 200), outline=(20, 20, 20), width=2)
        for a, b, c, e in ((30, 34, 52, 48), (52, 50, 74, 66),
                           (30, 54, 44, 66)):
            d.ellipse((a, b, c, e), fill=(60, 180, 90))
        box(d, 132, 14, 142, 62, "white")
        d.rectangle((132, 14, 142, 62), outline=(20, 20, 20))
        box(d, 134, 16, 140, 62, (220, 30, 40))
        disc(d, 137, 66, 11, (220, 30, 40), outline=(20, 20, 20), width=2)
        for ty in (20, 28, 36, 44, 52):
            seg(d, [(142, ty), (147, ty)], (20, 20, 20))
        txt(d, (154, 16), "+1.5°C", TY.amid, "white")
        txt(d, (154, 38), "LIMIT", TY.amidsm, "white")
        txt(d, (154, 50), "PASSED", TY.amidsm, "white")
        box(d, 228, 22, 284, 78, "white")
        d.rectangle((228, 22, 284, 78), outline=(20, 20, 20), width=2)
        for ly in (32, 42, 52):
            seg(d, [(236, ly), (276, ly)], (60, 60, 60), 2)
        seg(d, [(256, 22), (250, 40), (258, 56), (252, 78)], SCARLET, 3)
        txt(d, (240, 64), "NO", TY.amidsm, SCARLET, anchor="ma")
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
        # burning tanker, right of the island
        poly(d, [(180, 60), (232, 60), (224, 68), (188, 68)], (30, 30, 40))
        box(d, 188, 48, 202, 60, "white")
        burst(d, 212, 44, 9, 4, (255, 140, 40))
        burst(d, 212, 44, 5, 2, (255, 210, 31))
        for lx, ly, s, anch in ((136, 56, "BAHRAIN", "ma"),
                                (208, 28, "THE GULF", "ma")):
            txt(d, (lx, ly), s, TY.amidsm, "white", anchor=anch,
                stroke=1, stroke_fill=(0, 0, 0))
        poly(d, [(228, 34), (276, 34), (268, 42), (236, 42)],
             (120, 125, 135))
        box(d, 242, 26, 254, 34, (120, 125, 135))
        seg(d, [(248, 26), (248, 20)], (120, 125, 135), 2)
        seg(d, [(224, 44), (280, 44)], "white")
        txt(d, (252, 50), "5TH FLEET", TY.amidsm, "white", anchor="ma",
            stroke=1, stroke_fill=(0, 0, 0))
    elif key == "house258":
        # Lead 3: the US House flips. Navy hall, white Capitol dome
        # with columns and a gold cupola, seat bar bottom-right:
        # 258 blue against 177 red.
        box(d, 0, 0, w, h, MIDNIGHT)
        for sx, sy in ((22, 10), (70, 16), (140, 8), (210, 14),
                       (280, 8), (340, 16), (378, 10)):
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
    elif key == "arrest":
        # 'Chapo Isidro' arrested: dusk desert road, gold badge,
        # steel cuffs on a chain, patrol car with flashing lights.
        box(d, 0, 0, w, h, (220, 160, 90))
        box(d, 0, 60, w, h, (120, 80, 50))
        seg(d, [(0, 60), (w, 60)], (60, 40, 20), 2)
        poly(d, [(98, 22), (118, 22), (114, 46), (98, 52), (82, 46)],
             GILT, outline=(120, 90, 0))
        burst(d, 100, 34, 8, 3, (255, 240, 180))
        for cx in (52, 148):
            ring(d, cx - 12, 44, cx + 12, 68, (220, 220, 230), 4)
            disc(d, cx, 56, 4, (220, 220, 230))
        seg(d, [(64, 56), (136, 56)], (220, 220, 230), 3)
        ring(d, 96, 50, 104, 58, (220, 220, 230), 2)
        box(d, 150, 62, 186, 72, (20, 20, 26))
        box(d, 158, 56, 178, 62, (20, 20, 26))
        disc(d, 167, 54, 3, SCARLET)
        disc(d, 175, 54, 3, (60, 120, 255))
    elif key == "exam":
        # Minister quits over AI exam cheating: desk, exam paper
        # with red crosses, pencil, robot head for the AI angle.
        box(d, 0, 0, w, h, (120, 90, 60))
        box(d, 0, 62, w, h, (90, 65, 40))
        poly(d, [(70, 24), (130, 28), (126, 62), (66, 58)], "white",
             outline=(60, 60, 60))
        for ly in (34, 42, 50):
            seg(d, [(76, ly), (120, ly + 2)], ASH)
        for xx, xy in ((112, 34), (100, 46)):
            seg(d, [(xx - 4, xy - 4), (xx + 4, xy + 4)], SCARLET, 2)
            seg(d, [(xx + 4, xy - 4), (xx - 4, xy + 4)], SCARLET, 2)
        poly(d, [(140, 66), (172, 62), (176, 66), (144, 70)],
             (255, 200, 40))
        poly(d, [(172, 62), (180, 64), (176, 66)], (240, 200, 180))
        box(d, 30, 26, 52, 44, (150, 160, 180))
        d.rectangle((30, 26, 52, 44), outline=(60, 60, 70))
        disc(d, 38, 34, 2, (40, 200, 90))
        disc(d, 46, 34, 2, (40, 200, 90))
        seg(d, [(41, 26), (41, 20)], (60, 60, 70), 2)
        disc(d, 41, 20, 3, SCARLET)
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
    elif key == "cricket":
        # India declare on 720/9 in Wellington: stands and lights,
        # green outfield, tan pitch, stumps, batsman mid-swing,
        # scoreboard reading NZ 368 / IND 720/9.
        box(d, 0, 0, w, h, (60, 160, 90))
        box(d, 0, 20, w, 34, (45, 55, 70))
        crowd = ((220, 180, 140), (180, 120, 80), (240, 200, 160),
                 (200, 60, 60), (60, 120, 200), (240, 240, 240),
                 (30, 30, 30), (250, 200, 40))
        for row, cy in ((0, 25), (1, 30)):
            for i, hx in enumerate(range(6, w - 4, 7)):
                disc(d, hx, cy, 2, crowd[(i + row * 3) % len(crowd)])
        box(d, 0, 34, w, 36, (220, 220, 220))
        for px0 in (6, 190):
            seg(d, [(px0, 20), (px0, 34)], (120, 125, 135), 2)
            box(d, px0 - 5, 20, px0 + 5, 26, (90, 95, 105))
            for lx in (px0 - 3, px0 + 1):
                disc(d, lx, 22, 1, "white")
        poly(d, [(4, 26), (14, 26), (30, 44), (0, 44)], (235, 235, 195))
        poly(d, [(182, 26), (192, 26), (196, 44), (166, 44)],
             (235, 235, 195))
        for sy in range(36, h, 16):
            box(d, 0, sy, w, sy + 8, (52, 148, 82))
        box(d, 88, 38, 110, h, (214, 186, 140))
        seg(d, [(88, 42), (110, 42)], "white", 2)
        seg(d, [(88, 74), (110, 74)], "white", 2)
        for sx in (94, 98, 102):
            box(d, sx, 38, sx + 2, 48, (240, 220, 140))
        seg(d, [(94, 38), (104, 38)], (240, 220, 140))
        disc(d, 125, 51, 5, (200, 140, 90))
        box(d, 120, 56, 131, 70, (20, 20, 25))
        seg(d, [(122, 70), (116, 79)], "white", 4)
        seg(d, [(129, 70), (135, 79)], "white", 4)
        seg(d, [(128, 58), (142, 48)], (200, 140, 90), 3)
        seg(d, [(142, 48), (156, 34)], (200, 170, 110), 5)
        disc(d, 159, 33, 4, (200, 40, 40), outline="white", width=1)
        seg(d, [(166, 27), (172, 22)], "white", 2)
        for fx, fy in ((28, 58), (58, 70), (170, 52)):
            disc(d, fx, fy, 3, "white")
        box(d, 136, 58, 194, 78, "white")
        d.rectangle((136, 58, 194, 78), outline=BLACK, width=1)
        txt(d, (165, 63), "NZ 368", TY.slabssm, BLACK, anchor="mm")
        txt(d, (165, 72), "IND 720/9", TY.slabssm, BLACK, anchor="mm")
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
    elif key == "servers":
        # FBI probes a hack of its crime database: dark server room,
        # three racks with blinking lights, red bolt, glowing monitor.
        box(d, 0, 0, w, h, (16, 24, 44))
        for rx in (18, 76, 134):
            box(d, rx, 24, rx + 48, 72, (40, 48, 64))
            d.rectangle((rx, 24, rx + 48, 72), outline=(90, 100, 120))
            for ry in range(28, 68, 10):
                box(d, rx + 6, ry, rx + 42, ry + 6, (24, 32, 48))
                disc(d, rx + 38, ry + 3, 2, (60, 200, 90))
        poly(d, [(92, 22), (104, 22), (96, 40), (108, 40),
                 (84, 66), (90, 44), (80, 44)], (220, 30, 40))
        box(d, 140, 30, 176, 48, (180, 220, 240))
        seg(d, [(146, 36), (170, 36)], (20, 60, 120), 2)
        seg(d, [(146, 42), (162, 42)], (20, 60, 120), 2)
    elif key == "football":
        # Liverpool thrash 10-man Man Utd: green pitch, red striker
        # volleying into the net, white goal frame, 4–0 board.
        box(d, 0, 0, w, h, (30, 140, 60))
        for sy in range(20, h, 16):
            box(d, 0, sy, w, sy + 8, (26, 128, 54))
        seg(d, [(0, 40), (w, 40)], "white", 2)
        d.rectangle((150, 26, 192, 62), outline="white", width=3)
        for gx in range(154, 190, 8):
            seg(d, [(gx, 28), (gx, 60)], (220, 220, 220))
        for gy in range(30, 60, 8):
            seg(d, [(152, gy), (190, gy)], (220, 220, 220))
        disc(d, 89, 35, 5, (200, 140, 90))
        box(d, 84, 40, 95, 56, (200, 30, 40))
        seg(d, [(86, 56), (80, 68)], "white", 4)
        seg(d, [(93, 56), (100, 68)], "white", 4)
        seg(d, [(93, 44), (108, 36)], (200, 140, 90), 3)
        seg(d, [(108, 36), (128, 30)], (200, 140, 90), 4)
        disc(d, 133, 29, 5, "white", outline=BLACK, width=1)
        poly(d, [(130, 26), (134, 30), (130, 34), (126, 30)], BLACK)
        box(d, 8, 60, 66, 76, "white")
        d.rectangle((8, 60, 66, 76), outline=BLACK, width=1)
        txt(d, (37, 68), "LIV 4–0 MUN", TY.slabssm, BLACK, anchor="mm")
    elif key == "f1night":
        # Verstappen wins under lights in Las Vegas: night skyline,
        # neon strip, low red F1 car, checkered flag.
        box(d, 0, 0, w, h, (10, 12, 28))
        for bx, bh, col in ((10, 28, (200, 220, 240)), (34, 40, (255, 90, 90)),
                            (60, 24, (255, 220, 80)), (84, 34, (100, 200, 255)),
                            (110, 44, (220, 160, 255)), (142, 30, (200, 220, 240)),
                            (166, 38, (120, 240, 160))):
            box(d, bx, 18, bx + 18, 18 + bh, col)
        for wx in range(14, w, 10):
            disc(d, wx, 26, 1, "white")
        box(d, 0, 56, w, h, (30, 30, 36))
        seg(d, [(0, 58), (w, 58)], (240, 180, 40), 2)
        poly(d, [(30, 64), (120, 62), (128, 70), (36, 72)], (200, 30, 40))
        box(d, 50, 56, 84, 64, (200, 30, 40))
        seg(d, [(96, 58), (96, 52)], (220, 220, 230), 2)
        for wx in (40, 112):
            disc(d, wx, 72, 5, (20, 20, 20))
            disc(d, wx, 72, 2, (180, 180, 190))
        disc(d, 160, 34, 14, (255, 210, 31))
        for cx in range(152, 168, 4):
            for cy in range(26, 42, 4):
                box(d, cx, cy, cx + 2, cy + 2, "black")
        seg(d, [(160, 48), (160, 68)], (120, 120, 130), 2)
    elif key == "drones":
        # Kyiv region hit overnight: dark sky, red drone with a
        # rotor, a falling missile, a fire glow behind a roofline.
        box(d, 0, 0, w, h, (14, 16, 28))
        for sx, sy in ((30, 14), (80, 8), (150, 12), (185, 18)):
            disc(d, sx, sy, 1, "white")
        for rx, rw in ((0, 42), (42, 28), (70, 52), (122, 34),
                       (156, 40)):
            box(d, rx, 46, rx + rw, 62, (60, 60, 70))
        disc(d, 98, 54, 12, (255, 140, 40))
        disc(d, 98, 58, 6, (255, 210, 31))
        d.ellipse((54, 20, 64, 26), fill=(90, 95, 105))
        seg(d, [(46, 18), (72, 18)], (200, 200, 210), 2)
        seg(d, [(59, 26), (59, 30)], (200, 200, 210))
        seg(d, [(132, 34), (150, 42)], (255, 120, 60), 3)
        burst(d, 152, 44, 6, 3, (255, 140, 40))
    elif key == "africa":
        # SPLA-IO attack kills 24 in South Sudan: red sun, acacia
        # silhouettes, three white huts.
        box(d, 0, 0, w, h, (240, 180, 110))
        disc(d, 150, 28, 20, (230, 60, 40))
        box(d, 0, 54, w, h, (190, 140, 70))
        for ax, ay in ((30, 42), (170, 38)):
            seg(d, [(ax, 54), (ax, ay)], (90, 60, 40), 3)
            seg(d, [(ax - 14, ay + 2), (ax + 14, ay + 2)], (90, 60, 40), 3)
            seg(d, [(ax - 10, ay + 6), (ax + 10, ay + 6)], (90, 60, 40), 2)
        for hx, hy, hs in ((60, 60, 16), (95, 64, 20), (130, 62, 14)):
            box(d, hx, hy, hx + hs, hy + 16, (250, 245, 230))
            poly(d, [(hx - 4, hy), (hx + hs // 2, hy - 10),
                     (hx + hs + 4, hy)], (200, 60, 40))
    elif key == "ebola":
        # Ebola response disrupted in Congo: grey clinic, red
        # cross, red no-go circle over a syringe.
        box(d, 0, 0, w, h, (200, 210, 220))
        box(d, 0, 60, w, h, (130, 140, 150))
        box(d, 54, 34, 142, 64, "white")
        d.rectangle((54, 34, 142, 64), outline=(60, 60, 70))
        box(d, 66, 34, 130, 44, (200, 30, 40))
        for wx in (64, 92, 120):
            box(d, wx, 50, wx + 12, 60, (40, 90, 160))
        box(d, 84, 18, 112, 34, "white")
        box(d, 92, 8, 104, 34, (200, 30, 40))
        seg(d, [(88, 20), (108, 20)], SCARLET, 2)
        seg(d, [(98, 10), (98, 30)], SCARLET, 2)
        seg(d, [(138, 20), (158, 44)], (20, 20, 20), 3)
        seg(d, [(138, 20), (158, 44)], SCARLET, 2)
        ring(d, 140, 16, 172, 48, SCARLET, 3)
        seg(d, [(144, 20), (168, 44)], SCARLET, 3)
    elif key == "march":
        # Lisbon cost-of-living march: two banners and placards,
        # marchers below.
        box(d, 0, 0, w, h, (160, 210, 230))
        box(d, 0, 58, w, h, (90, 90, 98))
        for px, py, pw, ph, col, lab in ((20, 22, 74, 18, SCARLET, "FIM"),
                                         (100, 20, 80, 20, (20, 60, 140),
                                          "A VIDA")):
            box(d, px, py, px + pw, py + ph, col)
            txt(d, (px + pw // 2, py + ph // 2), lab, TY.slabssm,
                "white", anchor="mm")
            seg(d, [(px + pw // 2, py + ph), (px + pw // 2, 58)],
                (60, 60, 60), 2)
        for mx in (40, 78, 118, 156):
            disc(d, mx, 58, 5, (30, 30, 40))
            box(d, mx - 3, 63, mx + 3, 78, (30, 30, 40))
        seg(d, [(30, 48), (30, 62)], (60, 60, 60), 2)
        box(d, 22, 42, 38, 50, "white")
        seg(d, [(24, 46), (36, 46)], (20, 20, 20), 2)
    else:
        raise ValueError("unknown art: %s" % key)
    return img.resize((w, h), Image.LANCZOS)


# --- assembly ----------------------------------------------------------------
def heropic(key, w, big, small):
    """A lead picture: painted 105 tall with its bottom-left label,
    shrunk to 100."""
    img = art(key, w, 105)
    d2 = ImageDraw.Draw(img)
    tag(d2, w, 105, big, small)
    return img.resize((w, HA), Image.LANCZOS)


def minipic(key, big, small):
    """A small picture: painted 196x80 with its solid red banner,
    shrunk to 196x48."""
    img = art(key, 196, 80)
    d2 = ImageDraw.Draw(img)
    banner(d2, 196, big, small, SCARLET)
    return img.resize((196, SA), Image.LANCZOS)


def hero_card(img, d, story, x, y, w):
    """A lead card, 202 tall: 100px art with a bottom-left label, a
    14px navy strip (pill left, number + place + topic, source right
    in gold), a two-line 27px serif headline and a two-line 12px
    serif deck, the text block centred in the 88px area under the
    strip, all inside a 1px ink box."""
    num, place, topic, src, _st, head, deck, big, small, key, vtag = story
    box(d, x, y, x + w, y + HH, PANEL)
    img.paste(heropic(key, w, big, small), (x, y))
    sy = y + HA
    box(d, x, sy, x + w, sy + HK, MIDNIGHT)
    pw = int(d.textlength(vtag, font=TY.tag)) + 10
    d.rounded_rectangle((x + 8, sy + 2, x + 8 + pw, sy + 12), radius=2,
                        fill=PILL[vtag])
    txt(d, (x + 13, sy + 7), vtag, TY.tag, "white", anchor="lm")
    txt(d, (x + 14 + pw, sy + 7), "%d. %s · %s" % (num, place, topic),
        TY.strip, "white", anchor="lm")
    txt(d, (x + w - 8, sy + 7), src, TY.src, GILT, anchor="rm")
    hl = wrap(d, head, TY.hhead, w - 16, 2)
    dl = wrap(d, deck, TY.hdeck, w - 16, 2)
    bh = len(hl) * 30 + 2 + len(dl) * 13
    ty = sy + HK + (HT - bh) // 2
    for j, ln in enumerate(hl):
        txt(d, (x + 8, ty + j * 30), ln, TY.hhead, BLACK)
    for j, ln in enumerate(dl):
        txt(d, (x + 8, ty + len(hl) * 30 + 2 + j * 13), ln, TY.hdeck,
            (60, 60, 60))
    d.rectangle((x, y, x + w, y + HH), outline=BLACK, width=1)


def small_card(img, d, story, x, y):
    """A small card, 124 tall: 48px art with its red banner, a 14px
    navy strip (number + place + topic left, pill right — the strip
    text shrinks 9px to 8px when pill + text would overflow the
    196px card), a two-line 16px serif headline and a two-line 11px
    serif deck with its source, inside a 1px ink box."""
    num, place, topic, src, _st, head, deck, big, small, key, vtag = story
    w = 196
    box(d, x, y, x + w, y + SH, PANEL)
    img.paste(minipic(key, big, small), (x, y))
    sy = y + SA
    box(d, x, sy, x + w, sy + SK, MIDNIGHT)
    kick = "%d. %s · %s" % (num, place, topic)
    pw = int(d.textlength(vtag, font=TY.tag)) + 10
    fk = TY.stripsm
    if d.textlength(kick, font=fk) + pw + 12 > w:
        fk = TY.striptn
    txt(d, (x + 4, sy + 7), kick, fk, "white", anchor="lm")
    d.rounded_rectangle((x + w - 4 - pw, sy + 2, x + w - 4, sy + 12),
                        radius=2, fill=PILL[vtag])
    txt(d, (x + w + 1 - pw, sy + 7), vtag, TY.tag, "white", anchor="lm")
    hl = wrap(d, head, TY.shead, w - 16, 2)
    for j, ln in enumerate(hl):
        txt(d, (x + 8, sy + SK + 4 + j * 16), ln, TY.shead, BLACK)
    dl = wrap(d, deck + " — " + src, TY.sdeck, w - 16, 2)
    for j, ln in enumerate(dl):
        txt(d, (x + 8, sy + SK + 5 + len(hl) * 16 + j * 12), ln,
            TY.sdeck, (60, 60, 60))
    d.rectangle((x, y, x + w, y + SH), outline=BLACK, width=1)


def draw_map(d, x0, y0, w, h):
    """A light world map: pale blue sea, tan land from
    world.geo.json, navy dots for the also-list stories, numbered
    red pins for the drawn stories. Equirectangular projection;
    pins and dots that would sit on top of each other are fanned
    out a few pixels with a thin leader line back to their true
    spot (see PIN_OFF / DOT_OFF)."""
    with open(os.path.join(HERE, "world.geo.json")) as fh:
        geo = json.load(fh)

    def px(lon):
        return x0 + (lon + 180.0) / 360.0 * w

    def py(lat):
        return y0 + (90.0 - lat) / 180.0 * h

    box(d, x0, y0, x0 + w, y0 + h, SEA)
    for feat in geo["features"]:
        geom = feat["geometry"]
        polys = []
        if geom["type"] == "Polygon":
            polys = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            polys = geom["coordinates"]
        for poly_ring in polys:
            ring = poly_ring[0]
            pts = [(px(lon), py(lat)) for lon, lat in ring]
            poly(d, pts, SHORE, outline=(200, 180, 120))
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
    # ---- masthead 0-149: the date at 120px on its own layer,
    # squeezed horizontally to 996px so its ink top sits at 19
    # (ink 19-127, 109px tall); the deck line at y=123; the
    # kicker at the top right; the bottom rule at 147-149. ----
    title = "Monday 23 November 2026"
    lw = int(d.textlength(title, font=TY.mast)) + 8
    layer = Image.new("RGBA", (lw, 150), (0, 0, 0, 0))
    lt = ImageDraw.Draw(layer)
    lt.text((4, 0), title, font=TY.mast, fill=BLACK + (255,))
    ink_top = layer.getbbox()[1]
    layer = layer.resize((996, 150), Image.LANCZOS)
    img.paste(layer, (MX, 19 - ink_top), layer)
    txt(d, (MX, 123),
        "COP31 talks collapse with no deal · Missiles rain on the "
        "Gulf · Democrats win the House", TY.deck, SCARLET)
    txt(d, (RX, 1),
        "36 STORIES · 7 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER "
        "2026", TY.kick, BLACK, anchor="ra")
    box(d, 0, 147, W, 149, BLACK)
    # ---- numbers strip 150-162: six figures, red value + ink
    # caption, separated by middots. ----
    nx = MX + int(d.textlength("THE DAY IN NUMBERS:  ", font=TY.clock))
    txt(d, (MX, 150), "THE DAY IN NUMBERS:", TY.clock, SCARLET)
    for i, (value, caption) in enumerate(STATS):
        txt(d, (nx, 150), value, TY.clock, SCARLET)
        nx += int(d.textlength(value, font=TY.clock)) + 4
        txt(d, (nx, 150), caption, TY.clock, BLACK)
        nx += int(d.textlength(caption, font=TY.clock))
        if i < len(STATS) - 1:
            txt(d, (nx, 150), "  ·  ", TY.clock, ASH)
            nx += int(d.textlength("  ·  ", font=TY.clock))
    # ---- region bar 164-175: seven equal segments, count after
    # the name, white 9px bold centred in each segment. ----
    bx, by, bw, bh = MX, 164, 1000, 11
    segw = bw / len(REGIONS)
    for i, (label, count, fill, ink) in enumerate(REGIONS):
        sx = bx + i * segw
        box(d, sx, by, sx + segw - 1, by + bh, fill)
        txt(d, (sx + segw / 2, by + 6), "%s %d" % (label, count),
            TY.src, ink, anchor="mm")
    # ---- UTC timeline 176-202: a black label box at the left,
    # then seven evenly spaced columns (98-1012, 130.6px each):
    # red bold time above a ruled line with a red dot, bold
    # event below. ----
    tl_y = 176
    box(d, MX, tl_y, 90, tl_y + 20, BLACK)
    txt(d, (51, tl_y + 10), "THE DAY IN UTC", TY.src, "white",
        anchor="mm")
    timeline = [("00:30", "Tankers hit in Hormuz"),
                ("04:00", "Verstappen wins Vegas"),
                ("06:00", "COP31 talks collapse"),
                ("09:00", "Nepal PM meets Modi"),
                ("12:00", "Chapo Isidro arrested"),
                ("14:00", "Democrats pass 258"),
                ("17:00", "Factory toll at 7")]
    tl_x0, tl_x1 = 98, RX
    col = (tl_x1 - tl_x0) / len(timeline)
    seg(d, [(tl_x0, tl_y + 13), (tl_x1, tl_y + 13)], BLACK, 1)
    for i, (tt, ev) in enumerate(timeline):
        cx = tl_x0 + col * (i + 0.5)
        txt(d, (cx, tl_y), tt, TY.clock, SCARLET, anchor="ma")
        disc(d, cx, tl_y + 13, 3, SCARLET)
        txt(d, (cx, tl_y + 17), ev, TY.clocksm, BLACK, anchor="ma")
    # ---- heroes 205-407: lead 396 wide, two rails 294 wide,
    # 8px gaps. ----
    hx = MX
    for i, story in enumerate(FRONT[:3]):
        w = [396, 294, 294][i]
        hero_card(img, d, story, hx, HY, w)
        hx += w + 8
    # ---- smalls 415-793: three rows of five, 196 wide, 204
    # pitch, 126 row pitch, 9px gaps. ----
    for r in range(3):
        for c in range(5):
            k = 3 + r * 5 + c
            small_card(img, d, FRONT[k], MX + c * 204,
                       SY + r * SR)
    # ---- map + also 801-963: the light map at the left, the
    # 18-line also-list in two 320px columns at the right. ----
    txt(d, (MX, MY), "WHERE IT HAPPENED", TY.sect, BLACK)
    seg(d, [(MX, MY + 16), (348, MY + 16)], BLACK, 1)
    box(d, MX, MY + 22, 348, MY + 162, SEA)
    d.rectangle((MX, MY + 22, 348, MY + 162), outline=EDGE, width=1)
    draw_map(d, MX, MY + 22, MW, MH)
    also_x = 364
    txt(d, (also_x, MY), "ALSO ON MONDAY 23 NOVEMBER", TY.sect, BLACK)
    txt(d, (RX, MY), "18 MORE STORIES", TY.sect, BLACK, anchor="ra")
    seg(d, [(also_x, MY + 16), (RX, MY + 16)], BLACK, 1)
    col_w, rows = 320, 9
    for i, (num, city, line, src) in enumerate(ALSO):
        col_i = 0 if i < rows else 1
        row = i if i < rows else i - rows
        x = also_x + col_i * (col_w + 8)
        y = MY + 22 + row * 13
        txt(d, (x, y), "%d." % num, TY.alsonum, SCARLET)
        full = "%s: %s (%s)" % (city, line, src)
        lines = wrap(d, full, TY.also, col_w - 22, 1)
        txt(d, (x + 20, y), lines[0] if lines else "", TY.also, BLACK)
    # ---- date check 969-996: the red box naming the big stories
    # deliberately left out because they are not Monday — Saturday's
    # Sparta II drone hit (only the fire is Monday), Sunday's Hong
    # Kong vote and the 186-drone barrage; plus what is not yet
    # confirmed, and the Liverpool match, played Sunday. ----
    d.rectangle((MX, CY, RX, CY + 27), outline=SCARLET, width=2)
    chk = ("DATE CHECK — Left out, first reported Sunday 22 Nov: "
           "Sparta II hit (only the fire is Monday) · Hong Kong "
           "Election Committee vote · Russia's 186-drone barrage on "
           "Kyiv. Played Sunday, reported Monday: Liverpool–Man "
           "Utd. Not yet confirmed: Iran's radar-hit claim · COP31 "
           "final text.")
    chk_lines = wrap(d, chk, TY.chk, 976, 2)
    for j, ln in enumerate(chk_lines):
        txt(d, (20, CY - 1 + j * 11), ln, TY.chk, BLACK)
    # ---- footer 999-1019: a centred sources line, then the HOW
    # WE CHECKED legend as one line. ----
    txt(d, (512, FY),
        "Sources: Reuters · AP · AFP · SCMP · Al Jazeera · BBC · "
        "Guardian · Detik · Xinhua · IANS · Yonhap · ABC · ESPN · "
        "UKMTO · WHO. · Corrections: none", TY.foot, ASH, anchor="ma")
    hx = 20 + int(d.textlength("HOW WE CHECKED — ", font=TY.foot))
    txt(d, (20, FY + 10), "HOW WE CHECKED — ", TY.foot, SCARLET)
    txt(d, (hx, FY + 10),
        "CONFIRMED 2+ named sources agree · OFFICIAL on the record "
        "· REPORTED one named source · CLAIM one side's claim, "
        "unverified", TY.foot, BLACK)
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
