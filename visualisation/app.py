import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from pages.input_page import render_input_page
from pages.results_page import render_results_page
from pages.compare_page import (
    render_compare_input_page,
    render_compare_results_page
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Grover Algorithm Dashboard",
    page_icon="⚛️",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "input"

if "experiment_a" not in st.session_state:
    st.session_state.experiment_a = None

if "experiment_b" not in st.session_state:
    st.session_state.experiment_b = None


# ============================================================
# PAGE ROUTING
# ============================================================

if st.session_state.page == "input":

    render_input_page()


elif st.session_state.page == "results":

    render_results_page(
        st.session_state.experiment_a
    )


elif st.session_state.page == "compare":

    render_compare_input_page(
        st.session_state.experiment_a
    )


elif st.session_state.page == "compare_results":

    render_compare_results_page(
        st.session_state.experiment_a,
        st.session_state.experiment_b
    )