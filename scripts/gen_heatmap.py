"""Scrape the public contribution calendar and render it as an animated SVG.

Private contributions are only included if "Include private contributions on my
profile" is enabled in GitHub settings. Run daily by .github/workflows/heatmap.yml.
"""
import re
import sys
import urllib.request
from datetime import date

from common import FG, MUTED, frame, write

USER = sys.argv[1] if len(sys.argv) > 1 else "mhmdsamerdev"
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL, GAP = 11, 4


def fetch():
    req = urllib.request.Request(
        f"https://github.com/users/{USER}/contributions", headers={"User-Agent": "profile-heatmap"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode()
    days = {}
    for tag in re.findall(r"<td[^>]*ContributionCalendar-day[^>]*>", html):
        d = re.search(r'data-date="([\d-]+)"', tag)
        lvl = re.search(r'data-level="(\d)"', tag)
        if d and lvl:
            days[date.fromisoformat(d.group(1))] = int(lvl.group(1))
    total = re.search(r"([\d,]+)\s+contributions?\s+in the last year", html)
    if len(days) < 300:
        sys.exit(f"only parsed {len(days)} days; GitHub markup probably changed")
    return days, total.group(1) if total else None


def main():
    days, total = fetch()
    start = min(days)
    first_sunday = start.toordinal() - (start.weekday() + 1) % 7
    w, h = 860, 170
    left, top = 38, 40
    cells, months, seen = [], [], set()
    for d, lvl in sorted(days.items()):
        col = (d.toordinal() - first_sunday) // 7
        row = (d.weekday() + 1) % 7  # Sunday = 0
        x, y = left + col * (CELL + GAP), top + row * (CELL + GAP)
        delay = (col + row) * 0.012
        cells.append(
            f'<rect class="c" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{LEVELS[lvl]}"/>'
        )
        if d.day <= 7 and row == 0 and (d.year, d.month) not in seen and col < 52:
            seen.add((d.year, d.month))
            months.append(f'<text x="{x}" y="{top - 10}" font-size="11" fill="{MUTED}">{d.strftime("%b")}</text>')
    labels = "".join(
        f'<text x="{left - 8}" y="{top + r * (CELL + GAP) + 9}" font-size="10" fill="{MUTED}" text-anchor="end">{n}</text>'
        for r, n in [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    )
    legend_y = top + 7 * (CELL + GAP) + 16
    legend = "".join(
        f'<rect x="{w - 150 + i * 15}" y="{legend_y - 10}" width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>'
        for i, c in enumerate(LEVELS)
    )
    summary = f"{total} contributions in the last year" if total else "contributions in the last year"
    footer = (
        f'<text x="{left}" y="{legend_y}" font-size="12" fill="{FG}">{summary}</text>'
        f'<text x="{w - 184}" y="{legend_y}" font-size="11" fill="{MUTED}">less</text>{legend}'
        f'<text x="{w - 72}" y="{legend_y}" font-size="11" fill="{MUTED}">more</text>'
    )
    style = """
.c { opacity: 0; transform-box: fill-box; transform-origin: center; animation: pop 0.3s ease-out forwards; }
@keyframes pop { from { opacity: 0; transform: scale(0.3); } to { opacity: 1; transform: scale(1); } }
@media (prefers-reduced-motion: reduce) { .c { animation: none; opacity: 1; } }
"""
    write("contrib-heatmap.svg", frame(w, h, "".join(months) + labels + "\n".join(cells) + footer, style))
    print(f"{len(days)} days, total={total}")


if __name__ == "__main__":
    main()
