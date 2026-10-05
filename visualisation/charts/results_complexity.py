import pandas as pd
import plotly.express as px
import streamlit as st


def render_circuit_complexity(experiment):

    st.subheader(
        "Circuit Complexity"
    )

    df = pd.DataFrame({
        "Metric": [
            "Qubits",
            "Grover Iterations",
            "Oracle Queries",
            "Circuit Depth"
        ],

        "Value": [
            experiment["Qubits"],
            experiment["Iterations"],
            experiment["Oracle Queries"],
            experiment["Depth"]
        ]
    })

    fig = px.bar(
        df,
        x="Metric",
        y="Value",
        text="Value",
        title="Grover Circuit Complexity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )