"""Student Performance Dashboard — Streamlit app.

Run with:
    streamlit run app.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "study.csv"
PALETTE = ["#4A90D9", "#E87C5A", "#5AB88A", "#A78BFA"]
SCORES = ["Mathematics Score", "Reading Score", "Writing Score"]

st.set_page_config(
    page_title="Student Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] { font-size: 2rem; color: #4A90D9; }
    [data-testid="stMetricDelta"] { font-size: 0.85rem; }
    .section-header { color: #333; border-left: 4px solid #4A90D9;
                      padding-left: 10px; margin-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


if not DATA_PATH.exists():
    st.error(
        f"Couldn't find the dataset at `{DATA_PATH}`. "
        "Run the cleaning notebook first, or check that `data/study.csv` exists."
    )
    st.stop()

df_full = load_data(DATA_PATH)

# ---- Sidebar filters -------------------------------------------------
st.sidebar.title("🔍 Filters")
subject = st.sidebar.selectbox("Subject", SCORES)

genders = ["All"] + sorted(df_full["Gender"].unique().tolist())
sel_gender = st.sidebar.selectbox("Gender", genders)

edu_options = sorted(df_full["Parental Level of Education"].unique().tolist())
sel_edu = st.sidebar.multiselect(
    "Parental Education",
    options=edu_options,
    default=edu_options,
)

df = df_full.copy()
if sel_gender != "All":
    df = df[df["Gender"] == sel_gender]
df = df[df["Parental Level of Education"].isin(sel_edu)]

if df.empty:
    st.warning("No students match the current filters. Try widening your selection.")
    st.stop()

# ---- Header ------------------------------------------------------------
st.title("📚 Student Performance Dashboard")
st.caption(f"Showing **{len(df):,}** of **{len(df_full):,}** students")
st.markdown("---")


# ---- Metrics -------------------------------------------------------------
def delta(col: str) -> str:
    filtered_avg = df[col].mean()
    overall_avg = df_full[col].mean()
    return f"{filtered_avg - overall_avg:+.1f} vs overall"


c1, c2, c3 = st.columns(3)
c1.metric("Avg Mathematics", f"{df['Mathematics Score'].mean():.1f}", delta("Mathematics Score"))
c2.metric("Avg Reading", f"{df['Reading Score'].mean():.1f}", delta("Reading Score"))
c3.metric("Avg Writing", f"{df['Writing Score'].mean():.1f}", delta("Writing Score"))

st.markdown("---")

# ---- Tabs ----------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Distribution", "👨‍👩‍👧 Parental Impact", "👥 Demographics", "🔗 Correlation"]
)

with tab1:
    st.markdown(f"<h3 class='section-header'>{subject} Distribution</h3>", unsafe_allow_html=True)
    col_a, col_b = st.columns([2, 1])
    with col_a:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df[subject], bins=20, ax=ax, color=PALETTE[0], edgecolor="white", kde=True)
        ax.set_xlabel("Score")
        ax.set_ylabel("Number of Students")
        ax.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig)
    with col_b:
        st.markdown("**Summary Stats**")
        st.dataframe(
            df[subject].describe().rename("Value").to_frame().style.format("{:.1f}"),
            use_container_width=True,
        )

with tab2:
    st.markdown(
        "<h3 class='section-header'>Parental Education × Score × Prep Course</h3>",
        unsafe_allow_html=True,
    )
    fig2, ax2 = plt.subplots(figsize=(11, 5))
    sns.boxplot(
        data=df,
        x="Parental Level of Education",
        y=subject,
        hue="Preparation Course",
        ax=ax2,
        palette=PALETTE[:2],
    )
    ax2.set_xlabel("Parental Level of Education")
    ax2.set_ylabel(subject)
    plt.xticks(rotation=35, ha="right")
    ax2.spines[["top", "right"]].set_visible(False)
    fig2.tight_layout()
    st.pyplot(fig2)

with tab3:
    st.markdown("<h3 class='section-header'>Demographics</h3>", unsafe_allow_html=True)
    d1, d2 = st.columns(2)
    with d1:
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        counts = df["Gender"].value_counts()
        ax3.pie(
            counts,
            labels=counts.index,
            autopct="%1.1f%%",
            colors=PALETTE,
            startangle=90,
            wedgeprops={"edgecolor": "white", "linewidth": 2},
        )
        ax3.set_title("Gender Split")
        st.pyplot(fig3)
    with d2:
        fig4, ax4 = plt.subplots(figsize=(5, 4))
        sns.countplot(
            data=df,
            y="Parental Level of Education",
            order=df["Parental Level of Education"].value_counts().index,
            ax=ax4,
            color=PALETTE[0],
        )
        ax4.set_xlabel("Count")
        ax4.set_ylabel("")
        ax4.spines[["top", "right"]].set_visible(False)
        ax4.set_title("Parental Education Breakdown")
        st.pyplot(fig4)

with tab4:
    st.markdown("<h3 class='section-header'>Score Correlations</h3>", unsafe_allow_html=True)
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    corr = df[SCORES].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", linewidths=0.5, ax=ax5, vmin=0, vmax=1)
    ax5.set_title("Pearson Correlation between Scores")
    st.pyplot(fig5)

# ---- Footer ----------------------------------------------------------------
st.markdown("---")
col_l, col_r = st.columns([3, 1])
with col_l:
    if st.checkbox("Show raw data"):
        st.dataframe(df, use_container_width=True)
with col_r:
    st.download_button(
        "⬇️ Download filtered data",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_students.csv",
        mime="text/csv",
    )
