"""
Draw LAB1 and LAB2 block diagrams (clean version, no SDRAM, with BUTTON and 7-Seg).
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ----- Colour palette -----
CYAN_BG   = (180, 240, 240)
WHITE     = (255, 255, 255)
BLACK     = (0,   0,   0)
GRAY_BOX  = (230, 230, 230)
BLUE_BOX  = (210, 225, 255)
GREEN_BOX = (210, 245, 215)

W, H = 1100, 820   # canvas size

def make_font(size):
    """Try to load a nice font, fall back to default."""
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for f in candidates:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def draw_box(draw, x1, y1, x2, y2, fill=GRAY_BOX, outline=BLACK, lw=2):
    draw.rectangle([x1, y1, x2, y2], fill=fill, outline=outline, width=lw)

def draw_text_centered(draw, text, x1, y1, x2, y2, font, color=BLACK):
    """Draw multi-line text centred inside a box."""
    lines = text.split("\n")
    line_h = font.size + 4
    total_h = len(lines) * line_h
    cy = (y1 + y2) / 2 - total_h / 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        cx = (x1 + x2) / 2 - tw / 2
        draw.text((cx, cy), line, font=font, fill=color)
        cy += line_h

def arrow_down(draw, x, y1, y2, lw=2):
    draw.line([(x, y1), (x, y2)], fill=BLACK, width=lw)
    aw = 6
    draw.polygon([(x-aw, y2-aw*1.5), (x+aw, y2-aw*1.5), (x, y2)], fill=BLACK)

def arrow_right(draw, x1, x2, y, lw=2):
    draw.line([(x1, y), (x2, y)], fill=BLACK, width=lw)
    aw = 6
    draw.polygon([(x2-aw*1.5, y-aw), (x2-aw*1.5, y+aw), (x2, y)], fill=BLACK)

def horiz_line(draw, x1, x2, y, lw=2):
    draw.line([(x1, y), (x2, y)], fill=BLACK, width=lw)

def vert_line(draw, x, y1, y2, lw=2):
    draw.line([(x, y1), (x, y2)], fill=BLACK, width=lw)

def dots(draw, x, y, font_s):
    draw.text((x, y), "· · ·", font=font_s, fill=BLACK)


def build_diagram(lab_num: int) -> Image.Image:
    """
    lab_num = 1 : includes BUTTON, but NOT 7-Seg (LAB1)
    lab_num = 2 : includes BUTTON AND 7-Seg (LAB2)
    """
    img  = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    font_l  = make_font(18)   # large
    font_m  = make_font(15)   # medium
    font_s  = make_font(13)   # small
    font_xs = make_font(11)   # extra small

    # ── Title ──────────────────────────────────────────────────────────────────
    title = f"Figure: Diagram for LAB{lab_num} (Nios II System on DE10-Standard)"
    bbox  = draw.textbbox((0, 0), title, font=font_l)
    draw.text(((W - (bbox[2]-bbox[0])) // 2, 10), title, font=font_l, fill=BLACK)

    # ── Host computer ──────────────────────────────────────────────────────────
    hc_x1, hc_y1, hc_x2, hc_y2 = 390, 50, 620, 110
    draw_box(draw, hc_x1, hc_y1, hc_x2, hc_y2, fill=WHITE)
    draw_text_centered(draw, "Host computer", hc_x1, hc_y1, hc_x2, hc_y2, font_m)

    # arrow down from Host to USB-Blaster
    arrow_down(draw, (hc_x1+hc_x2)//2, hc_y2, 165)

    # ── USB-Blaster ────────────────────────────────────────────────────────────
    ub_x1, ub_y1, ub_x2, ub_y2 = 420, 165, 580, 220
    draw_box(draw, ub_x1, ub_y1, ub_x2, ub_y2, fill=WHITE)
    draw_text_centered(draw, "USB-Blaster\ninterface", ub_x1, ub_y1, ub_x2, ub_y2, font_m)

    # ── FPGA chip boundary ─────────────────────────────────────────────────────
    fp_x1, fp_y1, fp_x2, fp_y2 = 40, 270, W-40, H-60
    draw_box(draw, fp_x1, fp_y1, fp_x2, fp_y2, fill=CYAN_BG, lw=3)
    draw.text((fp_x2 - 100, fp_y1 + 6), "FPGA chip", font=font_s, fill=BLACK)

    # Reset_n and Clock labels + arrows
    draw.text((55, 237), "Reset_n", font=font_s, fill=BLACK)
    draw.text((185, 237), "Clock", font=font_s, fill=BLACK)
    arrow_down(draw, 80,  258, fp_y1+2)
    arrow_down(draw, 200, 258, fp_y1+2)

    # USB-Blaster arrow into FPGA
    ub_cx = (ub_x1+ub_x2)//2
    arrow_down(draw, ub_cx, ub_y2, fp_y1+2)

    # ── Nios II + JTAG Debug (merged box) ─────────────────────────────────────
    n2_x1, n2_y1, n2_x2, n2_y2 = 55, fp_y1+20, 420, fp_y1+110
    draw_box(draw, n2_x1, n2_y1, n2_x2, n2_y2, fill=WHITE)
    # Nios II left half
    draw_text_centered(draw, "Nios II processor", n2_x1, n2_y1, (n2_x1+n2_x2)//2, n2_y2, font_m)
    # Dashed divider
    mid_x = (n2_x1+n2_x2)//2
    draw.line([(mid_x, n2_y1+8), (mid_x, n2_y2-8)], fill=BLACK, width=1)
    # JTAG Debug right half
    draw_text_centered(draw, "JTAG Debug\nmodule", mid_x, n2_y1, n2_x2, n2_y2, font_m)

    # ── JTAG UART interface ────────────────────────────────────────────────────
    ju_x1, ju_y1, ju_x2, ju_y2 = 600, fp_y1+20, 800, fp_y1+110
    draw_box(draw, ju_x1, ju_y1, ju_x2, ju_y2, fill=WHITE)
    draw_text_centered(draw, "JTAG UART\ninterface", ju_x1, ju_y1, ju_x2, ju_y2, font_m)

    # USB-Blaster -> JTAG UART (down then right)
    vert_line(draw, ub_cx, fp_y1, fp_y1+20+(ju_y2-ju_y1)//2)
    arrow_right(draw, ub_cx, ju_x1, fp_y1+20+(ju_y2-ju_y1)//2)

    # JTAG Debug -> JTAG UART
    arrow_right(draw, n2_x2, ju_x1, (n2_y1+n2_y2)//2)

    # ── Avalon switch fabric ───────────────────────────────────────────────────
    av_x1, av_y1, av_x2, av_y2 = 55, fp_y1+145, fp_x2-55, fp_y1+195
    draw_box(draw, av_x1, av_y1, av_x2, av_y2, fill=GRAY_BOX, lw=2)
    draw_text_centered(draw, "Avalon switch fabric", av_x1, av_y1, av_x2, av_y2, font_m)

    # Nios II -> Avalon
    arrow_down(draw, (n2_x1+n2_x2)//2, n2_y2, av_y1)

    # JTAG UART -> Avalon (down)
    ju_cx = (ju_x1+ju_x2)//2
    arrow_down(draw, ju_cx, ju_y2, av_y1)

    # ── Bottom peripheral blocks ───────────────────────────────────────────────
    # Layout depends on lab number:
    # LAB1: On-chip memory | BUTTON | Switches | LEDs
    # LAB2: On-chip memory | BUTTON | Switches | LEDs | 7-Seg

    if lab_num == 1:
        blocks = [
            ("On-chip\nmemory",                GRAY_BOX, None,       None),
            ("BUTTON\nparallel input\ninterface", GREEN_BOX, "KEY3\nKEY0",  "KEY"),
            ("Switches\nparallel input\ninterface", GRAY_BOX, "SW3\nSW0",   "SW"),
            ("LEDs\nparallel output\ninterface",  GRAY_BOX, "LEDG3\nLEDG0", "LED"),
        ]
    else:  # lab_num == 2
        blocks = [
            ("On-chip\nmemory",                GRAY_BOX, None,       None),
            ("BUTTON\nparallel input\ninterface", GREEN_BOX, "KEY3\nKEY0",  "KEY"),
            ("Switches\nparallel input\ninterface", GRAY_BOX, "SW3\nSW0",   "SW"),
            ("LEDs\nparallel output\ninterface",  GRAY_BOX, "LEDG3\nLEDG0", "LED"),
            ("7-Segment LED\nparallel output\ninterface", BLUE_BOX, "HEX0\nHEX5",   "HEX"),
        ]

    n_blocks   = len(blocks)
    total_w    = av_x2 - av_x1
    blk_gap    = 18
    blk_w      = (total_w - blk_gap*(n_blocks+1)) // n_blocks
    blk_h      = 115
    blk_y1     = av_y2 + 30
    blk_y2     = blk_y1 + blk_h

    blk_rects = []
    for i, (label, fill, pin_labels, pin_prefix) in enumerate(blocks):
        bx1 = av_x1 + blk_gap + i*(blk_w + blk_gap)
        bx2 = bx1 + blk_w
        draw_box(draw, bx1, blk_y1, bx2, blk_y2, fill=fill)
        draw_text_centered(draw, label, bx1, blk_y1, bx2, blk_y2, font_xs)
        blk_rects.append((bx1, bx2))

        # Arrow from Avalon down to block
        bcx = (bx1+bx2)//2
        arrow_down(draw, bcx, av_y2, blk_y1)

        # Pin labels below (skip On-chip memory)
        if pin_labels:
            pin_lines = pin_labels.split("\n")
            px_left  = bx1 + 4
            px_right = bx2 - 4
            # dots
            dots(draw, (bx1+bx2)//2 - 14, blk_y2 + 4, font_xs)
            # two pin arrows
            for j, pin in enumerate(pin_lines):
                px = bx1 + (j+1) * blk_w // (len(pin_lines)+1)
                arrow_down(draw, px, blk_y2, blk_y2+38)
                draw.text((px-10, blk_y2+40), pin, font=font_xs, fill=BLACK)

    # ── Legend / note ──────────────────────────────────────────────────────────
    note_y = H - 50
    note   = f"LAB{lab_num} Nios II system — DE10-Standard (Cyclone V)"
    bbox_n = draw.textbbox((0, 0), note, font=font_s)
    draw.text(((W-(bbox_n[2]-bbox_n[0]))//2, note_y), note, font=font_s, fill=(80,80,80))

    return img


if __name__ == "__main__":
    out_dir = r"e:\EE5215_LAB\images"
    os.makedirs(out_dir, exist_ok=True)

    for lab in (1, 2):
        img = build_diagram(lab)
        out = os.path.join(out_dir, f"fig_{lab+1}_1.png")
        img.save(out, dpi=(200, 200))
        print(f"Saved: {out}")
