import pandas as pd


def summarize_accounts(posts: pd.DataFrame) -> pd.DataFrame:
    ordered = posts.sort_values(["post_datetime", "post_id"], kind="stable")
    latest = ordered.drop_duplicates("account_id", keep="last").set_index("account_id")
    summary = posts.groupby("account_id", sort=True).agg(
        post_count=("post_id", "size"),
        first_post=("post_datetime", "min"),
        last_post=("post_datetime", "max"),
    )
    summary["account_type"] = latest["account_type"]
    summary["follower_count"] = latest["follower_count"]
    summary["preferred_media"] = posts.groupby("account_id")["media_type"].agg(
        lambda values: ", ".join(sorted(values.mode()))
    )
    return summary.reset_index()
