
import plotly.graph_objects as go
import streamlit as st


def render_compare_measurement(experiment_a, experiment_b):
    st.subheader("Measurement Distribution Comparison")

    n_a = int(experiment_a["N"])
    n_b = int(experiment_b["N"])

    # Distributions can only be overlaid when both experiments
    # have the same number of possible states.
    if n_a != n_b:
        st.info(
            f"Measurement distributions cannot be overlaid because "
            f"Experiment A has N={n_a} and Experiment B has N={n_b}. "
            "Compare their target probabilities and circuit metrics below."
        )
        return

    n = n_a
    num_qubits = n.bit_length() - 1

    if n <= 1 or (n & (n - 1)) != 0:
        st.error("N must be a power of two greater than 1.")
        return

    # --------------------------------------------------
    # Normalize Qiskit measurement counts
    # --------------------------------------------------
    def normalize_counts(raw_counts):
        normalized = {}

        for key, value in raw_counts.items():
            state = str(key).replace(" ", "").replace("_", "")
            count = int(value)

            # Accept binary strings and integer state indices.
            if not state or count < 0:
                continue

            if all(bit in "01" for bit in state):
                # Binary measurement key.
                if len(state) > num_qubits:
                    continue
                state = state.zfill(num_qubits)
            else:
                try:
                    index = int(state)
                except ValueError:
                    continue

                if index < 0 or index >= n:
                    continue

                state = format(index, f"0{num_qubits}b")

            normalized[state] = normalized.get(state, 0) + count

        return normalized

    counts_a = normalize_counts(experiment_a.get("Counts", {}))
    counts_b = normalize_counts(experiment_b.get("Counts", {}))

    shots_a = sum(counts_a.values())
    shots_b = sum(counts_b.values())

    if shots_a == 0 or shots_b == 0:
        st.warning(
            "Measurement counts are missing or empty for one or both experiments."
        )
        return

    # Generate every possible state, including states with zero counts.
    states = [format(i, f"0{num_qubits}b") for i in range(n)]
    positions = list(range(n))

    probabilities_a = [
        counts_a.get(state, 0) / shots_a
        for state in states
    ]

    probabilities_b = [
        counts_b.get(state, 0) / shots_b
        for state in states
    ]

    # --------------------------------------------------
    # Target states
    # --------------------------------------------------
    target_a = str(experiment_a.get("Target State", "")).strip()
    target_b = str(experiment_b.get("Target State", "")).strip()

    # Remove ket notation if the stored value contains it.
    target_a = target_a.replace("|", "").replace("⟩", "").replace(">", "")
    target_b = target_b.replace("|", "").replace("⟩", "").replace(">", "")

    # Handle accidental spaces in binary strings.
    target_a = target_a.replace(" ", "")
    target_b = target_b.replace(" ", "")

    target_index_a = (
        int(target_a, 2)
        if target_a in states
        else None
    )

    target_index_b = (
        int(target_b, 2)
        if target_b in states
        else None
    )

    # --------------------------------------------------
    # Build comparison graph
    # --------------------------------------------------
    fig = go.Figure()

    # Numeric x positions prevent categorical-axis compression.
    # Slightly offset the bars so both experiments remain visible.
    bar_width = 0.38

    fig.add_trace(
        go.Bar(
            x=[p - bar_width / 2 for p in positions],
            y=probabilities_a,
            width=bar_width,
            name="Experiment A",
            marker_color="#0969DA",
            customdata=[
                (states[i], counts_a.get(states[i], 0))
                for i in positions
            ],
            hovertemplate=(
                "Experiment A<br>"
                "State: |%{customdata[0]}⟩<br>"
                "Probability: %{y:.2%}<br>"
                "Counts: %{customdata[1]}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Bar(
            x=[p + bar_width / 2 for p in positions],
            y=probabilities_b,
            width=bar_width,
            name="Experiment B",
            marker_color="#80C7FF",
            customdata=[
                (states[i], counts_b.get(states[i], 0))
                for i in positions
            ],
            hovertemplate=(
                "Experiment B<br>"
                "State: |%{customdata[0]}⟩<br>"
                "Probability: %{y:.2%}<br>"
                "Counts: %{customdata[1]}"
                "<extra></extra>"
            ),
        )
    )

    # Target markers are placed at the actual state positions.
    if target_index_a is not None:
        fig.add_vline(
            x=target_index_a,
            line_dash="dash",
            line_color="#0969DA",
            annotation_text=f"Target A: |{target_a}⟩",
            annotation_position="top left",
        )

    if target_index_b is not None:
        fig.add_vline(
            x=target_index_b,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Target B: |{target_b}⟩",
            annotation_position="top right",
        )

    # Give annotations extra room above the chart.
    fig.update_layout(
        title=f"Measurement Distribution Comparison (N={n})",
        xaxis=dict(
            title="Measured Quantum State",
            tickmode="array",
            tickvals=positions,
            ticktext=states,
            tickangle=-45,
            range=[-0.7, n - 0.3],
            type="linear",
        ),
        yaxis=dict(
            title="Probability",
            range=[0, 1.15],
            tickformat=".0%",
        ),
        barmode="overlay",
        bargap=0.15,
        hovermode="closest",
        margin=dict(
            t=120,
            b=110,
            l=60,
            r=40,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # --------------------------------------------------
    # Display useful validation information
    # --------------------------------------------------
    with st.expander("Measurement count validation"):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Experiment A**")
            st.write(f"Valid measurement counts: {shots_a}")
            st.write(f"Target state: |{target_a}⟩")
            st.write(
                f"Target probability: "
                f"{probabilities_a[target_index_a]:.2%}"
                if target_index_a is not None
                else "Target state is invalid."
            )

        with col2:
            st.write("**Experiment B**")
            st.write(f"Valid measurement counts: {shots_b}")
            st.write(f"Target state: |{target_b}⟩")
            st.write(
                f"Target probability: "
                f"{probabilities_b[target_index_b]:.2%}"
                if target_index_b is not None
                else "Target state is invalid."
            )

        st.caption(
            "Probabilities are calculated from the sum of valid measurement "
            "counts for each experiment."
        )