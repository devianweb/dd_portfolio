"""Generate a gnarled old oak silhouette as tapered filled SVG paths.

Usage: python duskwood-oak.py <seed> <max_depth> <out.svg> [moon] [min_twig_width] [ring_width]
Prints only the file name. The crown is grown to stay inside the moon; only the
trunk and roots pass through its lower rim.
"""
import math
import random
import sys

seed = int(sys.argv[1])
max_depth = int(sys.argv[2])
out = sys.argv[3]
with_moon = len(sys.argv) > 4 and sys.argv[4] == "moon"
min_w = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0  # prune twigs thinner than this
ring_w = float(sys.argv[6]) if len(sys.argv) > 6 else 3.0
rng = random.Random(seed)

# the moon, in final SVG units (viewBox 0 0 200 180)
MX, MY, MR = 100, 84, 66
RIM_CRATER = (28, 12)  # (angle in degrees, clockwise from 3 o'clock; radius)
# optional extra craters, (dx, dy, r) from moon centre, drawn as open arcs lit from the right
INNER_CRATERS = []
# tree units -> SVG units: trunk base sits on the ground at (100, 172)
SCALE, BASE_X, BASE_Y = 0.6, 100, 172
RIM_GAP = 5  # keep twigs this far inside the rim (SVG units)

shapes = []  # list of polygons (list of points) or ("circle", c, r)
UP = -math.pi / 2


def bez(p0, c, p1, t):
    return (
        (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
        (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1],
    )


def tapered(p0, p1, w0, w1, bend):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    c = ((p0[0] + p1[0]) / 2 + nx * bend * L, (p0[1] + p1[1]) / 2 + ny * bend * L)
    n = 8
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(p0, c, p1, t)
        tx = 2 * (1 - t) * (c[0] - p0[0]) + 2 * t * (p1[0] - c[0])
        ty = 2 * (1 - t) * (c[1] - p0[1]) + 2 * t * (p1[1] - c[1])
        tl = math.hypot(tx, ty) or 1
        ox, oy = -ty / tl, tx / tl
        w = (w0 + (w1 - w0) * t) / 2
        left.append((x + ox * w, y + oy * w))
        right.append((x - ox * w, y - oy * w))
    if max(w0, w1) < min_w:
        return
    shapes.append(left + right[::-1])
    shapes.append(("circle", p1, w1 / 2))


def tree_to_svg(p):
    return BASE_X + p[0] * SCALE, BASE_Y + p[1] * SCALE


_ca = math.radians(RIM_CRATER[0])
_cd = MR - RIM_CRATER[1] * 0.25
BITE = (MX + math.cos(_ca) * _cd, MY + math.sin(_ca) * _cd, RIM_CRATER[1])


def inside(p, half_w):
    """Is this tree point (plus half its branch width) clear of the moon's rim and bite?"""
    x, y = tree_to_svg(p)
    m = RIM_GAP + half_w * SCALE
    if math.hypot(x - MX, y - MY) > MR - m:
        return False
    return math.hypot(x - BITE[0], y - BITE[1]) > BITE[2] + m


def grow(cur, a, l, half_w):
    """Step from cur at angle a; steer towards the moon's centre, then shorten, to stay inside.

    Deterministic, so the random sequence (and so the tree) doesn't change."""
    centre = ((MX - BASE_X) / SCALE, (MY - BASE_Y) / SCALE)
    for _ in range(14):
        nxt = (cur[0] + math.cos(a) * l, cur[1] + math.sin(a) * l)
        if inside(nxt, half_w):
            return nxt, a
        to_c = math.atan2(centre[1] - cur[1], centre[0] - cur[0])
        d = (to_c - a + math.pi) % (2 * math.pi) - math.pi
        a += max(-0.14, min(0.14, d))
    for _ in range(8):
        l *= 0.7
        nxt = (cur[0] + math.cos(a) * l, cur[1] + math.sin(a) * l)
        if inside(nxt, half_w):
            return nxt, a
    return cur, a


def branch(p, ang, length, width, depth):
    segs = 2 if depth < max_depth else 1
    cur, a, w = p, ang, width
    side = 1 if ang > UP else -1
    for s in range(segs):
        a += rng.uniform(-0.32, 0.32)
        # limbs lean outwards but keep climbing: a tall, grand oak
        if depth >= 2:
            target = UP + side * 0.5
            a += (target - a) * 0.12
        a = max(-math.pi + 0.08, min(-0.08, a))
        w2 = w * (0.88 if s < segs - 1 else 0.8)
        nxt, a = grow(cur, a, length / segs, w2 / 2)
        tapered(cur, nxt, w, w2, rng.uniform(-0.2, 0.2))
        cur, w = nxt, w2
    if depth >= max_depth:
        hook = a + rng.choice([-1, 1]) * rng.uniform(0.9, 1.5)
        tip, _ = grow(cur, hook, length * 0.4, 0.1)
        tapered(cur, tip, w, 0.2, rng.uniform(-0.35, 0.35))
        return
    kids = 2 if depth < 2 else rng.choice([2, 2, 3])
    for k in range(kids):
        off = (k - (kids - 1) / 2) * rng.uniform(0.55, 0.85)
        ca = a + off
        cl = length * rng.uniform(0.68, 0.8)
        branch(cur, ca, cl, w * rng.uniform(0.66, 0.76), depth + 1)


# trunk: massive, tall, slightly twisting
base = (0.0, 0.0)
mid = (rng.uniform(-4, 4), -34)
top = (rng.uniform(-3, 3), -68)
tapered(base, mid, 30, 22, rng.uniform(-0.15, 0.15))
tapered(mid, top, 22, 17, rng.uniform(-0.15, 0.15))
# split into heavy limbs that climb
for ang, ln, wd in [(UP - 0.5, 46, 12), (UP - 0.04, 50, 10), (UP + 0.46, 46, 12)]:
    branch(top, ang + rng.uniform(-0.1, 0.1), ln, wd, 1)
# roots gripping the ground
for ang, ln, wd in [(math.pi - 0.1, 26, 11), (0.1, 28, 11), (math.pi - 0.5, 15, 7), (0.45, 16, 7)]:
    p0 = (math.cos(ang) * 6, -5)
    p1 = (p0[0] + math.cos(ang) * ln, 0)
    tapered(p0, p1, wd, 0.6, rng.uniform(-0.12, 0.05))

tf = tree_to_svg
scale = SCALE


def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


parts = []
for s in shapes:
    if s[0] == "circle":
        _, c, r = s
        r *= scale
        if r > 0.2:
            x, y = tf(c)
            parts.append(f"M{fmt(x-r)} {fmt(y)}a{fmt(r)} {fmt(r)} 0 1 0 {fmt(2*r)} 0a{fmt(r)} {fmt(r)} 0 1 0 {fmt(-2*r)} 0z")
        continue
    parts.append("M" + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in map(tf, s)) + "z")

# the moon: a ring broken by a crater on its rim

def pt(a, r):
    return MX + math.cos(a) * r, MY + math.sin(a) * r


moon = ""
if with_moon:
    ca, cr = math.radians(RIM_CRATER[0]), RIM_CRATER[1]
    cd = MR - cr * 0.25  # crater centre just inside the rim
    gap = math.acos((MR * MR + cd * cd - cr * cr) / (2 * MR * cd))
    (x0, y0), (x1, y1) = pt(ca + gap, MR), pt(ca - gap, MR)
    ccx, ccy = pt(ca, cd)
    def crater_arc(x, y, r):
        # just the shadowed upper-left wall of the hollow, so it doesn't read as a bubble
        a0, a1 = math.radians(150), math.radians(300)
        sx, sy = x + math.cos(a0) * r, y + math.sin(a0) * r
        ex, ey = x + math.cos(a1) * r, y + math.sin(a1) * r
        return f"M{fmt(sx)} {fmt(sy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(ex)} {fmt(ey)}"

    craters = " ".join(crater_arc(MX + dx, MY + dy, r) for dx, dy, r in INNER_CRATERS)
    # rim: the long way round the moon, then dip inwards along the crater's edge
    rim = (
        f"M{fmt(x0)} {fmt(y0)}A{MR} {MR} 0 1 1 {fmt(x1)} {fmt(y1)}"
        f"A{fmt(cr)} {fmt(cr)} 0 0 0 {fmt(x0)} {fmt(y0)}"
    )
    moon = (
        f'<g fill="none" stroke="currentColor" stroke-width="{ring_w:g}" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="{rim}"/>'
        + (f'<path stroke-width="{ring_w * 0.6:g}" d="{craters}"/>' if craters else "")
        + "</g>\n  "
    )
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 180" color="#64ffda">\n  '
    + moon
    + f'<path fill="currentColor" d="{" ".join(parts)}"/>\n</svg>\n'
)
open(out, "w", newline="\n").write(svg)
print(out)
