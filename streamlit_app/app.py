"""
IPL Data Analytics Dashboard
A polished, audience-friendly Streamlit experience for exploring IPL statistics.

Run with: streamlit run app.py
"""
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="IPL Analytics Dashboard", page_icon="🏏", layout="wide")

# ── Premium styling ───────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.18), transparent 28%),
            linear-gradient(135deg, #07111f 0%, #0f1b33 50%, #111827 100%);
        color: #f8fafc;
    }
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2rem;
        max-width: 100% !important;
        width: 100% !important;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #08111e 0%, #0b1324 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.15);
    }
    div[data-testid="stSidebar"] .stSelectbox,
    div[data-testid="stSidebar"] .stMultiSelect,
    div[data-testid="stSidebar"] .stRadio {
        background: rgba(15, 23, 42, 0.85);
        border-radius: 12px;
        padding: 0.4rem 0.6rem;
    }
    .css-1d391kg, .css-1lp1aud {
        color: #f8fafc;
    }
    .stMetric {
        background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.20);
        padding: 0.85rem 0.9rem;
        border-radius: 14px;
    }
    .stMetric [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #facc15 !important;
    }
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }
    .stPlotlyChart,
    .stVegaLiteChart,
    .stAltairChart,
    .stMarkdown,
    .stDataFrame {
        max-width: 100%;
        width: 100%;
    }
    .element-container {
        margin-bottom: 0.3rem;
    }
    .stTabs [role="tablist"] {
        gap: 0.5rem;
    }
    .stTabs [role="tab"] {
        border-radius: 10px 10px 0 0;
        background: rgba(255,255,255,0.05);
    }
    .hero-banner {
        background: linear-gradient(135deg, rgba(59,130,246,0.22), rgba(249,115,22,0.16));
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.22);
    }
    .hero-banner h1 {
        margin-bottom: 0.15rem;
        color: #fff;
        font-size: 1.85rem;
        line-height: 1.18;
    }
    .hero-banner p {
        margin-top: 0.25rem;
        color: #cbd5e1;
        font-size: 0.92rem;
    }
    .section-card {
        background: rgba(15, 23, 42, 0.42);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 14px;
        padding: 0.75rem 0.85rem;
        margin-top: 0.45rem;
    }
    .eyebrow {
        display: inline-block;
        background: rgba(251,191,36,0.16);
        color: #fde68a;
        border: 1px solid rgba(251,191,36,0.34);
        border-radius: 999px;
        padding: 0.22rem 0.6rem;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.82rem;
        letter-spacing: 0.02em;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.25rem;
    }
    [data-testid="stSidebar"] .st-bd {
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
    }
    @media (max-width: 900px) {
        .hero-banner h1 {
            font-size: 1.7rem;
        }
        .hero-banner p {
            font-size: 0.92rem;
        }
        .stMetric {
            margin-bottom: 0.6rem;
        }
    }
    @media (max-width: 680px) {
        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }
        .hero-banner {
            padding: 1rem;
        }
        .hero-banner h1 {
            font-size: 1.4rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Load cleaned data ───────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_ROOT = BASE_DIR / "data"
DATA_DIR_CANDIDATES = [
    DATA_ROOT / "clean_data",
    DATA_ROOT / "clean data",
]
DATA_DIR = next((path for path in DATA_DIR_CANDIDATES if path.exists()), DATA_ROOT)


@st.cache_data
def load_data():
    matches_path = DATA_DIR / "matches_clean.csv"
    deliveries_path = DATA_DIR / "deliveries_clean.csv"

    if not matches_path.exists() or not deliveries_path.exists():
        raise FileNotFoundError(
            f"Expected cleaned data files not found in '{DATA_DIR}'. "
            "Look for 'matches_clean.csv' and 'deliveries_clean.csv' under the project data folder."
        )

    matches = pd.read_csv(matches_path, parse_dates=["date"])
    deliveries = pd.read_csv(deliveries_path)

    # The cleaned CSV sometimes has season values that are offset or incomplete.
    # To keep the UI intuitive and consistent with match dates, normalize to the
    # actual year of the match when the season field is missing or inconsistent.
    if "season" in matches.columns:
        matches["season"] = pd.to_numeric(matches["season"], errors="coerce")
        if matches["season"].isna().any() or set(matches["season"].dropna().unique()) != set(matches["date"].dt.year.unique()):
            matches["season"] = matches["date"].dt.year

    return matches, deliveries


matches, deliveries = load_data()

# ── Sidebar navigation ──────────────────────────────────────
st.sidebar.title("🏏 IPL Analytics")
st.sidebar.caption("From the 2008 season to the latest 2024 edition")
page = st.sidebar.radio(
    "Explore",
    ["📊 Overview", "🏏 Player Stats", "🏟️ Venue Analysis", "📈 Trends"],
)

st.sidebar.markdown("### Filter the story")
st.sidebar.caption("Choose a clean audience lens for instant insight.")


def season_label(season):
    return str(int(season))


all_seasons = sorted(matches["season"].dropna().unique())
all_teams = sorted(set(matches["team1"].dropna().tolist() + matches["team2"].dropna().tolist()))
all_venues = sorted(matches["venue"].dropna().unique())

selected_seasons = st.sidebar.multiselect(
    "Seasons",
    all_seasons,
    default=all_seasons,
    format_func=season_label,
)
selected_teams = st.sidebar.multiselect("Teams", all_teams, default=all_teams)
selected_venues = st.sidebar.multiselect("Venues", all_venues, default=all_venues)

filtered_matches = matches[
    matches["season"].isin(selected_seasons)
    & matches["venue"].isin(selected_venues)
    & (matches["team1"].isin(selected_teams) | matches["team2"].isin(selected_teams))
].copy()

filtered_deliveries = deliveries[deliveries["match_id"].isin(filtered_matches["id"])].copy()
valid_matches = filtered_matches[
    filtered_matches["winner"].notna() & (filtered_matches["winner"] != "No Result")
].copy()

st.sidebar.markdown("### Quick story")
st.sidebar.info(
    f"Showing {len(valid_matches):,} completed matches across {len(selected_seasons)} seasons and {len(selected_teams)} teams."
)

if not valid_matches.empty:
    st.sidebar.success("Live filters are active and all cards update instantly.")

# ── Shared styling ──────────────────────────────────────────
sns.set_style("darkgrid")
plt.rcParams["figure.facecolor"] = "#0E1117"
plt.rcParams["axes.facecolor"] = "#0E1117"
plt.rcParams["axes.edgecolor"] = "#94A3B8"
plt.rcParams["text.color"] = "#F8FAFC"
plt.rcParams["axes.labelcolor"] = "#F8FAFC"
plt.rcParams["xtick.color"] = "#CBD5E1"
plt.rcParams["ytick.color"] = "#CBD5E1"
plt.rcParams["axes.titlecolor"] = "#F8FAFC"

# ============================================================
# PAGE 1: OVERVIEW
# ============================================================
if page == "📊 Overview":
    st.markdown(
        """
        <div class="hero-banner">
            <div class="eyebrow">IPL dashboard</div>
            <h1>IPL Dashboard</h1>
            <p>Explore the tournament in a simple and clear way with filters for teams, seasons, and venues.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        f"Season range: {season_label(min(selected_seasons))}–{season_label(max(selected_seasons))} • Filtered by your selected teams, venues, and seasons."
    )

    if valid_matches.empty:
        st.warning("No completed matches match the current filters. Please widen your selection.")
        st.stop()

    team_summary = valid_matches.groupby("winner").size().reset_index(name="wins")
    top_team = team_summary.sort_values("wins", ascending=False).iloc[0]
    most_frequent_venue = valid_matches["venue"].value_counts().idxmax()
    seasons = sorted(valid_matches["season"].unique())
    season_labels = [season_label(season) for season in seasons]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Games shown", f"{len(valid_matches):,}", help="Number of completed match results currently visible after filtering.")
    col2.metric("Balls tracked", f"{len(filtered_deliveries):,}", help="Number of delivery records included in the selected match window.")
    col3.metric("Teams in view", int(valid_matches["winner"].nunique()), help="Number of different teams that appear in the selected results.")
    col4.metric("Years in view", int(valid_matches["season"].nunique()), help="How many IPL seasons are represented in the current filter.")

    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    c1.metric("Top team", top_team["winner"])
    c2.metric("Top wins", int(top_team["wins"]))
    c3.metric("Most used venue", most_frequent_venue)

    st.markdown("---")

    st.markdown(
        """
        <div class="section-card">
            <strong>Filtered Summary Table</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    summary_table = team_summary.sort_values("wins", ascending=False).head(12).reset_index(drop=True)
    summary_table.insert(0, "Rank", range(1, len(summary_table) + 1))
    summary_table = summary_table.rename(columns={"winner": "Team", "wins": "Wins in selected matches"})
    summary_table = summary_table[["Rank", "Team", "Wins in selected matches"]]
    summary_table_styled = summary_table.style.set_properties(**{"text-align": "center"})
    st.caption("Each number in the table shows how many completed matches that team won inside the filters you selected.")
    st.dataframe(
        summary_table_styled,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Team": st.column_config.TextColumn("Team", width="large"),
            "Wins in selected matches": st.column_config.NumberColumn("Wins in selected matches", width="medium"),
        },
    )

    left, right = st.columns([1.2, 0.8])
    with left:
        st.subheader("🏆 Team wins")
        wins = team_summary.sort_values("wins", ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8.0, 4.6))
        sns.barplot(x="wins", y="winner", data=wins, palette="rocket", ax=ax)
        ax.set_title("Current winning race", fontsize=13)
        ax.set_xlabel("Wins")
        ax.set_ylabel("Team")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with right:
        st.subheader("📌 Simple insight")
        st.markdown(
            "A few franchises continue to define the competitive narrative across the league's most successful years."
        )
        st.info(
            f"Among the teams in your selected window, {top_team['winner']} leads with {int(top_team['wins'])} victories."
        )

    st.subheader("📈 Games by year")
    season_counts = valid_matches.groupby("season").size().reset_index(name="count")
    season_counts["season_label"] = season_counts["season"].map(season_label)
    fig, ax = plt.subplots(figsize=(8.4, 4.1))
    ax.plot(range(len(season_counts)), season_counts["count"], marker="o", linewidth=2.2, color="#F58518")
    ax.set_xticks(range(len(season_counts)))
    ax.set_xticklabels(season_counts["season_label"], rotation=45)
    ax.set_title("Season-wise competition flow", fontsize=13)
    ax.set_xlabel("Season")
    ax.set_ylabel("Completed Matches")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# ============================================================
# PAGE 2: PLAYER STATS
# ============================================================
elif page == "🏏 Player Stats":
    st.title("Player Performance Story")
    st.markdown("The biggest talent stories are often hidden in the small details of the ball-by-ball data.")

    if filtered_deliveries.empty:
        st.warning("No ball-by-ball records match the current filters.")
        st.stop()

    st.markdown(
        "<div style='color:#cbd5e1; font-size:0.95rem; margin-bottom:0.75rem;'>"
        "Select one of the tabs below to load the corresponding player summary. "
        "The charts appear only after you choose a view, keeping the page clean until then."
        "</div>",
        unsafe_allow_html=True,
    )

    tab_select, tab1, tab2 = st.tabs(["Select a view", "🏏 Top Run Scorers", "⚾ Top Wicket Takers"])

    with tab_select:
        st.markdown(
            "<div style='color:#94a3b8; font-size:1rem;'>"
            "Choose a tab to see either the top run scorers or the top wicket takers in the current filter."
            "</div>",
            unsafe_allow_html=True,
        )

    with tab1:
        top_scorers = (
            filtered_deliveries.groupby("batter")["batsman_runs"].sum().reset_index()
            .sort_values("batsman_runs", ascending=False)
            .head(15)
        )
        fig, ax = plt.subplots(figsize=(8.0, 4.5))
        sns.barplot(x="batsman_runs", y="batter", data=top_scorers, palette="viridis", ax=ax)
        ax.set_title("Top 15 Run Scorers in Current Filter", fontsize=13)
        ax.set_xlabel("Runs")
        ax.set_ylabel("Player")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

        st.success(
            f"The standout scoring profile belongs to {top_scorers.iloc[0]['batter']} with {int(top_scorers.iloc[0]['batsman_runs'])} runs."
        )

    with tab2:
        wickets = filtered_deliveries[filtered_deliveries["is_wicket"] == 1].copy()
        wickets = wickets[~wickets["dismissal_kind"].isin(["run out", "retired hurt", "obstructing the field"])]
        top_wickets = (
            wickets.groupby("bowler")["is_wicket"].sum().reset_index()
            .sort_values("is_wicket", ascending=False)
            .head(15)
        )
        fig, ax = plt.subplots(figsize=(8.0, 4.5))
        sns.barplot(x="is_wicket", y="bowler", data=top_wickets, palette="rocket", ax=ax)
        ax.set_title("Top 15 Wicket Takers in Current Filter", fontsize=13)
        ax.set_xlabel("Wickets")
        ax.set_ylabel("Player")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

        st.success(
            f"The bowling leadership story is led by {top_wickets.iloc[0]['bowler']} with {int(top_wickets.iloc[0]['is_wicket'])} dismissals."
        )

# ============================================================
# PAGE 3: VENUE ANALYSIS
# ============================================================
elif page == "🏟️ Venue Analysis":
    st.title("Venue Impact Explorer")
    st.markdown("Stadiums shape sentiment, pace, scoring patterns, and outcome narratives.")

    if filtered_matches.empty:
        st.warning("No venue records match the current filters.")
        st.stop()

    venue_counts = filtered_matches["venue"].value_counts().reset_index().head(10)
    venue_counts.columns = ["venue", "matches"]

    fig, ax = plt.subplots(figsize=(8.0, 4.5))
    sns.barplot(x="matches", y="venue", data=venue_counts, palette="magma", ax=ax)
    ax.set_title("Top 10 Venues by Matches Hosted in Current Filter", fontsize=13)
    ax.set_xlabel("Matches")
    ax.set_ylabel("Venue")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.subheader("🏟️ Venue Summary Table")
    venue_stats = []
    for venue in venue_counts["venue"].tolist():
        v_matches = matches[matches["venue"] == venue]
        venue_stats.append(
            {
                "Venue": venue,
                "Matches Hosted": len(v_matches),
                "Win Stories": int(v_matches["winner"].notna().sum()),
            }
        )
    st.dataframe(pd.DataFrame(venue_stats), use_container_width=True)

# ============================================================
# PAGE 4: TRENDS
# ============================================================
elif page == "📈 Trends":
    st.title("Trend & Pattern Intelligence")
    st.markdown("This page turns the IPL into a strategic narrative about phases, decisions, and momentum.")

    st.subheader("Average Runs per Over Number")
    over_runs = filtered_deliveries.groupby("over")["total_runs"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    colors = [
        "#2C3E50" if 0 <= o <= 5 else "#E74C3C" if 15 <= o <= 19 else "#3498DB"
        for o in over_runs["over"]
    ]
    ax.bar(over_runs["over"], over_runs["total_runs"], color=colors, edgecolor="white")
    ax.set_title("Average runs across match phases in current filter", fontsize=13)
    ax.set_xlabel("Over Number")
    ax.set_ylabel("Runs")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.subheader("Toss Decision Impact")
    toss = filtered_matches["toss_decision"].value_counts().reset_index()
    toss.columns = ["decision", "count"]

    col_left, col_right = st.columns([1.2, 0.8])
    with col_left:
        fig, ax = plt.subplots(figsize=(5.2, 4.0))
        ax.pie(
            toss["count"],
            labels=toss["decision"],
            autopct="%1.1f%%",
            startangle=90,
            colors=["#4C78A8", "#F58518"],
            textprops={"color": "#F8FAFC", "fontsize": 9},
            wedgeprops={"linewidth": 1, "edgecolor": "#0E1117"},
        )
        ax.set_title("Bat vs Field first preference", fontsize=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with col_right:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-card">
                <strong>Quick read:</strong><br>
                This chart shows whether teams usually choose to bat or field after winning the toss.
            </div>
            """,
            unsafe_allow_html=True,
        )

    valid = valid_matches.copy()
    toss_winners = valid[valid["toss_winner"] == valid["winner"]]
    win_pct = round(len(toss_winners) / len(valid) * 100, 1)
    st.info(f"Toss winners also won the match in **{win_pct}%** of cases, hinting at the value of winning the coin flip.")

    st.markdown("---")
    st.subheader("Simple summary")
    st.markdown(
        "This dashboard turns raw IPL data into a clear story that is easy to follow, even for someone seeing the game for the first time."
    )
