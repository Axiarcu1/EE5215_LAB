"""
Generate clean block diagram PNG images for LAB0-LAB3 using matplotlib.
Output: e:/EE5215_LAB/images/fig_1_1.png, fig_2_1.png, fig_3_1.png, fig_4_1.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
os.makedirs(OUT_DIR, exist_ok=True)

# ─── helpers ──────────────────────────────────────────────────────────────────

def add_box(ax, x, y, w, h, label, fc="#dbeafe", ec="#3b82f6", fontsize=9,
            style="round,pad=0.1", bold=False, color="black"):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle=style, facecolor=fc, edgecolor=ec, linewidth=1.2, zorder=3)
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(x, y, label, ha="center", va="center", fontsize=fontsize,
            color=color, fontweight=weight, zorder=4, multialignment="center")

def add_trap(ax, x, y, w, h, label, fc="#d1fae5", ec="#059669", fontsize=9):
    """Parallelogram approximated as FancyBbox with slant."""
    slope = 0.18
    xs = [x - w/2 + slope, x + w/2 + slope, x + w/2 - slope, x - w/2 - slope]
    ys = [y - h/2, y - h/2, y + h/2, y + h/2]
    poly = plt.Polygon(list(zip(xs, ys)), closed=True, facecolor=fc, edgecolor=ec, linewidth=1.2, zorder=3)
    ax.add_patch(poly)
    ax.text(x, y, label, ha="center", va="center", fontsize=fontsize, zorder=4, multialignment="center")

def add_border_box(ax, x, y, w, h, title, fc="#eff6ff", ec="#3b82f6"):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.15", facecolor=fc, edgecolor=ec,
                         linewidth=2, zorder=1)
    ax.add_patch(box)
    ax.text(x, y + h/2 + 0.12, title, ha="center", va="bottom",
            fontsize=9.5, fontweight="bold", color="#1d4ed8", zorder=5)

def arrow(ax, x1, y1, x2, y2, label="", color="#374151", lw=1.5, style="-|>", ls="-", label_side="top"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls, mutation_scale=14), zorder=5)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        offset = 0.12 if label_side == "top" else -0.18
        dx, dy = x2-x1, y2-y1
        if abs(dx) > abs(dy):   # horizontal
            ax.text(mx, my + offset, label, ha="center", va="bottom", fontsize=7, color="#6b7280", zorder=6)
        else:                   # vertical
            ax.text(mx + 0.12, my, label, ha="left", va="center", fontsize=7, color="#6b7280", zorder=6)

# ══════════════════════════════════════════════════════════════════════════════
# Figure 1.1 – LAB0
# ══════════════════════════════════════════════════════════════════════════════
def make_fig11():
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(0, 9); ax.set_ylim(0, 4)
    ax.axis("off")

    # PC
    add_box(ax, 1.3, 2, 1.8, 1.2, "PC\n(Quartus Prime)", fc="#f3f4f6", ec="#9ca3af")

    # FPGA border
    add_border_box(ax, 4.8, 2, 3.8, 2.8, "DE10-Standard (FPGA)")

    # inner FPGA blocks
    add_box(ax, 4.8, 2.9, 2.0, 0.55, "PLL / Clk",    fc="#bfdbfe", ec="#2563eb")
    add_box(ax, 4.8, 2.1, 2.0, 0.55, "User Logic",   fc="#bfdbfe", ec="#2563eb")
    add_box(ax, 4.8, 1.3, 2.0, 0.55, "I/O Buffer",   fc="#bfdbfe", ec="#2563eb")

    # LED/Switches  (aligned with I/O Buffer row y=1.3)
    add_box(ax, 7.9, 1.3, 1.6, 0.85, "LEDs &\nSwitches", fc="#fef9c3", ec="#d97706")

    # Arrows
    arrow(ax, 2.2, 2.0, 2.85, 2.0, "JTAG / USB")
    arrow(ax, 4.8, 2.62, 4.8, 2.37)
    arrow(ax, 4.8, 1.82, 4.8, 1.57)
    arrow(ax, 5.8, 1.3, 7.1, 1.3, "GPIO")   # straight right from I/O Buffer

    plt.tight_layout(pad=0.2)
    plt.savefig(os.path.join(OUT_DIR, "fig_1_1.png"), dpi=180, bbox_inches="tight")
    plt.close()
    print("✓ fig_1_1.png")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 2.1 – LAB1
# ══════════════════════════════════════════════════════════════════════════════
def make_fig21():
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.5)
    ax.axis("off")

    ax.text(5, 4.3, "FPGA – Combinational Logic Block",
            ha="center", va="top", fontsize=10, fontweight="bold", color="#1d4ed8")

    # Input
    add_trap(ax, 1.1, 2.25, 1.6, 0.85, "SW[9:0]\n(Input)", fc="#bbf7d0", ec="#16a34a")

    # FPGA border
    add_border_box(ax, 4.8, 2.25, 3.8, 3.2, "")

    # Internal blocks
    add_box(ax, 4.8, 3.2, 2.5, 0.65, "Decoder /\nEncoder", fc="#bfdbfe", ec="#2563eb")
    add_box(ax, 4.8, 2.25, 2.5, 0.65, "MUX",               fc="#bfdbfe", ec="#2563eb")
    add_box(ax, 4.8, 1.3,  2.5, 0.65, "ALU / Adder",       fc="#bfdbfe", ec="#2563eb")

    # Outputs
    add_trap(ax, 8.5, 3.2, 1.8, 0.85, "LEDR/G\n(Output)",  fc="#fed7aa", ec="#ea580c")
    add_trap(ax, 8.5, 1.3, 1.8, 0.85, "HEX\n7-Segment",    fc="#fed7aa", ec="#ea580c")

    # Arrows
    arrow(ax, 1.9, 2.25, 2.85, 2.25, "10 bits")             # SW → FPGA
    arrow(ax, 4.8, 2.87, 4.8, 2.57)                          # Dec → MUX
    arrow(ax, 4.8, 1.92, 4.8, 1.62)                          # MUX → ALU
    arrow(ax, 6.05, 3.2, 7.6, 3.2, "4b")                     # Dec → LED
    arrow(ax, 6.05, 1.3, 7.6, 1.3, "4b BCD")                 # ALU → HEX

    plt.tight_layout(pad=0.2)
    plt.savefig(os.path.join(OUT_DIR, "fig_2_1.png"), dpi=180, bbox_inches="tight")
    plt.close()
    print("✓ fig_2_1.png")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 3.1 – LAB2
# ══════════════════════════════════════════════════════════════════════════════
def make_fig31():
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 5)
    ax.axis("off")

    ax.text(5.8, 4.85, "FPGA – Sequential Logic Modules",
            ha="center", va="top", fontsize=10, fontweight="bold", color="#1d4ed8")

    # Clock source
    add_box(ax, 0.9, 3.2, 1.4, 0.85, "50 MHz\nClock", fc="#f3f4f6", ec="#9ca3af")

    # FPGA border  (x, y = center)
    add_border_box(ax, 5.5, 2.8, 5.8, 3.6, "")

    # RESET (left outside FPGA, below clock)
    add_trap(ax, 1.5, 1.6, 1.4, 0.75, "RESET\n(SW)", fc="#fee2e2", ec="#dc2626")

    # Internal blocks
    add_box(ax, 4.3, 3.6, 2.2, 0.7, "Clock Divider",          fc="#bfdbfe", ec="#2563eb")
    add_box(ax, 7.0, 3.6, 2.2, 0.7, "FSM\nController",        fc="#e9d5ff", ec="#7c3aed")
    add_box(ax, 4.3, 2.3, 2.2, 0.7, "Shift Register\n/ Counter", fc="#bfdbfe", ec="#2563eb")
    add_box(ax, 7.0, 2.3, 2.2, 0.7, "Output Logic",            fc="#bfdbfe", ec="#2563eb")

    # LEDs output
    add_trap(ax, 10.0, 2.3, 1.5, 0.8, "LEDs\nOutput", fc="#fed7aa", ec="#ea580c")

    # Arrows
    arrow(ax, 1.6, 3.2, 2.6, 3.6, "50MHz")       # Clock → ClkDiv (angled up)
    arrow(ax, 2.2, 1.6, 3.2, 2.3)                 # RESET → ShiftReg (angled)
    arrow(ax, 5.4, 3.6, 5.9, 3.6)                 # ClkDiv → FSM
    arrow(ax, 4.3, 3.25, 4.3, 2.65)               # ClkDiv → ShiftReg
    arrow(ax, 7.0, 3.25, 7.0, 2.65)               # FSM → OutputLogic
    arrow(ax, 5.4, 2.3, 5.9, 2.3)                 # ShiftReg → OutputLogic
    arrow(ax, 8.1, 2.3, 9.25, 2.3, "GPIO")        # OutputLogic → LEDs

    plt.tight_layout(pad=0.2)
    plt.savefig(os.path.join(OUT_DIR, "fig_3_1.png"), dpi=180, bbox_inches="tight")
    plt.close()
    print("✓ fig_3_1.png")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 4.1 – LAB3
# ══════════════════════════════════════════════════════════════════════════════
def make_fig41():
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(6.5, 5.85, "I2C Master Core (FPGA)",
            ha="center", va="top", fontsize=10, fontweight="bold", color="#1d4ed8")

    # Processor Interface
    add_box(ax, 1.0, 3.0, 1.7, 1.5, "Processor\nInterface\n(Reg R/W)", fc="#f3f4f6", ec="#9ca3af")

    # FPGA core border
    add_border_box(ax, 6.0, 3.0, 6.5, 4.5, "")

    # Left column (teal)
    add_box(ax, 4.7, 4.2, 2.2, 0.75, "Clock Gen\nSynchronizer",  fc="#ccfbf1", ec="#0d9488")
    add_box(ax, 4.7, 3.0, 2.2, 0.75, "Tx / Rx\nData FSM",        fc="#ccfbf1", ec="#0d9488")
    add_box(ax, 4.7, 1.8, 2.2, 0.75, "ACK / NACK\nLogic",        fc="#ccfbf1", ec="#0d9488")

    # Right column (purple)
    add_box(ax, 7.4, 4.2, 2.2, 0.75, "I2C Master\nControl FSM",  fc="#e9d5ff", ec="#7c3aed")
    add_box(ax, 7.4, 3.0, 2.2, 0.75, "I2C Bus\nControl FSM",     fc="#e9d5ff", ec="#7c3aed")

    # I2C bus
    add_box(ax, 10.2, 3.0, 1.8, 1.2, "I2C Bus\nSCL / SDA",      fc="#fed7aa", ec="#ea580c")

    # I2C Slave
    add_box(ax, 12.2, 3.0, 1.4, 1.0, "I2C Slave\nDevice",        fc="#fef9c3", ec="#d97706", bold=True)

    # Arrows – processor → core
    arrow(ax, 1.85, 3.0, 3.6, 3.0, "Config/Data")

    # Internal
    arrow(ax, 5.8, 4.2, 6.3, 4.2)                      # ClkGen → MasterFSM
    arrow(ax, 7.4, 3.82, 7.4, 3.37)                     # MasterFSM → BusFSM
    arrow(ax, 4.7, 3.82, 4.7, 3.37)                     # ClkGen → TxRx
    arrow(ax, 4.7, 2.62, 4.7, 2.17)                     # TxRx → ACK

    # Dashed feedback arrows
    arrow(ax, 7.4, 4.0, 5.8, 3.35, style="-|>", ls="--", color="#7c3aed")   # MasterFSM → TxRx
    arrow(ax, 5.8, 1.8, 7.3, 3.0,  style="-|>", ls="--", color="#0d9488")   # ACK → BusFSM

    # SCL/SDA → I2C bus
    arrow(ax, 8.5, 3.25, 9.3, 3.25, "SCL", color="#dc2626")
    arrow(ax, 8.5, 2.85,  9.3, 2.85, "SDA", color="#dc2626")

    # I2C bus → slave
    arrow(ax, 11.1, 3.0, 11.5, 3.0, "Open-drain")

    plt.tight_layout(pad=0.2)
    plt.savefig(os.path.join(OUT_DIR, "fig_4_1.png"), dpi=180, bbox_inches="tight")
    plt.close()
    print("✓ fig_4_1.png")


if __name__ == "__main__":
    make_fig11()
    make_fig21()
    make_fig31()
    make_fig41()
    print("\nAll diagrams saved to:", OUT_DIR)
