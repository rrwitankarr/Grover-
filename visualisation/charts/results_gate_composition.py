
import pandas as pd
import plotly.express as px
import streamlit as st


def render_gate_composition(experiment):
    st.subheader("Gate Composition")

    circuit = experiment["Circuit"]
    gate_counts = dict(circuit.count_ops())

    if not gate_counts:
        st.info("No gates found in this circuit.")
        return

    df = pd.DataFrame({
        "Gate": list(gate_counts.keys()),
        "Count": list(gate_counts.values())
    })

    fig = px.bar(
        df,
        x="Gate",
        y="Count",
        text="Count",
        title="Gate Composition"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

