from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_demo_and_category_save():
    app = AppTest.from_file(str(Path(__file__).parents[1] / "src/influencer_analyzer/app.py"))
    app.run()
    assert not app.exception
    app.button[0].click().run()
    assert not app.exception
    assert app.metric[0].value == "3"
    app.button[1].click().run()
    assert not app.exception
    app.toggle[0].set_value(False).run()
    assert app.metric[0].value == "4"
    assert not app.exception
