import streamlit as st

from influencer_analyzer.services.accounts import summarize_accounts
from influencer_analyzer.services.categories import categorize_accounts
from influencer_analyzer.state import initialize
from influencer_analyzer.ui import analysis_tab, category_tab, input_tab


def main():
    st.set_page_config(page_title="Influencer Analyzer", page_icon="📊", layout="wide")
    initialize()
    st.title("Influencer Analyzer")
    st.write("Turn Instagram post data into a clear view of your creators and their content.")
    creators_only = st.sidebar.toggle("Creator accounts only", value=True)
    st.sidebar.caption("Switch off to include brands and other account types.")
    input_view, category_view, analysis_view = st.tabs(["1 · Input", "2 · Categories", "3 · Analysis"])
    with input_view:
        input_tab.render()
    posts = st.session_state.posts
    if posts is None:
        for view in [category_view, analysis_view]:
            with view:
                st.info("Upload a CSV or explore demo data in the Input tab to get started.")
        return
    all_accounts = summarize_accounts(posts)
    creator_ids = all_accounts.loc[all_accounts.account_type.eq("creator"), "account_id"]
    filtered = posts[posts.account_id.isin(creator_ids)] if creators_only else posts
    if filtered.empty:
        for view in [category_view, analysis_view]:
            with view:
                st.info("No creator accounts found. Switch off 'Creator accounts only' to view all accounts.")
        return
    accounts = categorize_accounts(filtered, summarize_accounts(filtered), st.session_state.overrides)
    with category_view:
        category_tab.render(accounts)
    with analysis_view:
        analysis_tab.render(filtered, accounts)


if __name__ == "__main__":
    main()
