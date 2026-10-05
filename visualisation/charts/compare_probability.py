
import pandas as pd
import plotly.express as px
import streamlit as st


def render_compare_probability(exp_a, exp_b):
    st.subheader("1. Target Probability Comparison")

    probability_a = float(exp_a["Target Probability"])
    probability_b = float(exp_b["Target Probability"])

    df = pd.DataFrame({
        "Experiment": ["Experiment A", "Experiment B"],
        "Target Probability": [probability_a, probability_b],
    })

    fig = px.bar(
        df,
        x="Experiment",
        y="Target Probability",
        text=df["Target Probability"].map(lambda x: f"{x:.4f}"),
        title="Target Probability: A vs B",
        hover_data={"Target Probability": ":.4f"},
    )

    fig.update_layout(
        xaxis_title="Experiment",
        yaxis_title="Target Probability",
    )

    fig.update_yaxes(range=[0, 1], tickformat=".0%")
    fig.update_traces(textposition="outside", cliponaxis=False)

    st.plotly_chart(fig, use_container_width=True)

    difference = probability_b - probability_a
    st.caption(
        f"Difference (B − A): {difference:+.4f} "
        f"({difference * 100:+.2f} percentage points)"
    )