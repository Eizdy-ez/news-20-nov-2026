#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261120.

Original editorial front page, drawn programmatically with Pillow:
no photographs, no copied artwork, no network. Every shape and every
word is produced by this script, so the PNG is fully deterministic.

Layout (1024 x 1024, newspaper front page):
  header  : FRIDAY 20 NOVEMBER 2026 (the day, unmissable)
  hero    : Trump, Xi and Putin meet in Shenzhen
  row 2   : Kyiv under fire | ICJ genocide ruling on Myanmar
  row 3   : Tanker ablaze in the Strait of Hormuz | COP31 stalls |
            Markets slide (S&P 500 -3.7%)
Run:  python3 draw.py   ->  writes entry.png next to this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 24, 39)
NAVY = (30, 58, 95)
RED = (185, 28, 28)
TEAL = (13, 116, 128)
GREY = (90, 96, 108)
LIGHT = (255, 255, 255)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def fit(draw, text, size, width, bold=True):
    """Largest bold font size <= size that fits text on one line."""
    s = size
    while s > 10 and draw.textlength(text, font=font(s, bold=bold)) > width:
        s -= 1
    return font(s, bold=bold)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=None):
    x, y = xy
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, box, bg):
    draw.rectangle(box, fill=bg, outline=INK, width=3)


def kicker(draw, xy, text, color=RED, size=19):
    draw.text(xy, text, font=font(size, bold=True), fill=color)


# ---------------------------------------------------------------- flags
def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=2)
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                        fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 // 7], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([x + 6 + c * 15, y + 5 + r * 11,
                       x + 10 + c * 15, y + 9 + r * 11], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=2)
    d.text((x + 8, y + 4), "\u2605", font=font(24, bold=True), fill=(255, 222, 0))
    for sx, sy in ((w - 26, 6), (w - 16, 20), (w - 26, 34), (w - 16, 44)):
        d.text((x + sx, y + sy), "\u2605", font=font(12, bold=True),
               fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    for i, col in enumerate(((255, 255, 255), (0, 57, 166), (213, 0, 50))):
        d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=col)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def figure(d, cx, base_y, suit, tie, s=0.72):
    """A suited figure behind a table: no face, no likeness."""
    hw, hh = int(26 * s), int(52 * s)
    d.ellipse([cx - hw, base_y - hh * 2, cx + hw, base_y - hh], fill=(232, 200, 160))
    d.pieslice([cx - hw, base_y - hh * 2, cx + hw, base_y - hh], 180, 360,
               fill=(60, 60, 60))
    bw, bh = int(52 * s), int(58 * s)
    d.polygon([(cx - bw, base_y), (cx - int(44 * s), base_y - bh),
               (cx + int(44 * s), base_y - bh), (cx + bw, base_y)], fill=suit)
    d.polygon([(cx - 10, base_y - bh), (cx, base_y - bh + int(24 * s)),
               (cx + 10, base_y - bh)], fill=(255, 255, 255))
    d.polygon([(cx - 5, base_y - bh), (cx + 5, base_y - bh),
               (cx, base_y - bh + int(26 * s))], fill=tie)


def explosion(d, cx, cy, r):
    for rr, col in ((r, (255, 140, 0)), (int(r * 0.65), (255, 200, 0)),
                    (int(r * 0.35), (255, 240, 180))):
        pts = []
        for i in range(12):
            ang = i * 30
            rad = rr if i % 2 == 0 else rr * 0.55
            pts.append((cx + rad * math.cos(math.radians(ang)),
                        cy + rad * math.sin(math.radians(ang))))
        d.polygon(pts, fill=col)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip -------------------------------------------------
    d.rectangle([0, 0, W, 34], fill=INK)
    d.text((24, 6), "THE WORLD IN ONE DAY", font=font(19, bold=True), fill=LIGHT)
    rx = W - 24 - d.textlength("WORLD NEWS  •  ONE IMAGE", font=font(19, bold=True))
    d.text((rx, 6), "WORLD NEWS  •  ONE IMAGE", font=font(19, bold=True),
           fill=(253, 224, 71))

    # ---- masthead: the date, first and biggest --------------------
    date_font = fit(d, "FRIDAY 20 NOVEMBER 2026", 56, W - 48)
    d.text((24, 44), "FRIDAY 20 NOVEMBER 2026", font=date_font, fill=NAVY)
    d.text((24, 116), "Six stories that defined the day \u2014 from Shenzhen to Kyiv, "
                      "The Hague to the Gulf.",
           font=font(23), fill=INK)
    d.rectangle([24, 150, W - 24, 156], fill=RED)

    # ---- hero: Shenzhen summit ------------------------------------
    hx0, hy0, hx1, hy1 = 24, 168, W - 24, 492
    panel(d, (hx0, hy0, hx1, hy1), (226, 235, 245))
    d.rectangle([hx0 + 3, hy0 + 3, hx1 - 3, hy0 + 88], fill=(191, 219, 254))
    for i, (fn, label) in enumerate(((flag_us, "UNITED STATES"),
                                     (flag_cn, "CHINA"),
                                     (flag_ru, "RUSSIA"))):
        fx = hx0 + 90 + i * 330
        d.line([fx + 40, hy0 + 12, fx + 40, hy0 + 66], fill=INK, width=3)
        fn(d, fx + 44, hy0 + 14, 84, 50)
        d.text((fx + 44, hy0 + 66), label, font=font(15, bold=True), fill=INK)
    d.text((hx0 + 24, hy0 + 100), "THREE LEADERS, ONE TABLE",
           font=fit(d, "THREE LEADERS, ONE TABLE", 38, hx1 - hx0 - 48), fill=NAVY)
    text_block(d, (hx0 + 24, hy0 + 146),
               "Trump, Xi and Putin meet in Shenzhen and issue a joint peace "
               "pledge \u2014 their first three-way summit.",
               font(22), INK, hx1 - hx0 - 48, leading=28)
    table_y = hy1 - 26
    for i, (suit, tie) in enumerate((((30, 58, 95), (185, 28, 28)),
                                     ((120, 20, 20), (253, 224, 71)),
                                     ((40, 40, 40), (30, 58, 95)))):
        figure(d, hx0 + 190 + i * 310, table_y, suit, tie)
    d.rectangle([hx0 + 24, table_y, hx1 - 24, table_y + 20], fill=(120, 72, 20))
    d.rectangle([hx0 + 24, table_y, hx1 - 24, table_y + 20], outline=INK, width=2)

    # ---- row 2: Kyiv | The Hague ----------------------------------
    ry0, ry1 = 508, 730
    # Kyiv
    kx0, kx1 = 24, 504
    panel(d, (kx0, ry0, kx1, ry1), (23, 32, 54))
    art_b = ry0 + 82
    for bx, bh in ((kx0 + 30, 52), (kx0 + 110, 76), (kx0 + 210, 58),
                   (kx0 + 300, 80), (kx0 + 390, 54)):
        d.rectangle([bx, art_b - bh, bx + 62, art_b], fill=(8, 12, 24))
        for wy in range(art_b - bh + 8, art_b - 6, 16):
            d.rectangle([bx + 8, wy, bx + 18, wy + 8], fill=(253, 224, 71))
    explosion(d, kx0 + 130, ry0 + 36, 24)
    explosion(d, kx0 + 380, ry0 + 28, 18)
    kicker(d, (kx0 + 18, ry0 + 94), "KYIV  •  WAR IN UKRAINE")
    d.text((kx0 + 18, ry0 + 120), "KYIV UNDER FIRE",
           font=fit(d, "KYIV UNDER FIRE", 32, kx1 - kx0 - 36), fill=LIGHT)
    text_block(d, (kx0 + 18, ry0 + 160),
               "Russia fires 400+ drones and 110 missiles; 8 killed. "
               "Two missiles land in Poland.",
               font(19), (226, 232, 240), kx1 - kx0 - 36, leading=24)

    # The Hague
    tx0, tx1 = 520, W - 24
    panel(d, (tx0, ry0, tx1, ry1), (255, 251, 235))
    cx = (tx0 + tx1) // 2
    d.polygon([(cx - 150, ry0 + 40), (cx + 150, ry0 + 40), (cx, ry0 + 10)],
              fill=(120, 100, 60))
    for px in (cx - 130, cx - 48, cx + 28, cx + 110):
        d.rectangle([px, ry0 + 40, px + 20, ry0 + 80], fill=(255, 255, 255),
                    outline=INK, width=2)
    d.rectangle([tx0 + 3, ry0 + 80, tx1 - 3, ry0 + 82], fill=(120, 100, 60))
    kicker(d, (tx0 + 18, ry0 + 94), "THE HAGUE  •  JUSTICE")
    d.text((tx0 + 18, ry0 + 120), "GENOCIDE RULING",
           font=fit(d, "GENOCIDE RULING", 32, tx1 - tx0 - 36), fill=INK)
    text_block(d, (tx0 + 18, ry0 + 160),
               "UN court finds Myanmar committed genocide against the "
               "Rohingya \u2014 a first against a state.",
               font(19), INK, tx1 - tx0 - 36, leading=24)

    # ---- row 3: Hormuz | COP31 | Markets --------------------------
    by0, by1 = 746, 956
    bw = (W - 48 - 2 * 16) // 3  # 314
    # Hormuz
    bx0 = 24
    panel(d, (bx0, by0, bx0 + bw, by1), (186, 230, 253))
    d.rectangle([bx0 + 3, by0 + 3, bx0 + bw - 3, by0 + 76], fill=(14, 116, 144))
    d.rectangle([bx0 + 40, by0 + 42, bx0 + bw - 60, by0 + 64], fill=(30, 41, 59))
    d.rectangle([bx0 + 60, by0 + 24, bx0 + 110, by0 + 42], fill=(255, 255, 255),
                outline=INK, width=2)
    explosion(d, bx0 + bw - 70, by0 + 28, 17)
    kicker(d, (bx0 + 14, by0 + 86), "THE GULF", size=18)
    d.text((bx0 + 14, by0 + 110), "TANKER ABLAZE",
           font=fit(d, "TANKER ABLAZE", 25, bw - 28), fill=INK)
    text_block(d, (bx0 + 14, by0 + 142),
               "Ship struck in the Strait of Hormuz; fire aboard. "
               "US blockade holds.",
               font(17), INK, bw - 28, leading=22)
    # COP31
    cx0 = bx0 + bw + 16
    panel(d, (cx0, by0, cx0 + bw, by1), (204, 251, 233))
    d.ellipse([cx0 + bw // 2 - 32, by0 + 8, cx0 + bw // 2 + 32, by0 + 72],
              fill=(34, 139, 92), outline=INK, width=2)
    d.ellipse([cx0 + bw // 2 - 20, by0 + 22, cx0 + bw // 2 - 2, by0 + 38],
              fill=(167, 243, 208))
    d.ellipse([cx0 + bw // 2 + 4, by0 + 44, cx0 + bw // 2 + 22, by0 + 60],
              fill=(167, 243, 208))
    kicker(d, (cx0 + 14, by0 + 86), "ANTALYA  •  CLIMATE", color=TEAL, size=18)
    d.text((cx0 + 14, by0 + 110), "TALKS STALL",
           font=fit(d, "TALKS STALL", 25, bw - 28), fill=INK)
    text_block(d, (cx0 + 14, by0 + 142),
               "COP31 runs past its Friday deadline; draft drops the "
               "fossil-fuel phase-out.",
               font(17), INK, bw - 28, leading=22)
    # Markets
    mx0 = cx0 + bw + 16
    panel(d, (mx0, by0, mx0 + bw, by1), (255, 255, 255))
    for gy in (by0 + 16, by0 + 36, by0 + 56):
        d.line([mx0 + 14, gy, mx0 + bw - 14, gy], fill=(220, 220, 220), width=1)
    pts = [(mx0 + 16, by0 + 14), (mx0 + 80, by0 + 26), (mx0 + 150, by0 + 22),
           (mx0 + 220, by0 + 46), (mx0 + bw - 20, by0 + 68)]
    d.line(pts, fill=RED, width=5, joint="curve")
    d.polygon([(mx0 + bw - 20, by0 + 68), (mx0 + bw - 34, by0 + 56),
               (mx0 + bw - 40, by0 + 70)], fill=RED)
    kicker(d, (mx0 + 14, by0 + 86), "MARKETS", size=18)
    d.text((mx0 + 14, by0 + 110), "MARKETS SLIDE",
           font=fit(d, "MARKETS SLIDE", 25, bw - 28), fill=INK)
    text_block(d, (mx0 + 14, by0 + 142),
               "S&P 500 falls 3.7% into correction as AI shares sell off.",
               font(17), INK, bw - 28, leading=22)

    # ---- footer ----------------------------------------------------
    d.text((24, 970), "FRIDAY 20 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE",
           font=font(17, bold=True), fill=GREY)
    fx = W - 24 - d.textlength("SIX STORIES  •  ONE DAY", font=font(17, bold=True))
    d.text((fx, 970), "SIX STORIES  •  ONE DAY", font=font(17, bold=True), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
