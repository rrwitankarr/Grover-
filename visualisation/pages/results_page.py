
import streamlit as st

from visualisation.charts.results_measurement import (
    render_measurement_distribution,
)
from visualisation.charts.results_iteration import (
    render_iteration_analysis,
)
from visualisation.charts.results_complexity import (
    render_circuit_complexity,
)
from visualisation.charts.results_gate_composition import (
    render_gate_composition,
)
from visualisation.charts.results_timing import (
    render_timing,
)


def render_results_page(experiment):

    # ========================================================
    # VALIDATE EXPERIMENT
    # ========================================================

    if experiment is None:
        st.warning("No experiment results found.")
        st.session_state.page = "input"
        st.rerun()
        return

    st.title("Experiment Results")

    environment = experiment.get(
        "Environment",
        "Ideal Simulator",
    )

    # ========================================================
    # EXPERIMENT CONFIGURATION
    # ========================================================

    st.subheader("Experiment Configuration")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Database Size (N)",
            experiment["N"],
        )

    with col2:
        st.metric(
            "Target",
            experiment["Target"],
        )

    with col3:
        st.metric(
            "Qubits",
            experiment["Qubits"],
        )

    with col4:
        st.metric(
            "Target Probability",
            f"{experiment['Target Probability']:.4f}",
        )

    # ========================================================
    # ENVIRONMENT AND EXECUTION DETAILS
    # ========================================================

    st.write(
        f"**Execution Environment:** "
        f"{experiment.get('Environment', 'Ideal Simulator')}"
    )

    st.write(
        f"**Target State:** "
        f"|{experiment['Target State']}⟩"
    )

    if experiment.get("Environment") == "Noisy Simulator":
        st.write(
            f"**Noise Level:** "
            f"{experiment.get('Noise Level', 'Unknown')}"
        )

    elif experiment.get("Environment") == "IBM Quantum Hardware":
        st.write(
            f"**IBM Backend:** "
            f"{experiment.get('Backend', 'Unknown')}"
        )

        st.write(
            f"**IBM Job ID:** "
            f"{experiment.get('Job ID', 'Unknown')}"
        )

    st.write(
        f"**Shots:** {experiment.get('Shots', 1024)}   |   "
        f"**Iterations:** {experiment['Iterations']}   |   "
        f"**Oracle Queries:** {experiment['Oracle Queries']}   |   "
        f"**Circuit Depth:** {experiment['Depth']}"
    )

    st.divider()

    # ========================================================
    # MEASUREMENT DISTRIBUTION
    # ========================================================

    st.subheader("Measurement Distribution")

    render_measurement_distribution(experiment)

    st.divider()

    # ========================================================
    # ITERATION ANALYSIS
    # ========================================================

    st.subheader("Grover Iteration Analysis")

    if environment == "Noisy Simulator":
        st.info(
            "This iteration-analysis chart is not noise-aware. "
            "The measurement distribution and target probability "
            "above come from the selected noisy simulation."
        )

    elif environment == "IBM Quantum Hardware":
        st.info(
            "This iteration-analysis chart is simulator-based. "
            "It does not represent repeated executions on the "
            "selected IBM hardware backend."
        )

    render_iteration_analysis(experiment)

    st.divider()

    # ========================================================
    # CIRCUIT COMPLEXITY
    # ========================================================

    st.subheader("Circuit Complexity")

    render_circuit_complexity(experiment)

    st.divider()

    # ========================================================
    # GATE COMPOSITION
    # ========================================================

    st.subheader("Gate Composition")

    render_gate_composition(experiment)

    st.divider()

    # ========================================================
    # EXECUTION TIMING
    # ========================================================

    st.subheader("Execution Timing")

    render_timing(experiment)

    st.divider()

    # ========================================================
    # QUANTUM CIRCUIT
    # ========================================================

    st.subheader("Quantum Circuit")

    if experiment["N"] <= 16:
        try:
            circuit = experiment["Circuit"]
            fig = circuit.draw(output="mpl")

            st.pyplot(
                fig,
                use_container_width=True,
            )

        except Exception as error:
            st.error(
                f"Unable to display quantum circuit: {error}"
            )

    else:
        st.info(
            "Circuit visualization is hidden for N > 16 "
            "because the circuit can become very large."
        )

    st.divider()

    # ========================================================
    # RAW MEASUREMENT COUNTS
    # ========================================================

    with st.expander("Raw Measurement Counts"):
        st.json(
            experiment.get("Counts", {})
        )

    # ========================================================
    # NAVIGATION BUTTONS
    # ========================================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Compare with Another Input",
            use_container_width=True,
        ):
            st.session_state.page = "compare"
            st.rerun()

    with col2:
        if st.button(
            "New Experiment",
            use_container_width=True,
        ):
            st.session_state.experiment_a = None
            st.session_state.experiment_b = None
            st.session_state.page = "input"
            st.rerun()

