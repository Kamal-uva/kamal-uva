from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

OUT = Path("assets/mission-briefing.gif")
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 900, 240
BG = (5, 7, 8)
FG = (218, 224, 220)
MUTED = (108, 120, 116)
RED = (185, 45, 45)
BORDER = (55, 65, 62)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FS = ImageFont.truetype(FONT_PATH, 12)
FM = ImageFont.truetype(FONT_PATH, 17)
FN = ImageFont.truetype(FONT_PATH, 23)

lines = [
    ("> ESTABLISHING SECURE CONNECTION...", FG, 58, 68, FM),
    ("> IDENTITY CONFIRMED", RED, 58, 98, FM),
    ("KAMAL SANGAMESWARAN", FG, 58, 135, FN),
    ("SOFTWARE ENGINEER // AI // CLOUD // SIMULATION", FG, 58, 173, FM),
    ("> LOADING MISSION BRIEFING...", MUTED, 58, 202, FM),
]

def make(progress, cursor_line=None, cursor_on=True):
    im = Image.new("P", (W, H), 0)
    palette = [*BG, *FG, *MUTED, *RED, *BORDER] + [0, 0, 0] * 251
    im.putpalette(palette[:768])
    d = ImageDraw.Draw(im)
    d.rectangle((18, 14, W - 18, H - 14), outline=4, width=1)
    d.text((38, 30), "SECURE TERMINAL // KAMAL-UVA", font=FS, fill=2)
    d.text((W - 190, 30), "SESSION: ACTIVE", font=FS, fill=2)
    d.line((38, 52, W - 38, 52), fill=4, width=1)
    colors = {FG: 1, MUTED: 2, RED: 3}
    for i, (txt, col, x, y, ft) in enumerate(lines):
        p = progress[i]
        shown = txt[:math.ceil(len(txt) * p)]
        d.text((x, y), shown, font=ft, fill=colors[col])
        if cursor_line == i and cursor_on:
            bb = d.textbbox((x, y), shown, font=ft)
            d.rectangle((bb[2] + 4, y + 2, bb[2] + 10, y + ft.size - 1), fill=1)
    return im

frames, durations = [], []
progress = [0.0] * len(lines)
for i in range(len(lines)):
    for p in (0.34, 0.68, 1.0):
        state = progress.copy()
        state[i] = p
        frames.append(make(state, i, True))
        durations.append(110 if i != 2 else 140)
    progress[i] = 1.0

for k in range(6):
    frames.append(make([1.0] * len(lines), 4, k % 2 == 0))
    durations.append(300)

frames[0].save(
    OUT,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=True,
    disposal=2,
)
print(f"Generated {OUT}")
