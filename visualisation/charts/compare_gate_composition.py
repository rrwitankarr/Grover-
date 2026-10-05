
import plotly.graph_objects as go
import streamlit as st

from utils.helpers import get_computational_gate_counts


def render_compare_gate_composition(experiment_a, experiment_b):
    st.subheader("Gate Composition Comparison")

    circuit_a = experiment_a.get("Circuit")
    circuit_b = experiment_b.get("Circuit")

    if circuit_a is None or circuit_b is None:
        st.warning("Circuit data is unavailable for one or both experiments.")
        return

    operations_a = get_computational_gate_counts(experiment_a)
    operations_b = get_computational_gate_counts(experiment_b)

    all_gates = sorted(set(operations_a) | set(operations_b))

    if not all_gates:
        st.info("No computational gates were found.")
        return

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=all_gates,
        y=[operations_a.get(gate, 0) for gate in all_gates],
        name="Experiment A",
        text=[operations_a.get(gate, 0) for gate in all_gates],
        textposition="auto",
    ))

    fig.add_trace(go.Bar(
        x=all_gates,
        y=[operations_b.get(gate, 0) for gate in all_gates],
        name="Experiment B",
        text=[operations_b.get(gate, 0) for gate in all_gates],
        textposition="auto",
    ))

    fig.update_layout(
        title="Computational Gate Counts by Type",
        xaxis_title="Gate Type",
        yaxis_title="Number of Gates",
        barmode="group",
    )

    st.plotly_chart(fig, use_container_width=True)