"""Turn the avatar into a colored ASCII portrait that prints row by row.

Usage: python scripts/gen_ascii.py [path/to/image]
"""
import sys
from pathlib import Path

from PIL import Image, ImageEnhance

from common import escape, frame, write

W, H = 370, 370
COLS, ROWS = 86, 40
PAD = 14
RAMP = " :-=+*#%@@"
BG_RGB = (82, 88, 86)  # flat grey behind the avatar; knocked out to keep the figure readable
BG_TOL = 30
ROW_DELAY = 0.045  # seconds between rows


def quantize(c, step=24):
    return tuple(min(255, (v // step) * step + step // 2) for v in c)


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("avatar.jpg")
    img = Image.open(src).convert("RGB")
    small = img.resize((COLS, ROWS), Image.LANCZOS)
    img = ImageEnhance.Color(ImageEnhance.Contrast(small).enhance(1.4)).enhance(1.3)
    gray = img.convert("L")

    char_w = (W - 2 * PAD) / COLS
    line_h = (H - 2 * PAD) / ROWS
    font_size = char_w / 0.6

    rows = []
    for y in range(ROWS):
        # merge runs of the same (quantized) color into one tspan to keep the file small
        spans, run_color, run = [], None, ""
        for x in range(COLS):
            lum = gray.getpixel((x, y))
            raw = small.getpixel((x, y))
            if sum(abs(a - b) for a, b in zip(raw, BG_RGB)) < BG_TOL:
                ch = " "
            else:
                ch = RAMP[max(1, int(lum / 256 * len(RAMP)))]
            color = "#%02x%02x%02x" % quantize(img.getpixel((x, y)))
            if color != run_color and run:
                spans.append(f'<tspan fill="{run_color}">{escape(run)}</tspan>')
                run = ""
            run_color = color
            run += ch
        spans.append(f'<tspan fill="{run_color}">{escape(run)}</tspan>')
        ty = PAD + (y + 0.8) * line_h
        rows.append(
            f'<text class="r" style="animation-delay:{y * ROW_DELAY:.3f}s" x="{PAD}" y="{ty:.2f}" '
            f'textLength="{W - 2 * PAD}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{"".join(spans)}</text>'
        )

    style = f"""
.r {{ font-size: {font_size:.2f}px; font-weight: 700; clip-path: inset(0 100% 0 0); animation: print 0.35s steps(12, end) forwards; }}
@keyframes print {{ to {{ clip-path: inset(0 0 0 0); }} }}
@media (prefers-reduced-motion: reduce) {{ .r {{ animation: none; clip-path: none; }} }}
"""
    write("portrait-ascii.svg", frame(W, H, "\n".join(rows), style))


if __name__ == "__main__":
    main()
