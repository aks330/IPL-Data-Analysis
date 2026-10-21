


# ============================================================
# 1. LOAD DATA
# ============================================================

#df = pd.read_csv(r"C:\Users\USER\Downloads\sharing\ipl dataset\IPL_B2B_Dataset.csv")

# ============================================================
# IPL ADVANCED MATCH ANALYSIS
# # ============================================================
# IPL ADVANCED MATCH ANALYSIS
# PROFESSIONAL DATA ANALYTICS DASHBOARD
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(r"C:\Users\USER\Downloads\sharing\ipl dataset\IPL_B2B_Dataset.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# ============================================================
# 2. BASIC CLEANING FOR VISUALIZATION
# ============================================================

numeric_columns = [
    "runs_left",
    "balls_left",
    "wickets",
    "target_runs",
    "cur_run_rate",
    "req_run_rate",
    "result"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# Fill missing city values
if "city" in df.columns:
    df["city"] = df["city"].fillna("Unknown")

# Remove duplicates
df = df.drop_duplicates()

# Remove rows with missing important values
df = df.dropna(
    subset=numeric_columns
)

# Keep valid cricket values
df = df[
    (df["runs_left"] >= 0) &
    (df["balls_left"] >= 0) &
    (df["wickets"].between(0, 10)) &
    (df["target_runs"] > 0) &
    (df["cur_run_rate"] >= 0) &
    (df["req_run_rate"] >= 0)
]


# ============================================================
# 3. KPI CALCULATIONS
# ============================================================

total_records = len(df)

wins = int(
    (df["result"] == 1).sum()
)

losses = int(
    (df["result"] == 0).sum()
)

win_percentage = (
    wins / total_records * 100
)

loss_percentage = (
    losses / total_records * 100
)

avg_target = (
    df["target_runs"].mean()
)

avg_required_rr = (
    df["req_run_rate"].mean()
)

avg_current_rr = (
    df["cur_run_rate"].mean()
)


# ============================================================
# 4. TOP 5 TEAMS BY REQUIRED RUN RATE
# ============================================================

top_teams = (
    df.groupby(
        "batting_team"
    )["req_run_rate"]
    .mean()
    .sort_values(
        ascending=False
    )
    .head(5)
    .sort_values()
)


# ============================================================
# 5. BALLS REMAINING GROUPS
# ============================================================

balls_bins = [
    -1,
    20,
    40,
    60,
    80,
    100,
    120
]

balls_labels = [
    "0–20",
    "21–40",
    "41–60",
    "61–80",
    "81–100",
    "101–120"
]

df["balls_band"] = pd.cut(
    df["balls_left"],
    bins=balls_bins,
    labels=balls_labels
)

pressure = (
    df.groupby(
        "balls_band",
        observed=False
    )["req_run_rate"]
    .mean()
)


# ============================================================
# 6. CORRELATION
# ============================================================

correlation = df[
    [
        "runs_left",
        "balls_left",
        "wickets",
        "target_runs",
        "cur_run_rate",
        "req_run_rate",
        "result"
    ]
].corr()

rr_correlation = (
    correlation.loc[
        "req_run_rate",
        "result"
    ]
)

wicket_correlation = (
    correlation.loc[
        "wickets",
        "result"
    ]
)


# ============================================================
# 7. SCATTER PLOT SAMPLE
# ============================================================

sample_size = min(
    2500,
    len(df)
)

sample = df.sample(
    sample_size,
    random_state=42
)

win_points = sample[
    sample["result"] == 1
]

loss_points = sample[
    sample["result"] == 0
]


# ============================================================
# 8. PROFESSIONAL COLOR PALETTE
# ============================================================

BG = "#F5F7FB"

WHITE = "#FFFFFF"

DARK = "#172033"

GREY = "#667085"

LIGHT_GREY = "#E4E7EC"

BLUE = "#2563EB"

GREEN = "#16A34A"

PURPLE = "#7C3AED"

ORANGE = "#F59E0B"

RED = "#EF4444"

TEAL = "#0D9488"


# ============================================================
# 9. CREATE FIGURE
# ============================================================

fig = plt.figure(
    figsize=(20, 12),
    facecolor=BG
)


# ============================================================
# 10. HEADER
# ============================================================

fig.text(
    0.055,
    0.945,

    "IPL ADVANCED MATCH ANALYSIS",

    fontsize=25,

    fontweight="bold",

    color=DARK,

    ha="left"
)


fig.text(
    0.055,
    0.915,

    "Ball-level scoring pressure  •  Target analysis  •  Team performance  •  Match outcomes",

    fontsize=10.5,

    color=GREY,

    ha="left"
)


# Header line

fig.add_artist(
    plt.Line2D(
        [0.055, 0.945],
        [0.895, 0.895],

        transform=fig.transFigure,

        color=LIGHT_GREY,

        linewidth=1
    )
)


# ============================================================
# 11. KPI SECTION
# ============================================================

fig.text(
    0.055,
    0.865,

    "MATCH OVERVIEW",

    fontsize=9,

    fontweight="bold",

    color=GREY
)


# ============================================================
# 12. KPI CARD DATA
# ============================================================

kpis = [

    (
        "TOTAL RECORDS",
        f"{total_records:,}",
        BLUE,
        "DATA"
    ),

    (
        "WIN SHARE",
        f"{win_percentage:.1f}%",
        GREEN,
        "WIN"
    ),

    (
        "AVERAGE TARGET",
        f"{avg_target:.0f}",
        PURPLE,
        "RUNS"
    ),

    (
        "AVG REQUIRED RR",
        f"{avg_required_rr:.2f}",
        ORANGE,
        "RR"
    )
]


# ============================================================
# 13. KPI CARD POSITIONS
# ============================================================

card_positions = [

    (0.055, 0.785, 0.205, 0.065),

    (0.290, 0.785, 0.205, 0.065),

    (0.525, 0.785, 0.205, 0.065),

    (0.760, 0.785, 0.185, 0.065)
]


# ============================================================
# 14. CREATE KPI CARDS
# ============================================================

for (
    label,
    value,
    accent,
    icon
), (
    x,
    y,
    width,
    height
) in zip(
    kpis,
    card_positions
):

    card_ax = fig.add_axes(
        [
            x,
            y,
            width,
            height
        ]
    )

    card_ax.set_xlim(
        0,
        1
    )

    card_ax.set_ylim(
        0,
        1
    )

    card_ax.axis("off")


    # Card background

    card = FancyBboxPatch(

        (0, 0),

        1,

        1,

        boxstyle=(
            "round,pad=0.015,"
            "rounding_size=0.04"
        ),

        facecolor=WHITE,

        edgecolor=LIGHT_GREY,

        linewidth=1
    )

    card_ax.add_patch(card)


    # Accent line

    card_ax.plot(

        [0.035, 0.035],

        [0.18, 0.82],

        color=accent,

        linewidth=4,

        solid_capstyle="round"
    )


    # Small icon circle

    circle = Circle(

        (0.105, 0.50),

        0.18,

        facecolor=accent,

        alpha=0.10,

        edgecolor="none"
    )

    card_ax.add_patch(circle)


    card_ax.text(

        0.105,

        0.50,

        icon,

        ha="center",

        va="center",

        fontsize=5.5,

        fontweight="bold",

        color=accent
    )


    # Label

    card_ax.text(

        0.22,

        0.67,

        label,

        fontsize=7,

        fontweight="bold",

        color=GREY
    )


    # Value

    card_ax.text(

        0.22,

        0.20,

        value,

        fontsize=18,

        fontweight="bold",

        color=DARK
    )


# ============================================================
# 15. CHART STYLE FUNCTION
# ============================================================

def style_chart(
    ax,
    title
):

    ax.set_facecolor(
        WHITE
    )

    ax.set_title(

        title,

        loc="left",

        fontsize=12,

        fontweight="bold",

        color=DARK,

        pad=10
    )

    ax.grid(

        axis="y",

        color=LIGHT_GREY,

        linewidth=0.7
    )

    ax.set_axisbelow(
        True
    )

    ax.spines[
        "top"
    ].set_visible(
        False
    )

    ax.spines[
        "right"
    ].set_visible(
        False
    )

    ax.tick_params(

        labelsize=8,

        colors=GREY
    )


# ============================================================
# 16. TARGET SCORE DISTRIBUTION
# ============================================================

ax1 = fig.add_axes(
    [
        0.055,
        0.510,
        0.275,
        0.215
    ]
)

ax1.hist(

    df["target_runs"],

    bins=18,

    color=TEAL,

    edgecolor=WHITE,

    linewidth=0.8
)

ax1.axvline(

    avg_target,

    color=DARK,

    linestyle="--",

    linewidth=1.5
)

ax1.text(

    avg_target + 3,

    ax1.get_ylim()[1] * 0.86,

    f"Mean = {avg_target:.0f}",

    fontsize=8,

    fontweight="bold",

    color=DARK
)

style_chart(

    ax1,

    "Target Score Distribution"
)

ax1.set_xlabel(

    "Target Runs",

    fontsize=8,

    color=GREY
)

ax1.set_ylabel(

    "Records",

    fontsize=8,

    color=GREY
)


# ============================================================
# 17. MATCH OUTCOME DONUT
# ============================================================

ax2 = fig.add_axes(
    [
        0.355,
        0.510,
        0.275,
        0.215
    ]
)

wedges, _ = ax2.pie(

    [wins, losses],

    startangle=90,

    counterclock=False,

    colors=[
        GREEN,
        RED
    ],

    wedgeprops={

        "width": 0.30,

        "edgecolor": WHITE,

        "linewidth": 2
    }
)


# Center value

ax2.text(

    0,

    0.05,

    f"{win_percentage:.1f}%",

    ha="center",

    va="center",

    fontsize=18,

    fontweight="bold",

    color=DARK
)

ax2.text(

    0,

    -0.15,

    "Win Share",

    ha="center",

    va="center",

    fontsize=8,

    color=GREY
)

ax2.set_title(

    "Match Outcome",

    loc="left",

    fontsize=12,

    fontweight="bold",

    color=DARK,

    pad=10
)

ax2.legend(

    wedges,

    [

        f"Win  {wins:,}",

        f"Loss  {losses:,}"
    ],

    loc="lower center",

    bbox_to_anchor=(
        0.5,
        -0.04
    ),

    ncol=2,

    frameon=False,

    fontsize=7.5
)


# ============================================================
# 18. TOP TEAMS BY REQUIRED RR
# ============================================================

ax3 = fig.add_axes(
    [
        0.655,
        0.510,
        0.290,
        0.215
    ]
)

bars = ax3.barh(

    top_teams.index,

    top_teams.values,

    color=PURPLE,

    height=0.52
)

style_chart(

    ax3,

    "Teams with Highest Required RR"
)

ax3.set_xlabel(

    "Average Required RR",

    fontsize=8,

    color=GREY
)

ax3.grid(

    axis="x",

    color=LIGHT_GREY
)

ax3.grid(

    axis="y",

    visible=False
)


for bar, value in zip(

    bars,

    top_teams.values
):

    ax3.text(

        value + 0.06,

        bar.get_y()
        + bar.get_height() / 2,

        f"{value:.2f}",

        va="center",

        fontsize=7.5,

        fontweight="bold",

        color=DARK
    )


# ============================================================
# 19. SCORING PRESSURE
# ============================================================

ax4 = fig.add_axes(
    [
        0.055,
        0.255,
        0.275,
        0.195
    ]
)

x = np.arange(
    len(pressure)
)

y = pressure.values


ax4.plot(

    x,

    y,

    color=ORANGE,

    linewidth=2.5,

    marker="o",

    markersize=5
)


ax4.fill_between(

    x,

    y,

    color=ORANGE,

    alpha=0.10
)


ax4.set_xticks(
    x
)

ax4.set_xticklabels(

    pressure.index,

    fontsize=7
)

style_chart(

    ax4,

    "Scoring Pressure"
)

ax4.set_xlabel(

    "Balls Remaining",

    fontsize=8,

    color=GREY
)

ax4.set_ylabel(

    "Required RR",

    fontsize=8,

    color=GREY
)


# ============================================================
# 20. CURRENT RR VS REQUIRED RR
# ============================================================

ax5 = fig.add_axes(
    [
        0.355,
        0.255,
        0.275,
        0.195
    ]
)


ax5.scatter(

    loss_points["cur_run_rate"],

    loss_points["req_run_rate"],

    s=12,

    alpha=0.18,

    color=RED,

    label="Loss"
)


ax5.scatter(

    win_points["cur_run_rate"],

    win_points["req_run_rate"],

    s=12,

    alpha=0.18,

    color=GREEN,

    label="Win"
)


max_rr = max(

    df["cur_run_rate"].max(),

    df["req_run_rate"].max()
)


ax5.plot(

    [0, max_rr],

    [0, max_rr],

    color=DARK,

    linestyle="--",

    linewidth=1
)


style_chart(

    ax5,

    "Current RR vs Required RR"
)

ax5.set_xlabel(

    "Current RR",

    fontsize=8,

    color=GREY
)

ax5.set_ylabel(

    "Required RR",

    fontsize=8,

    color=GREY
)

ax5.legend(

    frameon=False,

    fontsize=7,

    loc="upper left"
)


# ============================================================
# 21. KEY INSIGHTS PANEL
# ============================================================

insight_ax = fig.add_axes(
    [
        0.655,
        0.255,
        0.290,
        0.195
    ]
)

insight_ax.set_xlim(
    0,
    1
)

insight_ax.set_ylim(
    0,
    1
)

insight_ax.axis(
    "off"
)


# Dark panel

panel = FancyBboxPatch(

    (0, 0),

    1,

    1,

    boxstyle=(
        "round,pad=0.02,"
        "rounding_size=0.035"
    ),

    facecolor=DARK,

    edgecolor=DARK
)

insight_ax.add_patch(
    panel
)


# Heading

insight_ax.text(

    0.07,

    0.84,

    "KEY INSIGHTS",

    fontsize=13,

    fontweight="bold",

    color=WHITE
)


insight_ax.text(

    0.07,

    0.75,

    "ANALYTICAL TAKEAWAYS",

    fontsize=7,

    fontweight="bold",

    color="#98A2B3"
)


insight_ax.plot(

    [0.07, 0.93],

    [0.69, 0.69],

    color="#475467",

    linewidth=1
)


# ============================================================
# 22. INSIGHT TEXT
# ============================================================

insights = [

    f"Average target score: {avg_target:.0f} runs",

    f"Win share: {win_percentage:.1f}%",

    f"Average required RR: {avg_required_rr:.2f}",

    f"RR vs outcome correlation: {rr_correlation:.2f}",

    f"Wickets vs outcome correlation: {wicket_correlation:.2f}",

    "Required RR rises as balls remaining decrease"
]


for i, text in enumerate(
    insights
):

    y_pos = (
        0.59 - i * 0.092
    )

    insight_ax.text(

        0.07,

        y_pos,

        "●",

        fontsize=5,

        color=ORANGE,

        va="center"
    )

    insight_ax.text(

        0.105,

        y_pos,

        text,

        fontsize=7.6,

        color="#E4E7EC",

        va="center"
    )


# ============================================================
# 23. FOOTER
# ============================================================

fig.text(

    0.945,

    0.075,

    "IPL BALL-LEVEL ANALYTICS",

    ha="right",

    fontsize=7,

    fontweight="bold",

    color=GREY
)


fig.text(

    0.945,

    0.055,

    "Python  •  Pandas  •  NumPy  •  Matplotlib",

    ha="right",

    fontsize=7,

    color=GREY
)


# ============================================================
# 24. SAVE HIGH-RESOLUTION IMAGE
# ============================================================

plt.savefig(

    "dashboard.png",

    dpi=300,

    bbox_inches="tight",

    facecolor=BG
)


# ============================================================
# 25. SHOW DASHBOARD
# ============================================================

plt.show()


# ============================================================
# END
# ============================================================
