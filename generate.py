#!/usr/bin/env python3
"""Draw the 25 November 2026 front page (make.fun news-image-20261125).

Reads stories.json next to this file and paints a 1024x1024 newspaper
front page with Pillow: masthead, lead story with a small drawn chart,
a simplified world map carrying 13 numbered pins, the pinned stories
listed beneath it, a row of briefs and a ticker strip at the foot.

Everything is fixed input -> fixed output: no clock, no randomness,
no network, so two runs write identical bytes.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
MX = 34                      # side margin
PAPER = (251, 248, 241)      # newsprint off-white
INK = (22, 22, 22)
SOFT = (92, 90, 84)          # grey for secondary text
FAINT = (168, 164, 154)
SEA = (208, 228, 240)
LAND = (196, 205, 158)
LAND_EDGE = (140, 150, 105)
RED = (178, 36, 28)
GREEN = (38, 110, 58)
BLUE = (28, 76, 136)
GOLD = (176, 132, 24)
WHITE = (255, 255, 255)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap to lines that fit max_w pixels."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def ellipsize(d, text, font, max_w):
    """Shorten text with an ellipsis so it fits max_w pixels."""
    if d.textlength(text, font=font) <= max_w:
        return text
    while text and d.textlength(text + "...", font=font) > max_w:
        text = text[:-1]
    return text + "..."


def rule(d, x0, x1, y, fill=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# Coarse continent outlines as (lon, lat) points, drawn small so a
# rough shape still reads as the world. Kept deliberately simple.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-112, 68), (-96, 69),
     (-88, 66), (-82, 66), (-76, 62), (-65, 60), (-56, 52), (-60, 46),
     (-68, 44), (-74, 39), (-76, 34), (-80, 27), (-84, 30), (-90, 21),
     (-86, 16), (-92, 15), (-97, 16), (-104, 19), (-110, 24), (-117, 33),
     (-123, 38), (-124, 46), (-130, 55), (-140, 60), (-152, 58),
     (-162, 58), (-168, 66)],
    # South America
    [(-80, 10), (-77, 5), (-72, 0), (-68, -4), (-60, -6), (-50, 0),
     (-40, -4), (-35, -8), (-38, -15), (-41, -22), (-48, -27), (-52, -33),
     (-58, -38), (-65, -41), (-68, -50), (-71, -54), (-73, -46), (-73, -36),
     (-71, -28), (-75, -18), (-79, -10), (-81, -4), (-80, 4)],
    # Africa
    [(-17, 15), (-16, 21), (-10, 30), (-6, 35), (2, 37), (10, 37),
     (15, 32), (22, 33), (30, 31), (33, 27), (36, 22), (39, 18),
     (43, 12), (48, 11), (51, 10), (48, 2), (42, -4), (40, -12),
     (36, -18), (32, -26), (28, -33), (20, -35), (16, -28), (13, -18),
     (12, -8), (9, -1), (9, 4), (2, 6), (-7, 5), (-13, 8), (-17, 12)],
    # Europe
    [(-10, 36), (-9, 43), (-4, 44), (-2, 48), (0, 50), (3, 51), (5, 53),
     (7, 55), (8, 57), (10, 59), (14, 57), (18, 56), (21, 55), (24, 59),
     (27, 60), (30, 62), (28, 65), (24, 68), (20, 70), (16, 70),
     (12, 66), (10, 62), (6, 58), (4, 55), (0, 52), (-3, 49), (-6, 46),
     (-9, 42), (-10, 39)],
    # Asia
    [(30, 62), (36, 66), (44, 68), (52, 69), (60, 69), (68, 71),
     (76, 72), (84, 73), (92, 74), (100, 75), (108, 74), (116, 73),
     (124, 72), (132, 71), (140, 72), (148, 71), (156, 69), (162, 66),
     (170, 66), (178, 65), (173, 62), (168, 60), (162, 58), (158, 53),
     (156, 59), (150, 59), (144, 56), (141, 50), (140, 44), (137, 40),
     (133, 36), (129, 34), (127, 36), (124, 32), (122, 30), (120, 26),
     (118, 24), (114, 22), (110, 20), (107, 16), (105, 12), (103, 8),
     (100, 7), (98, 10), (96, 15), (94, 17), (92, 21), (89, 22),
     (86, 20), (83, 17), (80, 14), (77, 9), (75, 12), (73, 19),
     (71, 22), (68, 23), (66, 25), (62, 25), (58, 26), (56, 26),
     (54, 27), (52, 28), (50, 29), (48, 30), (46, 29), (44, 28),
     (42, 24), (40, 21), (39, 18), (37, 15), (35, 13), (33, 14),
     (31, 17), (30, 21), (29, 27), (29, 31), (30, 36), (28, 40),
     (27, 41), (26, 40), (24, 38), (23, 36), (22, 38), (26, 40),
     (28, 44), (28, 48), (29, 52), (30, 56), (30, 60)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (122, -34),
     (126, -32), (130, -32), (134, -33), (137, -35), (140, -38),
     (144, -38), (147, -39), (150, -37), (153, -32), (153, -27),
     (151, -24), (149, -20), (146, -19), (143, -15), (142, -11),
     (139, -14), (136, -12), (133, -12), (130, -13), (127, -14),
     (124, -16), (121, -19), (118, -20), (115, -21)],
]


def project(lon, lat, box):
    """Equirectangular lon/lat -> pixels inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (78.0 - lat) / 136.0 * (y1 - y0)
    return x, y


def draw_map(d, box, pinned):
    """Sea, continents, graticule and numbered red pins."""
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=SEA, outline=FAINT, width=1)
    for lon in range(-150, 181, 30):
        gx, _ = project(lon, 0, box)
        d.line([(gx, y0), (gx, y1)], fill=(226, 238, 245), width=1)
    for lat in (-40, 0, 40):
        _, gy = project(0, lat, box)
        d.line([(x0, gy), (x1, gy)], fill=(226, 238, 245), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for story in pinned:
        px, py = project(story["lon"], story["lat"], box)
        r = 11
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=WHITE, width=2)
        label = str(story["n"])
        fw = d.textlength(label, font=fnt(SANS_B, 13))
        d.text((px - fw / 2, py - 7), label, font=fnt(SANS_B, 13),
               fill=WHITE)


def draw_masthead(d, date_text):
    d.line([(MX, 26), (W - MX, 26)], fill=INK, width=3)
    title = "THE WORLD IN ONE PAGE"
    tf = fnt(SERIF_B, 52)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 34), title, font=tf, fill=INK)
    df = fnt(SANS_B, 19)
    dw = d.textlength(date_text, font=df)
    d.text(((W - dw) / 2, 96), date_text, font=df, fill=RED)
    lf = fnt(SANS, 15)
    left = "WEDNESDAY EDITION"
    d.text((MX, 99), left, font=lf, fill=SOFT)
    right = "make.fun news-image"
    rw = d.textlength(right, font=lf)
    d.text((W - MX - rw, 99), right, font=lf, fill=SOFT)
    rule(d, MX, W - MX, 122, width=3)


def draw_lead(d, lead, x0, y0, w, h):
    """Lead story text left, small drawn market chart right."""
    chart_w = 268
    text_w = w - chart_w - 28
    # kicker chip
    chip_f = fnt(SANS_B, 16)
    chip_txt = "LEAD  ·  BUSINESS  ·  USA"
    cw = d.textlength(chip_txt, font=chip_f)
    d.rounded_rectangle([x0, y0, x0 + cw + 20, y0 + 26], radius=4, fill=RED)
    d.text((x0 + 10, y0 + 4), chip_txt, font=chip_f, fill=WHITE)
    # headline
    hf = fnt(SERIF_B, 46)
    d.text((x0, y0 + 34), lead["headline"], font=hf, fill=INK)
    # sub + detail
    sf = fnt(SANS, 20)
    y = y0 + 92
    for line in wrap(d, lead["sub"], sf, text_w):
        d.text((x0, y), line, font=sf, fill=INK)
        y += 25
    y += 4
    df = fnt(SANS, 16)
    for line in wrap(d, lead["detail"], df, text_w):
        d.text((x0, y), line, font=df, fill=SOFT)
        y += 20
    # chart panel: a chip that jumped
    cx0 = x0 + text_w + 28
    cy0 = y0 + 6
    cx1, cy1 = x0 + w, y0 + h - 8
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=8, fill=(24, 48, 34))
    d.text((cx0 + 16, cy0 + 12), "NVDA", font=fnt(SANS_B, 22), fill=WHITE)
    d.text((cx0 + 16, cy0 + 42), "+31.5%", font=fnt(SERIF_B, 34),
           fill=(120, 220, 140))
    d.text((cx0 + 16, cy0 + 82), "in one day", font=fnt(SANS, 15),
           fill=(200, 210, 200))
    d.text((cx0 + 16, cy1 - 26), "~$1tn regained", font=fnt(SANS_B, 15),
           fill=(150, 200, 160))
    # rising bars
    bx = cx1 - 108
    bars = [18, 26, 22, 34, 44, 58]
    for i, bh in enumerate(bars):
        d.rectangle([bx + i * 16, cy1 - 30 - bh, bx + i * 16 + 10,
                     cy1 - 30], fill=(90, 190, 120))
    d.line([(bx - 4, cy1 - 30 - 58), (bx + 96, cy1 - 30 - 14)],
           fill=(150, 230, 170), width=3)


def section_head(d, x, y, text):
    d.text((x, y), text, font=fnt(SANS_B, 15), fill=RED)
    rule(d, x, W - MX, y + 21, fill=FAINT, width=1)


def draw_pinned(d, pinned, y_top, y_bottom):
    """Two columns of numbered stories; returns nothing, asserts fit."""
    section_head(d, MX, y_top, "ON THE MAP  —  13 STORIES")
    col_w = (W - 2 * MX - 28) // 2
    left = pinned[:7]
    right = pinned[7:]
    row_h = (y_bottom - (y_top + 28)) // 7
    hf = fnt(SANS_B, 15)
    sf = fnt(SANS, 13)
    for col_i, col in enumerate((left, right)):
        x = MX + col_i * (col_w + 28)
        y = y_top + 28
        for story in col:
            num = str(story["n"])
            d.text((x, y), num, font=fnt(SERIF_B, 17), fill=RED)
            tx = x + 26
            head = story["headline"]
            head = ellipsize(d, head, hf, col_w - 26)
            d.text((tx, y + 1), head, font=hf, fill=INK)
            summ = ellipsize(d, story["summary"], sf, col_w - 26)
            d.text((tx, y + 20), summ, font=sf, fill=SOFT)
            y += row_h


def draw_briefs(d, briefs, y_top, y_bottom):
    section_head(d, MX, y_top, "BRIEFS")
    col_w = (W - 2 * MX - 28) // 2
    bf = fnt(SANS, 13)
    rows = (y_bottom - (y_top + 28)) // 6
    for col_i in range(2):
        x = MX + col_i * (col_w + 28)
        y = y_top + 28
        for story in briefs[col_i * 6:(col_i + 1) * 6]:
            line = story["headline"] + " — " + story["summary"]
            line = ellipsize(d, line, bf, col_w)
            d.text((x, y), "•  " + line, font=bf, fill=INK)
            y += rows


def draw_ticker(d, ticker, y):
    rule(d, MX, W - MX, y, width=2)
    tf = fnt(SANS, 12)
    half = (len(ticker) + 1) // 2
    for i, line in enumerate(("   •   ".join(ticker[:half]),
                             "   •   ".join(ticker[half:]))):
        tw = d.textlength(line, font=tf)
        d.text(((W - tw) / 2, y + 6 + i * 16), line, font=tf, fill=INK)
    rule(d, MX, W - MX, y + 38, fill=FAINT, width=1)
    ff = fnt(SANS, 12)
    foot = ("All stories as reported on Wednesday 25 November 2026  ·  "
            "make.fun news-image-20261125")
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, y + 44), foot, font=ff, fill=SOFT)


def main():
    with open(os.path.join(HERE, "stories.json")) as fh:
        data = json.load(fh)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d, data["date"])
    draw_lead(d, data["lead"], MX, 134, W - 2 * MX, 138)
    rule(d, MX, W - MX, 296, width=2)
    d.text((MX, 304), "THE WORLD TODAY", font=fnt(SANS_B, 15), fill=RED)
    draw_map(d, (MX, 324, W - MX, 500), data["pinned"])
    draw_pinned(d, data["pinned"], 508, 762)
    draw_briefs(d, data["briefs"], 772, 958)
    draw_ticker(d, data["ticker"], 960)
    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
