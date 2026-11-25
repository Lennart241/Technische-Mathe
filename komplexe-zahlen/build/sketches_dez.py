"""Skizzen für den Lernzettel zur Klausur am 14.12.2026 (neuer Prüfer, Notation mit j).

Aufruf: python3 sketches_dez.py <vorlage.html> <stil-quelle.html> <ausgabe.html>
Die CSS-Regeln werden aus der ersten Vorlage übernommen ({{STYLE}}).
"""
import math
import re
import sys

from sketches import Plane as _Plane, dot, fmt


class Plane(_Plane):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.imfmt = lambda v: ("−j" if v < 0 else "j") + (str(abs(int(v))) if abs(v) != 1 else "")


def arrow(pl, x0, y0, x1, y1, cls="vec"):
    """Pfeil von (x0,y0) nach (x1,y1) in Ebenenkoordinaten."""
    X0, Y0, X1, Y1 = pl.X(x0), pl.Y(y0), pl.X(x1), pl.Y(y1)
    a = math.atan2(Y1 - Y0, X1 - X0)
    h = 9
    p1 = (X1 - h * math.cos(a - 0.4), Y1 - h * math.sin(a - 0.4))
    p2 = (X1 - h * math.cos(a + 0.4), Y1 - h * math.sin(a + 0.4))
    return (f'<line x1="{X0:.1f}" y1="{Y0:.1f}" x2="{X1 - 6*math.cos(a):.1f}" y2="{Y1 - 6*math.sin(a):.1f}" class="{cls}"/>'
            f'<path d="M{X1:.1f},{Y1:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" class="{cls}-h"/>')


def arc(pl, r, a0, a1, cls="arc"):
    rr = r * pl.s
    large = 1 if (a1 - a0) > math.pi else 0
    return (f'<path d="M{pl.X(r*math.cos(a0)):.1f},{pl.Y(r*math.sin(a0)):.1f} '
            f'A{rr:.1f},{rr:.1f} 0 {large},0 {pl.X(r*math.cos(a1)):.1f},{pl.Y(r*math.sin(a1)):.1f}" class="{cls}"/>')


def sketch_gauss():
    pl = Plane("g1", -3, 3.5, -1, 3.8, s=48)
    pl.grid()
    for (x, y) in [(2, 3), (-2, 1)]:
        pl.add(f'<line x1="{pl.X(x):.1f}" y1="{pl.Y(0):.1f}" x2="{pl.X(x):.1f}" y2="{pl.Y(y):.1f}" class="radius im"/>')
        pl.add(f'<line x1="{pl.X(0):.1f}" y1="{pl.Y(y):.1f}" x2="{pl.X(x):.1f}" y2="{pl.Y(y):.1f}" class="radius faint"/>')
        pl.add(f'<line x1="{pl.X(0):.1f}" y1="{pl.Y(0)+3:.1f}" x2="{pl.X(x):.1f}" y2="{pl.Y(0)+3:.1f}" class="reline"/>')
    pl.add(arc(pl, 0.7, 0, math.atan2(3, 2)))
    pl.add(arc(pl, 0.5, 0, math.atan2(1, -2), "arc faint"))
    pl.add(arrow(pl, 0, 0, 2, 3))
    pl.add(arrow(pl, 0, 0, -2, 1))
    pl.axes()
    dot(pl, 2, 3, "z₁ = 2 + j3", 8, -6)
    dot(pl, -2, 1, "z₂ = −2 + j", -8, -10, "end")
    pl.add(f'<text x="{pl.X(0.55):.1f}" y="{pl.Y(1.75):.1f}" class="pl" text-anchor="end">|z₁| = √13</text>')
    pl.add(f'<text x="{pl.X(-1.1):.1f}" y="{pl.Y(0.75):.1f}" class="pl" text-anchor="middle">|z₂| = √5</text>')
    pl.add(f'<text x="{pl.X(1):.1f}" y="{pl.Y(0)+31:.1f}" class="pl re" text-anchor="middle">Re = 2</text>')
    pl.add(f'<text x="{pl.X(-1):.1f}" y="{pl.Y(0)+31:.1f}" class="pl re" text-anchor="middle">Re = −2</text>')
    pl.add(f'<text x="{pl.X(2)+6:.1f}" y="{pl.Y(1.5):.1f}" class="pl im">Im = 3</text>')
    pl.add(f'<text x="{pl.X(-2)-6:.1f}" y="{pl.Y(0.45):.1f}" class="pl im" text-anchor="end">Im = 1</text>')
    pl.add(f'<text x="{pl.X(0.78):.1f}" y="{pl.Y(0.2):.1f}" class="pl">φ₁</text>')
    return pl.svg("z1 = 2 + j3 und z2 = −2 + j in der Gaußschen Zahlenebene mit Realteil, Imaginärteil und Betrag")


def sketch_zeiger():
    pl = Plane("z1", -0.6, 4.2, -0.6, 4.6, s=50)
    pl.grid()
    pl.add(f'<line x1="{pl.X(3):.1f}" y1="{pl.Y(0):.1f}" x2="{pl.X(3):.1f}" y2="{pl.Y(4):.1f}" class="radius faint"/>')
    pl.add(f'<line x1="{pl.X(0):.1f}" y1="{pl.Y(4):.1f}" x2="{pl.X(3):.1f}" y2="{pl.Y(4):.1f}" class="radius faint"/>')
    pl.add(arc(pl, 1.1, 0, math.atan2(4, 3)))
    pl.add(arrow(pl, 0, 0, 3, 0, "vec re"))
    pl.add(arrow(pl, 0, 0, 0, 4, "vec im"))
    pl.add(arrow(pl, 0, 0, 3, 4, "vec"))
    pl.axes()
    pl.add(f'<text x="{pl.X(2.2):.1f}" y="{pl.Y(0)-8:.1f}" class="pl re">X₁ = 3</text>')
    pl.add(f'<text x="{pl.X(0)+8:.1f}" y="{pl.Y(3.55):.1f}" class="pl im">X₂ = j4</text>')
    pl.add(f'<text x="{pl.X(3)+6:.1f}" y="{pl.Y(4)-6:.1f}" class="pl" style="font-weight:600">X = 3 + j4</text>')
    pl.add(f'<text x="{pl.X(1.05):.1f}" y="{pl.Y(0.45):.1f}" class="pl">φ ≈ 53,13°</text>')
    pl.add(f'<text x="{pl.X(1.25):.1f}" y="{pl.Y(2.05):.1f}" class="pl" text-anchor="end">|X| = 5</text>')
    return pl.svg("Zeigerdiagramm: X1 = 3 und X2 = j4 ergeben den Summenzeiger X = 3 + j4 mit Länge 5")


def sketch_time():
    """x1, x2 und Summe über ωt von 0 bis 4π."""
    W, H, padl, padr, padt, padb = 560, 230, 40, 14, 14, 34
    tmax = 4 * math.pi
    ymax = 5.6

    def X(t):
        return padl + t / tmax * (W - padl - padr)

    def Y(v):
        return padt + (ymax - v) / (2 * ymax) * (H - padt - padb)

    parts = []
    for v in [-5, -4, -3, 0, 3, 4, 5]:
        parts.append(f'<line x1="{padl}" y1="{Y(v):.1f}" x2="{W-padr}" y2="{Y(v):.1f}" class="{"ax" if v == 0 else "g"}"/>')
        if v:
            parts.append(f'<text x="{padl-6}" y="{Y(v)+4:.1f}" class="t" text-anchor="end">{"−" if v < 0 else ""}{abs(v)}</text>')
    for k, lab in enumerate(["0", "π", "2π", "3π", "4π"]):
        t = k * math.pi
        parts.append(f'<line x1="{X(t):.1f}" y1="{padt}" x2="{X(t):.1f}" y2="{H-padb}" class="g"/>')
        parts.append(f'<text x="{X(t):.1f}" y="{H-padb+16}" class="t" text-anchor="middle">{lab}</text>')
    parts.append(f'<text x="{W-padr}" y="{H-4}" class="t" text-anchor="end">ωt</text>')
    phi = math.atan2(4, 3)
    curves = [
        ("c-re", lambda t: 3 * math.cos(t)),
        ("c-im", lambda t: 4 * math.cos(t + math.pi / 2)),
        ("c-sum", lambda t: 5 * math.cos(t + phi)),
    ]
    for cls, f in curves:
        pts = " ".join(f"{X(i*tmax/240):.1f},{Y(f(i*tmax/240)):.1f}" for i in range(241))
        parts.append(f'<polyline points="{pts}" class="{cls}"/>')
    tpk = 2 * math.pi - phi
    parts.append(f'<circle cx="{X(tpk):.1f}" cy="{Y(5):.1f}" r="3.5" class="pt"/>')
    parts.append(f'<text x="{X(tpk)+6:.1f}" y="{Y(5)-6:.1f}" class="pl">Maximum 5, um φ früher als bei 2π</text>')
    return (f'<svg class="timeplot" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Zeitverlauf von x1 = 3cos(ωt), x2 = 4cos(ωt + π/2) und der Summe 5cos(ωt + φ)">'
            + "".join(parts) + "</svg>")


def sketch_lambda():
    pl = Plane("l1", -3.5, 1.5, -3.8, 3.8, s=34)
    pl.grid()
    pl.add(f'<line x1="{pl.X(-2):.1f}" y1="{pl.Y(-3):.1f}" x2="{pl.X(-2):.1f}" y2="{pl.Y(3):.1f}" class="radius faint"/>')
    pl.axes()
    dot(pl, -2, 3, "λ₁ = −2 + j3", 8, -2)
    dot(pl, -2, -3, "λ₂ = −2 − j3", 8, 12)
    pl.add(f'<text x="{pl.X(-2):.1f}" y="{pl.Y(0)+16:.1f}" class="pl" text-anchor="middle">−2 = Dämpfung</text>')
    return pl.svg("Die Nullstellen λ = −2 ± j3 liegen spiegelbildlich zur reellen Achse")


SKETCHES = {
    "{{SVG_GAUSS}}": sketch_gauss,
    "{{SVG_ZEIGER}}": sketch_zeiger,
    "{{SVG_TIME}}": sketch_time,
    "{{SVG_LAMBDA}}": sketch_lambda,
}

if __name__ == "__main__":
    src, style_src, dst = sys.argv[1:4]
    html = open(src, encoding="utf-8").read()
    style = re.search(r"<style>.*?</style>", open(style_src, encoding="utf-8").read(), re.S).group(0)
    html = html.replace("{{STYLE}}", style)
    for key, fn in SKETCHES.items():
        assert key in html, key
        html = html.replace(key, fn())
    assert "{{" not in html
    open(dst, "w", encoding="utf-8").write(html)
    print("ok", dst, len(html))
