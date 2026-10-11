from pathlib import Path

import pytest

from influencer_analyzer.services.accounts import summarize_accounts
from influencer_analyzer.services.analytics import posting_frequency
from influencer_analyzer.services.categories import categorize_accounts
from influencer_analyzer.services.ingestion import read_csv

DEMO = Path(__file__).parents[1] / "src/influencer_analyzer/data/demo.csv"


def test_categories_latest_followers_and_overrides():
    posts, _ = read_csv(DEMO.read_bytes())
    result = categorize_accounts(posts, summarize_accounts(posts), {"001": "Education"})
    indexed = result.set_index("account_id")
    assert indexed.loc["001", "follower_count"] == 12800
    assert indexed.loc["001", "inferred_category"] == "Fashion"
    assert indexed.loc["001", "category"] == "Education"
    assert indexed.loc["003", "category"] == "Mixed"
    assert "Fashion: 66.7%" in indexed.loc["001", "category_breakdown"]
    assert posting_frequency(posts).loc["001"] == pytest.approx(3 * 7 / 38)


def test_duplicate_and_conflicting_posts():
    text = DEMO.read_text()
    posts, warnings = read_csv((text + text.splitlines()[1] + "\n").encode())
    assert len(posts) == 8
    assert warnings
    with pytest.raises(ValueError, match="conflicting"):
        read_csv((text + text.splitlines()[1].replace("12000", "13000") + "\n").encode())


def test_account_type_changes_use_latest_record():
    posts, warnings = read_csv(DEMO.read_text().replace("001,creator", "001,brand", 1).encode())
    assert warnings
    assert summarize_accounts(posts).set_index("account_id").loc["001", "account_type"] == "creator"


@pytest.mark.parametrize("old,new,message", [
    ("12000", "-1", "Follower"),
    ("12000", "1.5", "Follower"),
    ("2025-01-01 10:00:00", "bad-date", "invalid dates"),
    ("post_id,", "missing_id,", "Missing required"),
])
def test_invalid_upload(old, new, message):
    with pytest.raises(ValueError, match=message):
        read_csv(DEMO.read_text().replace(old, new, 1).encode())
