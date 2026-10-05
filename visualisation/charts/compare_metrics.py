
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.helpers import get_total_computational_gates


def _render_metric_chart(title, metric_name, value_a, value_b):
    df = pd.DataFrame({
        "Experiment": ["Experiment A", "Experiment B"],
        metric_name: [value_a, value_b],
    })

    fig = px.bar(
        df,
        x="Experiment",
        y=metric_name,
        text=metric_name,
        title=title,
    )

    fig.update_layout(
        xaxis_title="Experiment",
        yaxis_title=metric_name,
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    st.plotly_chart(fig, use_container_width=True)


def render_compare_metrics(exp_a, exp_b):
    st.subheader("3. Qubit Count Comparison")

    _render_metric_chart(
        "Number of Qubits",
        "Qubits",
        int(exp_a["Qubits"]),
        int(exp_b["Qubits"]),
    )

    st.subheader("4. Grover Iteration Comparison")

    _render_metric_chart(
        "Grover Iterations",
        "Iterations",
        int(exp_a["Iterations"]),
        int(exp_b["Iterations"]),
    )

    st.subheader("5. Oracle Query Comparison")

    _render_metric_chart(
        "Oracle Queries",
        "Oracle Queries",
        int(exp_a["Oracle Queries"]),
        int(exp_b["Oracle Queries"]),
    )

    st.subheader("6. Circuit Depth Comparison")

    _render_metric_chart(
        "Transpiled Circuit Depth",
        "Circuit Depth",
        int(exp_a["Depth"]),
        int(exp_b["Depth"]),
    )

    st.subheader("7. Total Computational Gate Count Comparison")

    gates_a = get_total_computational_gates(exp_a)
    gates_b = get_total_computational_gates(exp_b)

    _render_metric_chart(
        "Total Computational Gates",
        "Computational Gates",
        gates_a,
        gates_b,
    )