import pandas as pd


def posting_frequency(posts: pd.DataFrame) -> pd.Series:
    """Posts/week over the shared uploaded observation window, inclusive of both dates."""
    days = (posts.post_datetime.max().normalize() - posts.post_datetime.min().normalize()).days + 1
    return (posts.groupby("account_id").size() * 7 / days).rename("posts_per_week")


def monthly_activity(posts: pd.DataFrame) -> pd.DataFrame:
    return posts.assign(month=posts.post_datetime.dt.strftime("%Y-%m")).groupby(
        "month", as_index=False
    ).agg(posts=("post_id", "size"))
