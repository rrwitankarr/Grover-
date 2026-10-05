
import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from qiskit import transpile
from qiskit_aer import AerSimulator

from grover.single_target import (
    create_grover_circuit,
    calculate_iterations,
)



@st.cache_data(show_spinner=False)
def run_iteration_analysis(n, target, shots=1024):
    simulator = AerSimulator()
    optimal_iterations = calculate_iterations(n)
    max_iterations = min(optimal_iterations + 4, 20)

    rows = []

    for iteration in range(max_iterations + 1):
        circuit, target_state, actual_iterations = (
            create_grover_circuit(
                n=n,
                target=target,
                iterations=iteration,
            )
        )

        # Confirm the generated object is a Qiskit circuit.
        if not hasattr(circuit, "num_qubits"):
            raise TypeError(
                "create_grover_circuit() did not return "
                "a QuantumCircuit as its first value. "
                f"Received: {type(circuit).__name__}"
            )

        result = simulator.run(
            circuit,
            shots=shots,
        ).result()

        counts = result.get_counts()
        target_count = counts.get(target_state, 0)

        rows.append({
            "Iterations": actual_iterations,
            "Target Probability": target_count / shots,
            "Circuit Depth": circuit.depth(),
            "Target Count": target_count,
        })

    return pd.DataFrame(rows)


def render_iteration_analysis(experiment):
    """Display the interactive Grover iteration graphs."""

    st.subheader("Grover Iteration Analysis")

    n = int(experiment["N"])
    target = int(experiment["Target"])
    shots = int(experiment.get("Shots", 1024))

    with st.spinner(
        "Analysing Grover iterations..."
    ):
        df = run_iteration_analysis(
            n,
            target,
            shots,
        )

    if df.empty:
        st.warning("No iteration-analysis results were generated.")
        return

    optimal_iterations = calculate_iterations(n)

    st.caption(
        f"Search space: N={n} | "
        f"Target: {target} | "
        f"Expected optimal iterations: {optimal_iterations}"
    )

    # --------------------------------------------------
    # Graph 1: Target probability vs iterations
    # --------------------------------------------------

    st.markdown("#### Target Probability vs Iterations")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Iterations"],
            y=df["Target Probability"],
            mode="lines+markers",
            name="Measured probability",
            hovertemplate=(
                "Iterations: %{x}<br>"
                "Target probability: %{y:.2%}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_vline(
        x=optimal_iterations,
        line_dash="dash",
        annotation_text="Expected optimum",
    )

    fig.update_layout(
        xaxis_title="Number of Grover Iterations",
        yaxis_title="Target Probability",
        yaxis=dict(range=[0, 1]),
        hovermode="x unified",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # --------------------------------------------------
    # Graph 2: Circuit depth vs iterations
    # --------------------------------------------------

    st.markdown("#### Circuit Depth vs Iterations")

    depth_fig = px.line(
        df,
        x="Iterations",
        y="Circuit Depth",
        markers=True,
        title="Circuit Depth Growth",
    )

    depth_fig.update_layout(
        xaxis_title="Number of Grover Iterations",
        yaxis_title="Transpiled Circuit Depth",
    )

    st.plotly_chart(
        depth_fig,
        use_container_width=True,
    )

    # --------------------------------------------------
    # Results table
    # --------------------------------------------------

    with st.expander("View iteration data"):
        display_df = df.copy()

        display_df["Target Probability"] = (
            display_df["Target Probability"] * 100
        ).round(2)

        display_df = display_df.rename(
            columns={
                "Target Probability": "Target Probability (%)",
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )