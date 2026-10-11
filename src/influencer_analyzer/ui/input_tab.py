from pathlib import Path

import streamlit as st

from influencer_analyzer.config import REQUIRED_COLUMNS
from influencer_analyzer.state import load_dataset


def render():
    st.subheader("Start with your post data")
    st.write("Upload an Instagram analytics CSV. Categories and analysis update from this data.")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded is not None:
        try:
            load_dataset(uploaded.getvalue())
        except ValueError as exc:
            st.error(str(exc))
            st.info("The previous valid dataset, if any, remains active.")
    if uploaded is None and st.button("Explore demo data"):
        load_dataset((Path(__file__).parents[1] / "data" / "demo.csv").read_bytes())
    for warning in st.session_state.warnings:
        st.warning(warning)
    posts = st.session_state.posts
    if posts is not None:
        st.success(f"Active dataset: {len(posts):,} posts · {posts.account_id.nunique():,} accounts")
        st.dataframe(posts.head(100), hide_index=True, width="stretch")
        st.caption("Preview shows the first 100 posts. The full dataset is used for analysis.")
    with st.expander("CSV format"):
        st.code(",".join(REQUIRED_COLUMNS), language=None)
        st.write("One row per post. Dates are interpreted as UTC. Account IDs are preserved as text.")
    st.caption("Data and category corrections last for this browser session. Export results before leaving.")
