"""Skizzen für den Lernzettel „DGL Teil 1“ (Lösungsscharen).

Aufruf: python3 sketches_dgl.py <vorlage.html> <stil-quelle.html> <ausgabe.html>
"""
import math
import re
import sys


def family(uid, f, consts, special, xr, yr, label, xlabel="x", ylabel="y", asym=None, point=None):
    W, H, pl, pr, pt, pb = 520, 300, 38, 14, 14, 30
    x0, x1 = xr
    y0, y1 = yr

    def X(v):
        return pl + (v - x0) / (x1 - x0) * (W - pl - pr)

    def Y(v):
        return pt + (y1 - v) / (y1 - y0) * (H - pt - pb)

    p = [f'<defs><clipPath id="cl-{uid}"><rect x="{pl}" y="{pt}" width="{W-pl-pr}" height="{H-pt-pb}"/></clipPath></defs>']
    for v in range(math.ceil(x0), math.floor(x1) + 1):
        p.append(f'<line x1="{X(v):.1f}" y1="{pt}" x2="{X(v):.1f}" y2="{H-pb}" class="{"ax" if v == 0 else "g"}"/>')
        p.append(f'<text x="{X(v):.1f}" y="{H-pb+16}" class="t" text-anchor="middle">{str(v).replace("-", "−")}</text>')
    step = 1 if (y1 - y0) <= 10 else 2
    v = math.ceil(y0 / step) * step
    while v <= y1:
        p.append(f'<line x1="{pl}" y1="{Y(v):.1f}" x2="{W-pr}" y2="{Y(v):.1f}" class="{"ax" if v == 0 else "g"}"/>')
        p.append(f'<text x="{pl-6}" y="{Y(v)+4:.1f}" class="t" text-anchor="end">{str(v).replace("-", "−")}</text>')
        v += step
    p.append(f'<text x="{W-pr}" y="{H-4}" class="t" text-anchor="end">{xlabel}</text>')
    p.append(f'<text x="{pl+4}" y="{pt+11}" class="t">{ylabel}</text>')
    if asym is not None:
        pts = " ".join(f"{X(x0 + i*(x1-x0)/200):.1f},{Y(asym(x0 + i*(x1-x0)/200)):.1f}" for i in range(201))
        p.append(f'<polyline points="{pts}" class="asym" clip-path="url(#cl-{uid})"/>')

    def curve(c, cls):
        pts = []
        for i in range(401):
            xv = x0 + i * (x1 - x0) / 400
            try:
                yv = f(xv, c)
            except (ValueError, OverflowError, ZeroDivisionError):
                continue
            if yv != yv or abs(yv) > 1e3:
                continue
            pts.append(f"{X(xv):.1f},{Y(max(min(yv, y1 + 5), y0 - 5)):.1f}")
        return f'<polyline points="{" ".join(pts)}" class="{cls}" clip-path="url(#cl-{uid})"/>'

    for c in consts:
        p.append(curve(c, "fam"))
    p.append(curve(special, "spec"))
    if point:
        px, py, txt = point
        p.append(f'<circle cx="{X(px):.1f}" cy="{Y(py):.1f}" r="4.5" class="pt-spec"/>'
                 f'<text x="{X(px)+8:.1f}" y="{Y(py)-8:.1f}" class="pl">{txt}</text>')
    return (f'<svg class="timeplot" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">' + "".join(p) + "</svg>")


SKETCHES = {
    "{{SVG_FAM_SEP}}": lambda: family(
        "s1", lambda x, k: k * math.exp(x * x), [-3, -2, -1, -0.5, 0, 0.5, 1, 3], 2, (-1.6, 1.6), (-6, 8),
        "Lösungsschar y = K·e^(x²); hervorgehoben die spezielle Lösung mit y(0) = 2", point=(0, 2, "y(0) = 2")),
    "{{SVG_FAM_LIN}}": lambda: family(
        "l1", lambda x, c: c * math.exp(-2 * x) + 2 * x - 1, [-3, -2, -1, 0, 3, 5], 2, (-0.6, 3), (-3, 6),
        "Lösungsschar y = C·e^(−2x) + 2x − 1; alle Kurven nähern sich der Geraden 2x − 1",
        asym=lambda x: 2 * x - 1, point=(0, 1, "y(0) = 1")),
    "{{SVG_FAM_RC}}": lambda: family(
        "r1", lambda t, c: 10 * (1 - math.exp(-t)), [], 0, (0, 5), (0, 12),
        "Ladekurve u(t) = U0·(1 − e^(−t/τ)) mit U0 = 10 V und τ = 1", xlabel="t / τ", ylabel="u in V",
        asym=lambda t: 10, point=(1, 10 * (1 - math.exp(-1)), "nach 1τ: 63 %")),
}

if __name__ == "__main__":
    src, style_src, dst = sys.argv[1:4]
    html = open(src, encoding="utf-8").read()
    style = re.search(r"<style>.*?</style>", open(style_src, encoding="utf-8").read(), re.S).group(0)
    html = html.replace("{{STYLE}}", style)
    for key, fn in SKETCHES.items():
        if key not in html:
            continue
        html = html.replace(key, fn())
    assert "{{" not in html
    open(dst, "w", encoding="utf-8").write(html)
    print("ok", dst, len(html))
