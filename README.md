# Influencer Analyzer

A uv-managed Python/Streamlit application with Input, Categories, and Analysis tabs.

## Run locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run from this directory:

```powershell
uv sync
uv run streamlit run src/influencer_analyzer/app.py
```

Open the local URL printed by Streamlit. Upload your Instagram analytics CSV or click
**Explore demo data** for a small fictional dataset. Creator accounts are shown by default;
the sidebar switch includes brands and other account types.

## Workflow

1. Upload and validate post-level data in Input. Invalid uploads leave the previous valid dataset active.
2. Review account categories and content shares. Edit Category, then save corrections.
   Education and custom categories from your upload are supported. Export categorized accounts.
3. Explore follower counts, post formats, monthly activity, and account comparisons. Export analysis.

Uploads and corrections exist only in the browser session. A different dataset resets corrections.
Exported summaries are reports, not post-level files to re-upload. No Instagram API or database is used.

## Data rules

Required fields: `post_id,account_id,account_type,follower_count,media_type,content_category,traffic_source,has_call_to_action,post_datetime,post_date`.
One row represents one post. IDs remain text. Required values cannot be blank. Follower counts must
be non-negative integers; call-to-action values are 0 or 1. Dates are interpreted as UTC and must agree.
Identical rows are removed with a warning; conflicting post IDs are rejected. Inconsistent account types
produce a warning and use the latest observed type. Creator filtering retains all posts of accounts
whose latest observed type is creator.

The primary account category is its most frequent post category. Ties are Mixed. Manual corrections
are stored separately from the source data. Follower counts use the latest observed timestamp;
ties use the lexically greatest post ID. Follower counts are never summed across posts.
Posts/week uses the inclusive shared date window of the displayed posts, not account lifetime.
Content shares reflect only uploaded posts. Engagement, reach, growth history, and ROI cannot be
inferred from this dataset. Monthly activity counts uploaded posts and omits months with none.

## Development

```powershell
uv run pytest
uv run ruff check .
```

`src/influencer_analyzer/ui` contains the tabs; `services` contains independent ingestion,
account aggregation, classification, and analytics. `state.py` owns session data and corrections.
`config.py` owns required fields and category choices. The packaged demo is fictional.
