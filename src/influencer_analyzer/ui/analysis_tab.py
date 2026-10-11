import plotly.express as px
import streamlit as st

from influencer_analyzer.services.analytics import monthly_activity, posting_frequency


def render(posts, accounts):
    st.subheader("Understand and compare your influencers")
    cols = st.columns(3)
    cols[0].metric("Accounts", f"{len(accounts):,}")
    cols[1].metric("Posts", f"{len(posts):,}")
    cols[2].metric("Median followers", f"{accounts.follower_count.median():,.0f}")
    left, right = st.columns(2)
    with left:
        counts = accounts.groupby("category", as_index=False).size()
        st.plotly_chart(px.bar(counts, x="category", y="size", title="Accounts by category",
                               labels={"size": "Accounts", "category": "Category"}),
                        width="stretch")
    with right:
        st.plotly_chart(px.bar(posts.groupby("media_type", as_index=False).size(),
                               x="media_type", y="size", title="Post formats",
                               labels={"size": "Posts", "media_type": "Format"}), width="stretch")
    st.plotly_chart(px.line(monthly_activity(posts), x="month", y="posts", markers=True,
                            title="Monthly posting activity"), width="stretch")
    comparison = accounts.merge(posting_frequency(posts), on="account_id")
    selected = st.multiselect("Compare accounts (up to 5)", accounts.account_id.tolist(),
                              max_selections=5)
    if selected:
        st.dataframe(comparison[comparison.account_id.isin(selected)], hide_index=True,
                     width="stretch")
    st.dataframe(comparison.sort_values("follower_count", ascending=False), hide_index=True,
                 width="stretch")
    st.caption("Follower counts use the latest observed post for each account; equal timestamps use "
               "post ID as a tie breaker. Posts/week uses the shared uploaded date window. "
               "Likes, comments, and reach are absent, so engagement and campaign ROI are unavailable.")
    st.download_button("Export analysis", comparison.to_csv(index=False).encode("utf-8"),
                       "influencer_analysis.csv", "text/csv")
