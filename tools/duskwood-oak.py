"""Generate a gnarled old oak silhouette as tapered filled SVG paths.

Usage: python oak.py <seed> <max_depth> <out.svg> [moon]
Prints only the file name. The tree is auto-fitted into the frame.
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

fit_pts = []  # every outline point, pruned or not, so variants fit identically
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
    fit_pts.extend(left + right)
    if max(w0, w1) < min_w:
        return
    shapes.append(left + right[::-1])
    shapes.append(("circle", p1, w1 / 2))


def branch(p, ang, length, width, depth):
    segs = 2 if depth < max_depth else 1
    cur, a, w = p, ang, width
    side = 1 if ang > UP else -1
    for s in range(segs):
        a += rng.uniform(-0.32, 0.32)
        # an old oak's limbs reach outwards and level off
        if depth >= 2:
            target = UP + side * 1.15
            a += (target - a) * 0.18
        a = max(-math.pi + 0.08, min(-0.08, a))
        l = length / segs
        nxt = (cur[0] + math.cos(a) * l, cur[1] + math.sin(a) * l)
        w2 = w * (0.88 if s < segs - 1 else 0.8)
        tapered(cur, nxt, w, w2, rng.uniform(-0.2, 0.2))
        cur, w = nxt, w2
    if depth >= max_depth:
        hook = a + rng.choice([-1, 1]) * rng.uniform(0.9, 1.5)
        tip = (cur[0] + math.cos(hook) * length * 0.4, cur[1] + math.sin(hook) * length * 0.4)
        tapered(cur, tip, w, 0.2, rng.uniform(-0.35, 0.35))
        return
    kids = 2 if depth < 2 else rng.choice([2, 2, 3])
    for k in range(kids):
        off = (k - (kids - 1) / 2) * rng.uniform(0.55, 0.85)
        ca = a + off
        cl = length * rng.uniform(0.68, 0.8)
        branch(cur, ca, cl, w * rng.uniform(0.66, 0.76), depth + 1)


# trunk: short, massive, slightly twisting
base = (0.0, 0.0)
mid = (rng.uniform(-3, 3), -18)
top = (rng.uniform(-2, 2), -34)
tapered(base, mid, 30, 22, rng.uniform(-0.15, 0.15))
tapered(mid, top, 22, 18, rng.uniform(-0.15, 0.15))
# split straight into heavy limbs
for ang, ln, wd in [(UP - 1.0, 40, 12), (UP - 0.15, 34, 10), (UP + 0.95, 42, 12)]:
    branch(top, ang + rng.uniform(-0.1, 0.1), ln, wd, 1)
# roots gripping the ground
for ang, ln, wd in [(math.pi - 0.1, 26, 11), (0.1, 28, 11), (math.pi - 0.5, 15, 7), (0.45, 16, 7)]:
    p0 = (math.cos(ang) * 6, -5)
    p1 = (p0[0] + math.cos(ang) * ln, 0)
    tapered(p0, p1, wd, 0.6, rng.uniform(-0.12, 0.05))

# fit into frame: x 6..194, y 8..base at 172
pts = fit_pts
minx = min(p[0] for p in pts); maxx = max(p[0] for p in pts)
miny = min(p[1] for p in pts); maxy = max(p[1] for p in pts)
scale = min(188 / (maxx - minx), 164 / (maxy - miny))
cx = (minx + maxx) / 2


def tf(p):
    return (100 + (p[0] - cx) * scale, 172 + (p[1] - maxy) * scale)


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

moon = ""
if with_moon:
    moon = f'<circle cx="100" cy="88" r="64" fill="none" stroke="currentColor" stroke-width="{ring_w:g}"/>\n  '
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 180" color="#64ffda">\n  '
    + moon
    + f'<path fill="currentColor" d="{" ".join(parts)}"/>\n</svg>\n'
)
open(out, "w", newline="\n").write(svg)
print(out)
