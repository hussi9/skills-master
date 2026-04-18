#!/usr/bin/env python3
"""
skills-master LinkedIn image — clean stats infographic.
1200x628 (LinkedIn optimal). No diagram. Just numbers and contrast.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 628
img = Image.new('RGB', (W, H), (10, 12, 18))
draw = ImageDraw.Draw(img)

FD = '/Users/airbook/.claude/skills/canvas-design/canvas-fonts/'
def f(n, s): return ImageFont.truetype(FD + n, s)

F_HUGE  = f('BricolageGrotesque-Bold.ttf',   96)
F_BIG   = f('BricolageGrotesque-Bold.ttf',   48)
F_MED   = f('BricolageGrotesque-Regular.ttf', 22)
F_BODY  = f('Outfit-Regular.ttf',             18)
F_LABEL = f('Outfit-Regular.ttf',             14)
F_MONO  = f('JetBrainsMono-Regular.ttf',      13)
F_TAG   = f('Outfit-Bold.ttf',                13)

# Colors
BG      = (10,  12,  18)
GOLD    = (212, 175, 55)
WHITE   = (240, 238, 232)
DIM     = (90,  92,  102)
RED     = (220, 80,  80)
GREEN   = (80,  200, 120)
CARD_BG = (16,  20,  30)
BORDER  = (30,  34,  48)

def t(x, y, txt, fn, col, anchor='lt'):
    bb = draw.textbbox((0,0), txt, font=fn)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    if anchor == 'center':
        draw.text((x - tw//2, y - th//2), txt, font=fn, fill=col)
    elif anchor == 'rt':
        draw.text((x - tw, y), txt, font=fn, fill=col)
    else:
        draw.text((x, y), txt, font=fn, fill=col)

def rect(x, y, w, h, fill=None, outline=None, radius=8):
    draw.rounded_rectangle([(x,y),(x+w,y+h)], radius=radius, fill=fill, outline=outline)

# ── Left panel (dark) ─────────────────────────────────────────────────────────
# Thin gold left bar
draw.rectangle([(0,0),(4,H)], fill=GOLD)

# Main headline
t(48, 56, 'skills-master', F_BIG, WHITE)
t(48, 116, 'Fix how Claude Code picks skills.', F_MED, DIM)
t(48, 146, 'One file. Zero config. 90% accuracy.', F_MED, GOLD)

# Divider
draw.line([(48, 188),(420, 188)], fill=BORDER, width=1)

# Before / After
t(48, 204, 'BEFORE', F_TAG, RED)
t(48, 224, '"500 error in prod" →', F_BODY, DIM)
t(48, 248, 'Claude fires brainstorming.', F_BODY, DIM)
t(48, 272, 'Spends 3 turns ideating. Wrong model.', F_BODY, DIM)

draw.line([(48, 306),(420, 306)], fill=BORDER, width=1)

t(48, 322, 'AFTER', F_TAG, GREEN)
t(48, 342, '"500 error in prod" →', F_BODY, WHITE)
t(48, 366, 'Q1: broken → systematic-debugging', F_MONO, GOLD)
t(48, 390, '+ sonnet. Fix in one pass.', F_BODY, WHITE)

# Install block
draw.line([(48, 430),(420, 430)], fill=BORDER, width=1)
t(48, 448, 'INSTALL', F_TAG, DIM)
draw.rectangle([(48, 468),(420, 510)], fill=(16,20,30), outline=BORDER)
t(60, 480, 'curl -sL .../SKILL.md > ~/.claude/skills/', F_MONO, DIM)
t(60, 498, 'skills-master/SKILL.md', F_MONO, GOLD)

t(48, 526, 'github.com/hussi9/skills-master', F_LABEL, DIM)

# ── Right panel (stats) ───────────────────────────────────────────────────────
RX = 480
draw.rectangle([(RX, 0),(W, H)], fill=(13,16,24))

# Panel title
t(RX + 40, 56, 'Real numbers from 20 tasks', F_LABEL, DIM)
draw.line([(RX+40, 80),(W-40, 80)], fill=BORDER, width=1)

# Big stat cards
cards = [
    ('90%',    'routing accuracy',        'overall path + skill + model',  GOLD),
    ('20-30%', 'of the time Claude',      'picks the wrong skill today',   RED),
    ('10s',    'to route any task',       '3 questions, deterministic',    GREEN),
    ('2,700+', 'skills available',        'Antigravity · Composio · GitHub', WHITE),
]

cy = 100
for val, label, sub, col in cards:
    rect(RX+32, cy, W-RX-64, 108, fill=CARD_BG, outline=BORDER)

    # Big number
    bb = draw.textbbox((0,0), val, font=F_HUGE)
    vw = bb[2]-bb[0]
    draw.text((RX+48, cy+10), val, font=F_HUGE, fill=col)

    # Labels right side
    lx = RX + 48 + vw + 20
    bb2 = draw.textbbox((0,0), label, font=F_MED)
    lh = bb2[3]-bb2[1]
    draw.text((lx, cy+22), label, font=F_MED, fill=WHITE)
    draw.text((lx, cy+22+lh+6), sub, font=F_LABEL, fill=DIM)

    cy += 120

# Bottom note
t(RX+32, cy+8, '48 installs in week 1 · no star prompt · word of mouth only', F_LABEL, DIM)

# ── Save ──────────────────────────────────────────────────────────────────────
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skills-master-visual.png')
img.save(out, 'PNG', dpi=(144,144))
print(f'Saved: {out}  [{W}×{H}]')
