"""Erzeugt die SVG-Skizzen für den Lernzettel und setzt sie in die HTML-Vorlage ein.

Aufruf: python3 sketches.py <vorlage.html> <ausgabe.html>
"""
import math
import sys

S = 40  # Pixel pro Einheit


class Plane:
    def __init__(self, uid, xmin, xmax, ymin, ymax, s=S, step=1):
        self.uid, self.xmin, self.xmax, self.ymin, self.ymax, self.s, self.step = (
            uid, xmin, xmax, ymin, ymax, s, step)
        self.pad = 26
        self.w = (xmax - xmin) * s + 2 * self.pad
        self.h = (ymax - ymin) * s + 2 * self.pad
        self.parts = []
        self.imfmt = lambda v: f"{fmt(v)}i"

    def X(self, x):
        return self.pad + (x - self.xmin) * self.s

    def Y(self, y):
        return self.pad + (self.ymax - y) * self.s

    def P(self, x, y):
        return f"{self.X(x):.1f},{self.Y(y):.1f}"

    def grid(self):
        p = []
        x = math.ceil(self.xmin)
        while x <= self.xmax:
            p.append(f'<line x1="{self.X(x):.1f}" y1="{self.Y(self.ymin):.1f}" x2="{self.X(x):.1f}" y2="{self.Y(self.ymax):.1f}" class="g"/>')
            x += 1
        y = math.ceil(self.ymin)
        while y <= self.ymax:
            p.append(f'<line x1="{self.X(self.xmin):.1f}" y1="{self.Y(y):.1f}" x2="{self.X(self.xmax):.1f}" y2="{self.Y(y):.1f}" class="g"/>')
            y += 1
        self.parts.insert(0, "\n".join(p))

    def axes(self):
        p = []
        ax, ay = self.Y(0), self.X(0)
        p.append(f'<line x1="{self.X(self.xmin):.1f}" y1="{ax:.1f}" x2="{self.X(self.xmax)+10:.1f}" y2="{ax:.1f}" class="ax"/>')
        p.append(f'<path d="M{self.X(self.xmax)+10:.1f},{ax:.1f} l-8,-4 v8 z" class="axh"/>')
        p.append(f'<line x1="{ay:.1f}" y1="{self.Y(self.ymin):.1f}" x2="{ay:.1f}" y2="{self.Y(self.ymax)-10:.1f}" class="ax"/>')
        p.append(f'<path d="M{ay:.1f},{self.Y(self.ymax)-10:.1f} l-4,8 h8 z" class="axh"/>')
        p.append(f'<text x="{self.X(self.xmax)+4:.1f}" y="{ax+18:.1f}" class="lre">Re</text>')
        p.append(f'<text x="{ay+8:.1f}" y="{self.Y(self.ymax)-2:.1f}" class="lim">Im</text>')
        x = math.ceil(self.xmin)
        while x <= self.xmax:
            if x != 0:
                p.append(f'<line x1="{self.X(x):.1f}" y1="{ax-4:.1f}" x2="{self.X(x):.1f}" y2="{ax+4:.1f}" class="ax"/>')
                p.append(f'<text x="{self.X(x):.1f}" y="{ax+16:.1f}" class="t" text-anchor="middle">{fmt(x)}</text>')
            x += self.step
        y = math.ceil(self.ymin)
        while y <= self.ymax:
            if y != 0:
                p.append(f'<line x1="{ay-4:.1f}" y1="{self.Y(y):.1f}" x2="{ay+4:.1f}" y2="{self.Y(y):.1f}" class="ax"/>')
                p.append(f'<text x="{ay-7:.1f}" y="{self.Y(y)+4:.1f}" class="t" text-anchor="end">{self.imfmt(y)}</text>')
            y += self.step
        self.parts.append("\n".join(p))

    def add(self, s):
        self.parts.append(s)

    def svg(self, label):
        hid = f"h-{self.uid}"
        defs = (f'<defs><pattern id="{hid}" width="7" height="7" patternUnits="userSpaceOnUse" '
                f'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" class="hl"/></pattern>'
                f'<clipPath id="c-{self.uid}"><rect x="{self.X(self.xmin):.1f}" y="{self.Y(self.ymax):.1f}" '
                f'width="{(self.xmax-self.xmin)*self.s:.1f}" height="{(self.ymax-self.ymin)*self.s:.1f}"/></clipPath></defs>')
        body = "\n".join(self.parts).replace("HATCH", f"url(#{hid})").replace("CLIP", f"url(#c-{self.uid})")
        return (f'<svg class="plane" viewBox="0 0 {self.w:.0f} {self.h:.0f}" role="img" aria-label="{label}">'
                f'{defs}{body}</svg>')


def fmt(v):
    if v == int(v):
        v = int(v)
        return "−" + str(-v) if v < 0 else str(v)
    return str(v)


def region(pl, d):
    pl.add(f'<path d="{d}" class="fill" clip-path="CLIP"/><path d="{d}" fill="HATCH" clip-path="CLIP"/>')


def circle_path(cx, cy, r, pl):
    return (f"M{pl.X(cx-r):.1f},{pl.Y(cy):.1f} a{r*pl.s:.1f},{r*pl.s:.1f} 0 1,0 {2*r*pl.s:.1f},0 "
            f"a{r*pl.s:.1f},{r*pl.s:.1f} 0 1,0 {-2*r*pl.s:.1f},0 z")


def dot(pl, x, y, text, dx=8, dy=-8, anchor="start"):
    pl.add(f'<circle cx="{pl.X(x):.1f}" cy="{pl.Y(y):.1f}" r="3.5" class="pt"/>'
           f'<text x="{pl.X(x)+dx:.1f}" y="{pl.Y(y)+dy:.1f}" class="pl" text-anchor="{anchor}">{text}</text>')


def sketch_parabola():
    pl = Plane("d1", -4.5, 4.5, -2, 4)
    pl.grid()
    xs = [pl.xmin + i * (pl.xmax - pl.xmin) / 90 for i in range(91)]
    pts = " L".join(pl.P(x, x * x / 4 - 1) for x in xs)
    region(pl, f"M{pts} L{pl.P(pl.xmax, pl.ymax+1)} L{pl.P(pl.xmin, pl.ymax+1)} Z")
    pl.add(f'<path d="M{pts}" class="edge" clip-path="CLIP"/>')
    pl.axes()
    dot(pl, 0, -1, "Scheitel (0 | −1)", 8, 16)
    dot(pl, -2, 0, "−2", -6, -8, "end")
    dot(pl, 2, 0, "2", 6, -8)
    pl.add(f'<text x="{pl.X(-3.9):.1f}" y="{pl.Y(3.4):.1f}" class="note">y ≥ x²/4 − 1</text>')
    return pl.svg("Fläche oberhalb der Parabel y = x²/4 − 1, Rand gehört dazu")


def sketch_disc(uid, cx, cy, win, label, center_label, extra=None):
    pl = Plane(uid, *win)
    pl.grid()
    region(pl, circle_path(cx, cy, 1, pl))
    pl.add(f'<path d="{circle_path(cx, cy, 1, pl)}" class="edge dash"/>')
    pl.axes()
    dot(pl, cx, cy, center_label, 8, -8)
    pl.add(f'<line x1="{pl.X(cx):.1f}" y1="{pl.Y(cy):.1f}" x2="{pl.X(cx+1):.1f}" y2="{pl.Y(cy):.1f}" class="radius"/>'
           f'<text x="{pl.X(cx+0.5):.1f}" y="{pl.Y(cy)+15:.1f}" class="pl" text-anchor="middle">r = 1</text>')
    return pl.svg(label)


def sketch_halfdisc():
    pl = Plane("d3", -2.5, 2.5, -3.5, 1)
    pl.grid()
    r = pl.s
    d = (f"M{pl.X(0):.1f},{pl.Y(-1):.1f} A{r:.1f},{r:.1f} 0 0,1 {pl.X(0):.1f},{pl.Y(-3):.1f} Z")
    region(pl, d)
    pl.add(f'<path d="{circle_path(0, -2, 1, pl)}" class="edge dash faint"/>')
    pl.add(f'<path d="{d}" class="edge dash"/>')
    pl.axes()
    dot(pl, 0, -2, "−2i", -8, 4, "end")
    pl.add(f'<text x="{pl.X(0.55):.1f}" y="{pl.Y(0.55):.1f}" class="note">Re(z) &gt; 0</text>')
    return pl.svg("Rechte Hälfte der offenen Kreisscheibe um −2i mit Radius 1, Ränder gehören nicht dazu")


def sketch_outside():
    pl = Plane("d5", -2.5, 2.5, -2, 2)
    pl.grid()
    outer = (f"M{pl.P(pl.xmin, pl.ymax)} L{pl.P(pl.xmax, pl.ymax)} L{pl.P(pl.xmax, pl.ymin)} "
             f"L{pl.P(pl.xmin, pl.ymin)} Z ")
    d = outer + circle_path(0, 0, 1, pl)
    pl.add(f'<path d="{d}" class="fill" fill-rule="evenodd"/><path d="{d}" fill="HATCH" fill-rule="evenodd"/>')
    pl.add(f'<path d="{circle_path(0, 0, 1, pl)}" class="edge"/>')
    pl.axes()
    pl.add(f'<text x="{pl.X(1.25):.1f}" y="{pl.Y(1.5):.1f}" class="note">|z| ≥ 1</text>')
    return pl.svg("Alles außerhalb des Einheitskreises, der Kreis selbst gehört dazu")


def sketch_roots():
    pl = Plane("f1", -1.75, 1.75, -1.75, 1.75, s=70, step=1)
    pl.grid()
    R = 4 ** 0.2
    pl.add(f'<path d="{circle_path(0, 0, R, pl)}" class="edge dash faint"/>')
    pts = []
    for k in range(5):
        a = math.pi / 10 + 2 * math.pi * k / 5
        pts.append((R * math.cos(a), R * math.sin(a), k))
    poly = " ".join(pl.P(x, y) for x, y, _ in pts)
    pl.add(f'<polygon points="{poly}" class="poly"/>')
    pl.axes()
    for x, y, k in pts:
        ux, uy = x / R, y / R
        pl.add(f'<line x1="{pl.X(0):.1f}" y1="{pl.Y(0):.1f}" x2="{pl.X(x):.1f}" y2="{pl.Y(y):.1f}" class="radius faint"/>')
        dot(pl, x, y, f"z{chr(0x2080 + k)}", ux * 14 - 6, -uy * 14 + 4)
    pl.add(f'<text x="{pl.X(0.35):.1f}" y="{pl.Y(0.12):.1f}" class="pl">π/10</text>')
    return pl.svg("Die fünf Lösungen von z⁵ = 4i bilden ein regelmäßiges Fünfeck auf dem Kreis mit Radius fünfte Wurzel aus 4")


def sketch_polar():
    pl = Plane("p1", -0.5, 3.5, -0.5, 2.5, s=50)
    pl.grid()
    x, y = 3, 2
    pl.add(f'<line x1="{pl.X(0):.1f}" y1="{pl.Y(0):.1f}" x2="{pl.X(x):.1f}" y2="{pl.Y(y):.1f}" class="vec"/>')
    pl.add(f'<line x1="{pl.X(x):.1f}" y1="{pl.Y(0):.1f}" x2="{pl.X(x):.1f}" y2="{pl.Y(y):.1f}" class="radius im"/>')
    pl.add(f'<line x1="{pl.X(0):.1f}" y1="{pl.Y(0):.1f}" x2="{pl.X(x):.1f}" y2="{pl.Y(0):.1f}" class="radius re"/>')
    a = math.atan2(y, x)
    rr = 0.8 * pl.s
    pl.add(f'<path d="M{pl.X(0.8):.1f},{pl.Y(0):.1f} A{rr:.1f},{rr:.1f} 0 0,0 {pl.X(0.8*math.cos(a)):.1f},{pl.Y(0.8*math.sin(a)):.1f}" class="arc"/>')
    pl.axes()
    dot(pl, x, y, "z = x + iy = r·e^(iφ)", -6, -10, "end")
    pl.add(f'<text x="{pl.X(1.0):.1f}" y="{pl.Y(0.22):.1f}" class="pl">φ</text>')
    pl.add(f'<text x="{pl.X(1.35):.1f}" y="{pl.Y(1.15):.1f}" class="pl">r</text>')
    pl.add(f'<text x="{pl.X(1.5):.1f}" y="{pl.Y(0)+30:.1f}" class="pl re" text-anchor="middle">x = r·cos φ</text>')
    pl.add(f'<text x="{pl.X(x)+6:.1f}" y="{pl.Y(1):.1f}" class="pl im">y = r·sin φ</text>')
    return pl.svg("Zeiger von 0 nach z mit Länge r und Winkel φ zur reellen Achse")


SKETCHES = {
    "{{SVG_POLAR}}": sketch_polar,
    "{{SVG_D1}}": sketch_parabola,
    "{{SVG_D2}}": lambda: sketch_disc("d2", -2, 1, (-4, 1.5, -1, 3),
                                      "Offene Kreisscheibe um −2 + i mit Radius 1", "−2 + i"),
    "{{SVG_D3}}": sketch_halfdisc,
    "{{SVG_D4}}": lambda: sketch_disc("d4", 0, 2, (-2.5, 2.5, -1, 3.5),
                                      "Offene Kreisscheibe um 2i mit Radius 1", "2i"),
    "{{SVG_D5}}": sketch_outside,
    "{{SVG_ROOTS}}": sketch_roots,
}

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    html = open(src, encoding="utf-8").read()
    for key, fn in SKETCHES.items():
        assert key in html, key
        html = html.replace(key, fn())
    open(dst, "w", encoding="utf-8").write(html)
    print("ok", dst, len(html))
