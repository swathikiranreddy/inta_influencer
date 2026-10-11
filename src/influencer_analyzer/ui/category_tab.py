import hashlib

import streamlit as st

from influencer_analyzer.config import CATEGORIES


def render(accounts):
    st.subheader("Discover each account’s content mix")
    st.caption("Primary category uses the most frequent post category; ties are Mixed.")
    selected = st.multiselect("Filter categories", sorted(accounts.category.unique()))
    visible = accounts[accounts.category.isin(selected)] if selected else accounts
    columns = ["account_id", "account_type", "follower_count", "post_count", "category",
               "inferred_category", "category_breakdown"]
    options = sorted(set(CATEGORIES) | set(accounts.category) | set(accounts.inferred_category))
    editor_version = hashlib.sha256(visible[columns].to_csv(index=False).encode()).hexdigest()
    with st.form("category_corrections"):
        edited = st.data_editor(
            visible[columns], hide_index=True, width="stretch",
            disabled=[column for column in columns if column != "category"],
            column_config={"category": st.column_config.SelectboxColumn(
                "Category", options=options, required=True
            )}, key=f"category_editor_{st.session_state.dataset_id}_{editor_version}",
        )
        if st.form_submit_button("Save category corrections"):
            for row in edited.itertuples():
                if row.category == row.inferred_category:
                    st.session_state.overrides.pop(row.account_id, None)
                else:
                    st.session_state.overrides[row.account_id] = row.category
            st.rerun()
    if st.button("Reset all category corrections"):
        st.session_state.overrides = {}
        st.rerun()
    st.download_button("Export categorized accounts", visible.to_csv(index=False).encode("utf-8"),
                       "categorized_accounts.csv", "text/csv")
