import pandas as pd
import streamlit as st

from grover.single_target import run_grover

from charts.compare_probability import (
    render_compare_probability
)

from charts.compare_measurement import (
    render_compare_measurement
)

from charts.compare_metrics import (
    render_compare_metrics
)

from charts.compare_timing import (
    render_compare_timing
)

from charts.compare_gate_composition import (
    render_compare_gate_composition
)


N_OPTIONS = [
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    512
]

ENVIRONMENTS = [
    "Ideal Simulator",
    "Noisy Simulator",
    "IBM Quantum Hardware"
]


# ============================================================
# EXPERIMENT B INPUT
# ============================================================

def render_compare_input_page(
    experiment_a
):

    if experiment_a is None:

        st.session_state.page = "input"

        st.rerun()

        return

    st.title(
        "Compare with Another Input"
    )

    st.info(
        "Experiment A is stored. "
        "Configure Experiment B."
    )

    # ========================================================
    # EXPERIMENT A SUMMARY
    # ========================================================

    st.subheader(
        "Experiment A"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "N",
            experiment_a["N"]
        )

    with col2:

        st.metric(
            "Target",
            experiment_a["Target"]
        )

    with col3:

        st.metric(
            "Qubits",
            experiment_a["Qubits"]
        )

    with col4:

        st.metric(
            "Probability",
            f"{experiment_a['Target Probability']:.4f}"
        )

    st.divider()

    # ========================================================
    # EXPERIMENT B
    # ========================================================

    st.subheader(
        "Experiment B"
    )

    n = st.selectbox(
        "Database Size (N)",
        N_OPTIONS,
        key="compare_n"
    )

    target = st.selectbox(
        "Target",
        list(
            range(
                1,
                n + 1
            )
        ),
        key="compare_target"
    )

    shots = st.selectbox(
        "Shots",
        [1024],
        key="compare_shots"
    )

    environment = st.selectbox(
        "Execution Environment",
        ENVIRONMENTS,
        key="compare_environment"
    )

    if environment == "Noisy Simulator":

        st.info(
            "Noisy Simulator execution "
            "is not connected yet."
        )

    if environment == "IBM Quantum Hardware":

        st.info(
            "IBM Quantum Hardware execution "
            "is not connected yet."
        )

    st.divider()

    # ========================================================
    # RUN B
    # ========================================================

    if st.button(
        "Run Experiment B and Compare",
        type="primary",
        use_container_width=True
    ):

        if environment != "Ideal Simulator":

            st.error(
                "Currently only the Ideal Simulator "
                "is connected."
            )

            return

        with st.spinner(
            "Running Experiment B..."
        ):

            result = run_grover(
                n=n,
                target=target,
                shots=shots
            )

            result["Shots"] = shots
            result["Environment"] = environment

            st.session_state.experiment_b = result

            st.session_state.page = (
                "compare_results"
            )

        st.rerun()

    st.divider()

    # ========================================================
    # BACK
    # ========================================================

    if st.button(
        "← Back to Experiment A",
        use_container_width=True
    ):

        st.session_state.page = "results"

        st.rerun()


# ============================================================
# COMPARISON RESULTS
# ============================================================

def render_compare_results_page(
    exp_a,
    exp_b
):

    if exp_a is None or exp_b is None:

        st.session_state.page = "input"

        st.rerun()

        return

    st.title(
        "Experiment A vs Experiment B"
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### Experiment A"
        )

        st.write(
            f"**N:** {exp_a['N']}"
        )

        st.write(
            f"**Target:** {exp_a['Target']}"
        )

        st.write(
            f"**Target State:** "
            f"|{exp_a['Target State']}⟩"
        )

        st.write(
            f"**Qubits:** "
            f"{exp_a['Qubits']}"
        )

        st.write(
            f"**Probability:** "
            f"{exp_a['Target Probability']:.4f}"
        )

    with col2:

        st.markdown(
            "### Experiment B"
        )

        st.write(
            f"**N:** {exp_b['N']}"
        )

        st.write(
            f"**Target:** {exp_b['Target']}"
        )

        st.write(
            f"**Target State:** "
            f"|{exp_b['Target State']}⟩"
        )

        st.write(
            f"**Qubits:** "
            f"{exp_b['Qubits']}"
        )

        st.write(
            f"**Probability:** "
            f"{exp_b['Target Probability']:.4f}"
        )

    st.divider()

    # ========================================================
    # COMPARISON GRAPHS
    # ========================================================

    render_compare_probability(
        exp_a,
        exp_b
    )

    st.divider()

    render_compare_measurement(
        exp_a,
        exp_b
    )

    st.divider()

    render_compare_metrics(
        exp_a,
        exp_b
    )

    st.divider()

    render_compare_timing(
        exp_a,
        exp_b
    )

    st.divider()

    render_compare_gate_composition(
        exp_a,
        exp_b
    )

    # ========================================================
    # NUMERICAL TABLE
    # ========================================================

    st.divider()

    st.subheader(
        "10. Numerical Comparison"
    )

    gates_a = sum(
        exp_a["Circuit"].count_ops().values()
    )

    gates_b = sum(
        exp_b["Circuit"].count_ops().values()
    )

    df = pd.DataFrame({

        "Metric": [
            "N",
            "Target",
            "Qubits",
            "Grover Iterations",
            "Oracle Queries",
            "Circuit Depth",
            "Total Gates",
            "Target Probability",
            "Transpile Time",
            "Execution Time"
        ],

        "Experiment A": [
            exp_a["N"],
            exp_a["Target"],
            exp_a["Qubits"],
            exp_a["Iterations"],
            exp_a["Oracle Queries"],
            exp_a["Depth"],
            gates_a,
            exp_a["Target Probability"],
            exp_a.get(
                "Transpile Time",
                0
            ),
            exp_a.get(
                "Execution Time",
                0
            )
        ],

        "Experiment B": [
            exp_b["N"],
            exp_b["Target"],
            exp_b["Qubits"],
            exp_b["Iterations"],
            exp_b["Oracle Queries"],
            exp_b["Depth"],
            gates_b,
            exp_b["Target Probability"],
            exp_b.get(
                "Transpile Time",
                0
            ),
            exp_b.get(
                "Execution Time",
                0
            )
        ]
    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # BUTTONS
    # ========================================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Compare Another Input",
            use_container_width=True
        ):

            st.session_state.page = "compare"

            st.rerun()

    with col2:

        if st.button(
            "New Experiment",
            use_container_width=True
        ):

            st.session_state.experiment_a = None
            st.session_state.experiment_b = None

            st.session_state.page = "input"

            st.rerun()