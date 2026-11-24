"""Build-time renderer for the news-image-20261124 front page.

Draws a 1024x1024 photo-led front page with Pillow (build time only;
the shipped entry program main.py just copies the PNG, stdlib only).
Deterministic: fixed palette, fixed geometry, no randomness, no
network, no timestamps in the PNG (Pillow writes no time chunk).
Run:  python3 render.py   (writes entry.png next to this file)
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = font("DejaVuSerif-Bold.ttf", 62)
SANS_B = font("DejaVuSans-Bold.ttf", 30)
SANS_B_SM = font("DejaVuSans-Bold.ttf", 22)
SANS = font("DejaVuSans.ttf", 20)
SANS_SM = font("DejaVuSans.ttf", 17)
SANS_XS = font("DejaVuSans.ttf", 15)
DATE_F = font("DejaVuSans-Bold.ttf", 34)
TAG_F = font("DejaVuSans-Bold.ttf", 19)

PAPER = (246, 241, 229)
NAVY = (15, 42, 74)
GOLD = (212, 175, 55)
INK = (20, 20, 20)


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel_shell(draw, x, y, w, h, tag, tag_bg):
    draw.rectangle([x, y, x + w, y + h], outline=(90, 80, 60), width=2)
    tw = draw.textlength(tag, font=TAG_F) + 18
    draw.rectangle([x, y, x + tw, y + 30], fill=tag_bg)
    draw.text((x + 9, y + 4), tag, font=TAG_F, fill=(255, 255, 255))


def headline(draw, x, y, w, text, size=27):
    fnt = font("DejaVuSans-Bold.ttf", size)
    lines = wrap(draw, text, fnt, w)
    yy = y
    for ln in lines:
        draw.text((x, yy), ln, font=fnt, fill=(255, 255, 255))
        yy += size + 4
    return yy


def draw_sea(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + 130), (255, 190, 110), (140, 170, 210))
    d.ellipse([x + w - 110, y + 18, x + w - 50, y + 78], fill=(255, 214, 90))
    vgrad(d, (x, y + 130, x + w, y + h), (38, 90, 140), (16, 48, 88))
    # waves
    for i, wy in enumerate((y + 150, y + 175, y + 198)):
        for k in range(5):
            wx = x + 20 + k * 100 + (i * 37) % 60
            d.arc([wx, wy, wx + 60, wy + 18], 180, 360, fill=(190, 215, 235), width=3)
    # corvette silhouette
    hx, hy = x + 60, y + 168
    d.polygon([(hx, hy), (hx + 300, hy), (hx + 330, hy + 26),
               (hx + 20, hy + 26)], fill=(32, 38, 46))
    d.rectangle([hx + 90, hy - 26, hx + 210, hy], fill=(44, 52, 62))
    d.rectangle([hx + 150, hy - 52, hx + 168, hy - 26], fill=(44, 52, 62))
    d.line([(hx + 159, hy - 52), (hx + 159, hy - 78)], fill=(44, 52, 62), width=4)
    d.rectangle([hx + 220, hy - 18, hx + 244, hy], fill=(70, 76, 84))
    # blast burst at the bow
    bx, by = hx + 340, hy - 6
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 10, 30
        a = math.radians(ang)
        d.line([(bx + r1 * math.cos(a), by + r1 * math.sin(a)),
                (bx + r2 * math.cos(a), by + r2 * math.sin(a))],
               fill=(255, 140, 40), width=5)
    d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 190, 60))
    # sea drone quadcopter
    dx, dy = x + w - 120, y + 105
    d.ellipse([dx - 16, dy - 8, dx + 16, dy + 8], fill=(20, 20, 20))
    for sx in (-34, 34):
        d.line([(dx + sx - 16, dy - 10), (dx + sx + 16, dy - 10)],
               fill=(20, 20, 20), width=3)
        d.line([(dx + sx, dy - 8), (dx, dy - 4)], fill=(20, 20, 20), width=3)
    d.ellipse([dx - 5, dy + 8, dx + 5, dy + 16], fill=(200, 40, 30))


def draw_cop(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (250, 200, 120), (214, 140, 60))
    d.ellipse([x + w // 2 - 62, y + 22, x + w // 2 + 62, y + 146],
              fill=(255, 120, 30))
    # conference hall silhouette
    d.rectangle([x + 40, y + 150, x + w - 40, y + 196], fill=(70, 48, 30))
    d.polygon([(x + 150, y + 150), (x + w // 2, y + 108), (x + w - 150, y + 150)],
              fill=(90, 62, 38))
    # flags row
    for i in range(7):
        fx = x + 60 + i * 58
        d.line([(fx, y + 120), (fx, y + 150)], fill=(40, 28, 18), width=3)
        d.polygon([(fx, y + 120), (fx + 26, y + 128), (fx, y + 136)],
                  fill=(150, 30, 30) if i % 2 == 0 else (30, 90, 150))
    # cracked earth
    d.rectangle([x, y + 196, x + w, y + h], fill=(120, 74, 40))
    for (x1, y1, x2, y2) in [(x + 40, y + 200, x + 130, y + 232),
                             (x + 130, y + 232, x + 90, y + 250),
                             (x + 260, y + 200, x + 300, y + 240),
                             (x + 300, y + 240, x + 380, y + 226),
                             (x + 420, y + 200, x + 400, y + 248)]:
        d.line([(x1, y1), (x2, y2)], fill=(60, 34, 18), width=4)


def draw_nato(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 24, 46))
    cx, cy = x + w // 2, y + 118
    for r, col in ((92, (40, 120, 70)), (66, (50, 150, 90)), (40, (70, 190, 110))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
    d.line([(cx, cy), (cx + 88, cy - 40)], fill=(90, 220, 130), width=3)
    d.line([(cx - 92, cy), (cx + 92, cy)], fill=(40, 120, 70), width=1)
    d.line([(cx, cy - 92), (cx, cy + 92)], fill=(40, 120, 70), width=1)
    # missile / drone trails arcing in
    d.arc([x + 20, y - 40, x + 260, y + 200], 300, 60, fill=(255, 255, 255), width=3)
    d.arc([x + w - 280, y - 60, x + w - 20, y + 180], 120, 240, fill=(255, 200, 60), width=3)
    d.ellipse([x + 235, y + 30, x + 247, y + 42], fill=(255, 255, 255))
    d.ellipse([x + w - 250, y + 22, x + w - 238, y + 34], fill=(255, 200, 60))
    # jet silhouette
    jx, jy = x + w - 150, y + 165
    d.polygon([(jx, jy), (jx + 70, jy - 12), (jx + 96, jy), (jx + 70, jy + 12)],
              fill=(180, 190, 205))
    d.polygon([(jx + 30, jy - 6), (jx + 52, jy - 26), (jx + 58, jy - 6)],
              fill=(180, 190, 205))
    # red alert triangle
    ax, ay = x + 30, y + 150
    d.polygon([(ax, ay), (ax + 44, ay), (ax + 22, ay + 38)], fill=(220, 40, 30))
    d.text((ax + 18, ay + 8), "!", font=font("DejaVuSans-Bold.ttf", 24),
           fill=(255, 255, 255))


def draw_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 26, 14))
    # circuit traces
    for (x1, y1, x2, y2) in [(x + 20, y + 40, x + 150, y + 40),
                             (x + 150, y + 40, x + 150, y + 120),
                             (x + w - 20, y + 180, x + w - 160, y + 180),
                             (x + w - 160, y + 180, x + w - 160, y + 90),
                             (x + 30, y + 200, x + 120, y + 200),
                             (x + w - 30, y + 30, x + w - 120, y + 30)]:
        d.line([(x1, y1), (x2, y2)], fill=(40, 160, 80), width=3)
    for (nx, ny) in [(150, 40), (150, 120), (w - 160, 180), (w - 160, 90),
                     (120, 200), (w - 120, 30)]:
        d.ellipse([x + nx - 6, y + ny - 6, x + nx + 6, y + ny + 6],
                  fill=(120, 220, 140))
    # chip
    cx, cy = x + w // 2 - 70, y + 78
    d.rectangle([cx, cy, cx + 140, cy + 110], fill=(18, 60, 30),
                outline=(118, 185, 0), width=4)
    d.rectangle([cx + 28, cy + 28, cx + 112, cy + 82], fill=(118, 185, 0))
    d.text((cx + 38, cy + 44), "NVIDIA", font=font("DejaVuSans-Bold.ttf", 20),
           fill=(8, 26, 14))
    # rising chart arrow
    pts = [(x + 40, y + 215), (x + 150, y + 185), (x + 250, y + 195),
           (x + 350, y + 140), (x + 450, y + 95)]
    d.line(pts, fill=(140, 230, 90), width=6, joint="curve")
    d.polygon([(x + 450, y + 95), (x + 424, y + 92), (x + 448, y + 122)],
              fill=(140, 230, 90))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=SERIF_B)) / 2, 12), title,
           font=SERIF_B, fill=(255, 255, 255))
    date = "TUESDAY  •  24 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=DATE_F)) / 2, 92), date,
           font=DATE_F, fill=GOLD)
    kicker = "Four stories that defined the day — from Libya to Antalya, Brussels and Wall Street"
    d.text(((W - d.textlength(kicker, font=SANS)) / 2, 162), kicker,
           font=SANS, fill=(60, 55, 45))

    # ---- 2x2 photo panels ----
    px, py, pw, ph = 16, 192, 490, 300
    gap = 12
    panels = [
        (px, py, "LEAD", (178, 34, 34), draw_sea,
         "SEA DRONE HITS RUSSIAN CORVETTE OFF BENGHAZI, LIBYA"),
        (px + pw + gap, py, "CLIMATE", (34, 110, 60), draw_cop,
         "COP31 COLLAPSES: 90+ NATIONS REJECT DRAFT WITH NO 'FOSSIL FUELS'"),
        (px, py + ph + gap, "SECURITY", (40, 60, 120), draw_nato,
         "NATO: 25 AIRSPACE VIOLATIONS IN 2026 — DEBRIS IN POLAND, 20 NOV"),
        (px + pw + gap, py + ph + gap, "MARKETS", (30, 120, 40), draw_nvidia,
         "HUANG BACK AS NVIDIA CEO — NASDAQ +6.51%"),
    ]
    for (x, y, tag, tbg, draw_fn, head) in panels:
        draw_fn(d, x, y, pw, 200)
        d.rectangle([x, y + 200, x + pw, y + ph], fill=(24, 24, 28))
        headline(d, x + 12, y + 210, pw - 24, head)
        panel_shell(d, x, y, pw, ph, tag, tbg)

    # ---- bottom strip: three more stories ----
    sy = py + 2 * ph + gap + 12  # 816
    d.rectangle([16, sy, W - 16, 1008], fill=(18, 32, 48))
    d.text((28, sy + 10), "ALSO TODAY", font=TAG_F, fill=GOLD)
    items = [
        ("US–IRAN", "US Treasury sanctions; Qatar mediates talks"),
        ("ROHINGYA AT ICJ", "14 states back the case against Myanmar"),
        ("NEPAL QUAKE", "Magnitude 5.6 earthquake shakes Nepal"),
    ]
    col_w = (W - 32 - 24) // 3
    for i, (t, body) in enumerate(items):
        cx = 28 + i * col_w
        d.rectangle([cx, sy + 44, cx + 10, sy + 54], fill=GOLD)
        d.text((cx + 18, sy + 38), t, font=SANS_B_SM, fill=(255, 255, 255))
        for j, ln in enumerate(wrap(d, body, SANS_SM, col_w - 24)):
            d.text((cx + 18, sy + 66 + j * 22), ln, font=SANS_SM,
                   fill=(205, 210, 220))
        if i < 2:
            d.line([(cx + col_w - 8, sy + 40), (cx + col_w - 8, sy + 170)],
                   fill=(70, 90, 110), width=1)
    d.text((28, 992), "THE WORLD TODAY — 24 NOVEMBER 2026",
           font=SANS_XS, fill=(140, 150, 165))

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
