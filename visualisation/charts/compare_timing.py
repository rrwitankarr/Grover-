
import pandas as pd
import plotly.express as px
import streamlit as st


def _render_timing_chart(title, metric_name, value_a, value_b):
    values = []

    for experiment, value in [
        ("Experiment A", value_a),
        ("Experiment B", value_b),
    ]:
        # Missing or invalid timing values should not crash the chart.
        try:
            numeric_value = float(value)
            if numeric_value < 0:
                numeric_value = 0.0
        except (TypeError, ValueError):
            numeric_value = 0.0

        values.append({
            "Experiment": experiment,
            metric_name: numeric_value,
        })

    df = pd.DataFrame(values)

    fig = px.bar(
        df,
        x="Experiment",
        y=metric_name,
        text=df[metric_name].map(lambda value: f"{value:.6f} s"),
        title=title,
        labels={
            "Experiment": "Experiment",
            metric_name: "Time (seconds)",
        },
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_layout(
        yaxis=dict(rangemode="tozero"),
        margin=dict(t=70, b=40),
    )

    st.plotly_chart(fig, use_container_width=True)


def render_compare_timing(exp_a, exp_b):
    st.subheader("Execution Time Comparison")

    # Transpilation time
    st.markdown("#### Transpile Time")

    _render_timing_chart(
        title="Transpilation Time: A vs B",
        metric_name="Transpile Time",
        value_a=exp_a.get("Transpile Time", 0),
        value_b=exp_b.get("Transpile Time", 0),
    )

    # Circuit execution time
    st.markdown("#### Execution Time")

    _render_timing_chart(
        title="Execution Time: A vs B",
        metric_name="Execution Time",
        value_a=exp_a.get("Execution Time", 0),
        value_b=exp_b.get("Execution Time", 0),
    )

    # Combined timing, excluding unrelated UI and plotting time
    st.markdown("#### Combined Transpile + Execution Time")

    def combined_time(experiment):
        try:
            transpile = float(experiment.get("Transpile Time", 0) or 0)
            execution = float(experiment.get("Execution Time", 0) or 0)

            if transpile < 0 or execution < 0:
                return 0.0

            return transpile + execution
        except (TypeError, ValueError):
            return 0.0

    _render_timing_chart(
        title="Combined Transpile + Execution Time: A vs B",
        metric_name="Combined Time",
        value_a=combined_time(exp_a),
        value_b=combined_time(exp_b),
    )