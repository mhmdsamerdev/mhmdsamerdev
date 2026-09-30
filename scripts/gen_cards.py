"""Generate the `whoami` info card and the `ls ~/projects` listing.

Edit INFO / PROJECTS below, then run: python scripts/gen_cards.py
"""
from common import BLUE, FG, GREEN, MUTED, ORANGE, PURPLE, YELLOW, escape, frame, write

INFO = [
    ("name", "Mohammed Samer"),
    ("role", "software engineer"),
    ("stack", "Python · FastAPI · React · TypeScript"),
    ("", "C++ · Linux · Chrome extensions"),
    ("now", "rebuilding NetLanding"),
    ("wins", "UTMxHackathon '26 finalist (VertiFlow)"),
    ("site", "mhmdsamer.dev (soon)"),
    ("mail", "mhmdsamer.dev@gmail.com"),
]

# (name, status, description)
PROJECTS = [
    ("vertiflow", "finalist", "IoT vertical-farm platform · hackathon finalist"),
    ("netlanding", "active", "self-hosted income tracker: gross vs. what lands"),
    ("shelfie", "public", "local-first library manager for PDFs & EPUBs"),
    ("cleanrename", "public", "lightweight bulk renamer for Windows (C++)"),
    ("miftah", "wip", "switch languages in-browser, no OS language packs"),
    ("tsuzuki", "wip", "CLI that resumes mpv where you left off (Linux)"),
    ("mindroad", "wip", "local-first learning tracker in one SQLite file"),
    ("smartschedule", "paused", "attendance planner with a \"safe skip\" buffer"),
]

STATUS_COLOR = {"finalist": YELLOW, "active": GREEN, "public": BLUE, "wip": PURPLE, "paused": MUTED}
FADE_STYLE = """
.l { opacity: 0; animation: in 0.4s ease-out forwards; }
@keyframes in { from { opacity: 0; transform: translateX(-6px); } to { opacity: 1; transform: none; } }
@media (prefers-reduced-motion: reduce) { .l { animation: none; opacity: 1; } }
"""


def dots(y, w):
    return "".join(
        f'<circle cx="{16 + i * 16}" cy="{y}" r="5" fill="{c}"/>' for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"])
    ) + f'<line x1="0" y1="{y + 13}" x2="{w}" y2="{y + 13}" stroke="#21262d"/>'


def info_card():
    w, h = 490, 370
    lines = [dots(18, w)]
    lines.append(f'<text class="l" style="animation-delay:0.1s" x="20" y="62" font-size="14" fill="{GREEN}">mhmdsamer<tspan fill="{MUTED}">@</tspan>github</text>')
    lines.append(f'<text class="l" style="animation-delay:0.2s" x="20" y="80" font-size="13" fill="{MUTED}">{"─" * 22}</text>')
    for i, (key, val) in enumerate(INFO):
        y = 110 + i * 28
        delay = 0.4 + i * 0.25
        label = f"{key}:" if key else ""
        lines.append(
            f'<text class="l" style="animation-delay:{delay:.2f}s" x="20" y="{y}" font-size="14" xml:space="preserve">'
            f'<tspan fill="{ORANGE}">{escape(label):<7}</tspan><tspan x="84" fill="{FG}">{escape(val)}</tspan></text>'
        )
    y = 110 + len(INFO) * 28 + 4
    swatches = "".join(
        f'<rect x="{20 + i * 22}" y="{y - 12}" width="18" height="12" rx="2" fill="{c}"/>'
        for i, c in enumerate(["#f85149", ORANGE, YELLOW, GREEN, BLUE, PURPLE, FG])
    )
    lines.append(f'<g class="l" style="animation-delay:{0.4 + len(INFO) * 0.25:.2f}s">{swatches}</g>')
    write("info-card.svg", frame(w, h, "\n".join(lines), FADE_STYLE))


def projects():
    w = 860
    top, step = 62, 26
    h = top + len(PROJECTS) * step + 44
    lines = [dots(18, w)]
    lines.append(
        f'<text class="l" style="animation-delay:0.1s" x="20" y="{top - 16}" font-size="13" fill="{MUTED}">'
        f"total {len(PROJECTS)} · public repos are pinned, the rest are private</text>"
    )
    for i, (name, status, desc) in enumerate(PROJECTS):
        y = top + 12 + i * step
        color = STATUS_COLOR[status]
        lines.append(
            f'<text class="l" style="animation-delay:{0.3 + i * 0.15:.2f}s" x="20" y="{y}" font-size="14">'
            f'<tspan fill="{MUTED}">drwxr-xr-x</tspan>'
            f'<tspan x="130" fill="{color}">[{status}]</tspan>'
            f'<tspan x="240" fill="{BLUE}" font-weight="bold">{name}/</tspan>'
            f'<tspan x="390" fill="{FG}">{escape(desc)}</tspan></text>'
        )
    y = top + 12 + len(PROJECTS) * step + 8
    lines.append(
        f'<text class="l" style="animation-delay:{0.3 + len(PROJECTS) * 0.15:.2f}s" x="20" y="{y}" font-size="14">'
        f'<tspan fill="{GREEN}">mhmdsamer@github</tspan><tspan fill="{FG}"> ~ $ </tspan>'
        f'<tspan fill="{FG}" class="cur">█</tspan></text>'
    )
    style = FADE_STYLE + """
.cur { animation: blink 1s steps(1) infinite; }
@keyframes blink { 50% { opacity: 0; } }
"""
    write("projects.svg", frame(w, h, "\n".join(lines), style))


if __name__ == "__main__":
    info_card()
    projects()
