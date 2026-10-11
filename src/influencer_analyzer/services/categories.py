import pandas as pd


def categorize_accounts(posts: pd.DataFrame, accounts: pd.DataFrame, overrides: dict) -> pd.DataFrame:
    counts = posts.groupby(["account_id", "content_category"]).size()
    rows = []
    for account_id, group in counts.groupby(level=0):
        values = group.droplevel(0).sort_values(ascending=False)
        winners = values[values.eq(values.max())].index.tolist()
        primary = winners[0] if len(winners) == 1 else "Mixed"
        breakdown = "; ".join(f"{name}: {count / values.sum():.1%}" for name, count in values.items())
        rows.append({
            "account_id": account_id, "inferred_category": primary,
            "category": overrides.get(account_id, primary), "category_breakdown": breakdown,
        })
    return accounts.merge(pd.DataFrame(rows), on="account_id", validate="one_to_one")
