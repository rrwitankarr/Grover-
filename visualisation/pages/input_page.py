
import streamlit as st

from grover.single_target import run_grover
from grover.noise_simulation import run_noisy_grover
from grover.ibm_hardware import run_ibm_grover


N_OPTIONS = [4, 8, 16, 32, 64, 128, 256, 512]

ENVIRONMENTS = [
    "Ideal Simulator",
    "Noisy Simulator",
    "IBM Quantum Hardware",
]

NOISE_OPTIONS = [0.0, 0.001, 0.005, 0.01]

IBM_BACKENDS = [
    "ibm_fez",
    "ibm_kingston",
    "ibm_marrakesh",
]


def render_input_page():
    st.title("Grover Algorithm Dashboard")
    st.write(
        "Configure and run a Grover search experiment."
    )

    st.subheader("Experiment Input")

    # --------------------------------------------------
    # SEARCH SPACE
    # --------------------------------------------------

    n = st.selectbox(
        "Database Size (N)",
        N_OPTIONS,
        key="input_n",
    )

    # --------------------------------------------------
    # TARGET
    # Targets use the existing 1-based convention.
    # --------------------------------------------------

    target = st.selectbox(
        "Target",
        list(range(1, n + 1)),
        key=f"input_target_{n}",
    )

    # --------------------------------------------------
    # SHOTS
    # --------------------------------------------------

    shots = st.selectbox(
        "Shots",
        [1024],
        key="input_shots",
    )

    # --------------------------------------------------
    # EXECUTION ENVIRONMENT
    # --------------------------------------------------

    environment = st.selectbox(
        "Execution Environment",
        ENVIRONMENTS,
        key="input_environment",
    )

    noise = None
    backend_name = None

    # --------------------------------------------------
    # NOISY SIMULATOR SETTINGS
    # --------------------------------------------------

    if environment == "Noisy Simulator":
        noise = st.selectbox(
            "Noise Level",
            NOISE_OPTIONS,
            index=2,
            format_func=lambda x: f"{x:g}",
            key="input_noise",
        )

        st.info(
            f"Depolarizing noise will be applied with "
            f"error probability {noise:g}."
        )

    # --------------------------------------------------
    # IBM HARDWARE SETTINGS
    # --------------------------------------------------

    elif environment == "IBM Quantum Hardware":
        backend_name = st.selectbox(
            "IBM Quantum Backend",
            IBM_BACKENDS,
            index=0,
            key="input_ibm_backend",
        )

        st.warning(
            "This submits a real quantum job. "
            "Hardware availability, queue time, and "
            "account usage limits may apply."
        )

    # --------------------------------------------------
    # AUTOMATICALLY CALCULATED INFORMATION
    # --------------------------------------------------

    qubits = n.bit_length() - 1

    target_state = format(
        target - 1,
        f"0{qubits}b",
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Qubits Required", qubits)

    with col2:
        st.metric(
            "Target State",
            f"|{target_state}⟩",
        )

    with col3:
        st.metric("Shots", shots)

    st.divider()

    # --------------------------------------------------
    # RUN EXPERIMENT
    # --------------------------------------------------

    if st.button(
        "Run Experiment",
        type="primary",
        use_container_width=True,
    ):
        try:
            with st.spinner(
                f"Running on {environment}..."
            ):
                # Ideal simulator
                if environment == "Ideal Simulator":
                    result = run_grover(
                        n=n,
                        target=target,
                        shots=shots,
                    )

                # Noisy Aer simulator
                elif environment == "Noisy Simulator":
                    result = run_noisy_grover(
                        n=n,
                        target=target,
                        shots=shots,
                        noise_level=noise,
                    )

                # Real IBM quantum hardware
                elif environment == "IBM Quantum Hardware":
                    result = run_ibm_grover(
                        n=n,
                        target=target,
                        shots=shots,
                        backend_name=backend_name,
                    )

                else:
                    raise ValueError(
                        "Unsupported execution environment."
                    )

                # --------------------------------------
                # STANDARDIZE RESULT METADATA
                # --------------------------------------

                result["Shots"] = shots
                result["Environment"] = environment

                if environment == "Noisy Simulator":
                    result["Noise Level"] = noise

                elif environment == "IBM Quantum Hardware":
                    result["Backend"] = backend_name

                # --------------------------------------
                # SAVE EXPERIMENT A
                # --------------------------------------

                st.session_state.experiment_a = result
                st.session_state.experiment_b = None
                st.session_state.page = "results"

            st.rerun()

        except Exception as e:
            st.error(
                f"Experiment failed: {e}"
            )
            st.exception(e)