import hashlib

import streamlit as st

from influencer_analyzer.services.ingestion import read_csv


def initialize():
    for key, value in {"posts": None, "overrides": {}, "dataset_id": "", "warnings": []}.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_dataset(content: bytes):
    dataset_id = hashlib.sha256(content).hexdigest()
    if dataset_id != st.session_state.dataset_id:
        posts, warnings = read_csv(content)
        st.session_state.update(
            posts=posts, overrides={}, dataset_id=dataset_id, warnings=warnings
        )
