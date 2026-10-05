import pandas as pd
import plotly.express as px
import streamlit as st


def render_timing(experiment):

    st.subheader(
        "Execution Information"
    )

    df = pd.DataFrame({
        "Stage": [
            "Transpile",
            "Execution"
        ],

        "Time": [
            experiment.get(
                "Transpile Time",
                0
            ),

            experiment.get(
                "Execution Time",
                0
            )
        ]
    })

    fig = px.bar(
        df,
        x="Stage",
        y="Time",
        text="Time",
        title="Transpile and Execution Time"
    )

    fig.update_yaxes(
        title="Time (seconds)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )