
import pandas as pd
import plotly.express as px
import streamlit as st


def render_measurement_distribution(experiment):
    st.subheader("Measurement Distribution")

    n = experiment["N"]
    qubits = experiment["Qubits"]
    counts = experiment.get("Counts", {})
    target_state = experiment["Target State"]
    shots = experiment.get("Shots", sum(counts.values()))

    states = [
        format(i, f"0{qubits}b")
        for i in range(n)
    ]

    df = pd.DataFrame({
        "State": states,
        "Probability": [
            counts.get(state, 0) / shots if shots else 0
            for state in states
        ],
        "Type": [
            "Target" if state == target_state else "Other"
            for state in states
        ]
    })

    fig = px.bar(
        df,
        x="State",
        y="Probability",
        color="Type",
        title=f"Measurement Distribution (N={n})"
    )

    fig.update_yaxes(
        title="Probability",
        range=[0, 1]
    )

    st.plotly_chart(fig, use_container_width=True)

