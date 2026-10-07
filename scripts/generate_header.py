from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

OUT = Path("assets/mission-briefing.gif")
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 1000, 300
BG = (5, 7, 8)
FG = (218, 224, 220)
MUTED = (108, 120, 116)
GREEN = (70, 200, 120)
BORDER = (55, 65, 62)
SCAN = (35, 70, 60)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FS = ImageFont.truetype(FONT_PATH, 13)
FM = ImageFont.truetype(FONT_PATH, 18)
FN = ImageFont.truetype(FONT_PATH, 25)

lines = [
    ("> ESTABLISHING ENCRYPTED CHANNEL...", FG, 60, 82, FM),
    ("> VERIFYING IDENTITY............. COMPLETE", MUTED, 60, 118, FM),
    ("> ACCESS GRANTED", GREEN, 60, 154, FM),
    ("KAMAL SANGAMESWARAN", FG, 60, 198, FN),
    ("SOFTWARE ENGINEER // AI/ML // CLOUD // SIMULATION", FG, 60, 234, FM),
    ("CURRENT ASSIGNMENT: UVA SOLAR CAR // SIMULATION TEAM LEAD", MUTED, 60, 266, FS),
]

def draw_reticle(d, cx, cy, r, angle_step):
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=4, width=1)
    d.line((cx-r-8, cy, cx+r+8, cy), fill=4, width=1)
    d.line((cx, cy-r-8, cx, cy+r+8), fill=4, width=1)
    # tiny rotating tick pair
    offsets = [(r-3,0),(0,r-3),(-r+3,0),(0,-r+3)]
    ox, oy = offsets[angle_step % 4]
    d.ellipse((cx+ox-2, cy+oy-2, cx+ox+2, cy+oy+2), fill=3)

def make(progress, cursor_line=None, cursor_on=True, scan_x=None, reticle_step=0, final=False):
    im = Image.new("P", (W, H), 0)
    palette = [*BG, *FG, *MUTED, *GREEN, *BORDER, *SCAN] + [0, 0, 0] * 250
    im.putpalette(palette[:768])
    d = ImageDraw.Draw(im)

    d.rectangle((18, 14, W - 18, H - 14), outline=4, width=1)
    d.text((38, 30), "Q BRANCH TERMINAL // KAMAL-UVA", font=FS, fill=2)
    d.text((W - 210, 30), "FOR YOUR EYES ONLY", font=FS, fill=2)
    d.line((38, 56, W - 38, 56), fill=4, width=1)

    # clearance indicator
    d.ellipse((W-92, 64, W-82, 74), fill=3)
    d.text((W-185, 60), "CLEARANCE", font=FS, fill=2)

    draw_reticle(d, W-90, H-70, 20, reticle_step)

    if scan_x is not None:
        d.line((scan_x, 58, scan_x, H-28), fill=5, width=2)

    colors = {FG: 1, MUTED: 2, GREEN: 3}
    for i, (txt, col, x, y, ft) in enumerate(lines):
        p = progress[i]
        shown = txt[:math.ceil(len(txt) * p)]
        d.text((x, y), shown, font=ft, fill=colors[col])
        if cursor_line == i and cursor_on:
            bb = d.textbbox((x, y), shown, font=ft)
            d.rectangle((bb[2] + 4, y + 2, bb[2] + 10, y + ft.size - 1), fill=1)

    if final:
        d.text((60, 286), "> MISSION BRIEFING READY_", font=FS, fill=3)

    return im

frames, durations = [], []
progress = [0.0] * len(lines)

# opening scanner + reticle motion
for k in range(8):
    sx = 40 + int((W-80) * (k / 7))
    frames.append(make(progress, scan_x=sx, reticle_step=k))
    durations.append(140)

# type each line more slowly
for i in range(len(lines)):
    for p in (0.25, 0.50, 0.75, 1.0):
        state = progress.copy()
        state[i] = p
        frames.append(make(state, i, True, reticle_step=i))
        durations.append(180 if i != 3 else 220)
    progress[i] = 1.0

# final hold with subtle motion + cursor blink: ~4.8 sec
for k in range(12):
    frames.append(make([1.0]*len(lines), cursor_line=5, cursor_on=(k%2==0), reticle_step=k, final=True))
    durations.append(400)

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
