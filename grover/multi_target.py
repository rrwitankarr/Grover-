import math
import time
import csv
import os

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


# ============================================================
# SEARCH SPACE VALIDATION
# ============================================================

def validate_search_space(n):
    return n >= 2 and (n & (n - 1)) == 0


# ============================================================
# NUMBER OF QUBITS
# ============================================================

def calculate_qubits(n):
    return int(math.log2(n))


# ============================================================
# NUMBER OF GROVER ITERATIONS
# ============================================================

def calculate_iterations(n, marked_count):
    """
    Optimal iteration estimate for M marked states:

        k ≈ π/4 * sqrt(N/M)

    A more accurate amplitude-based expression is used
    to determine the integer iteration count.
    """

    theta = math.asin(
        math.sqrt(marked_count / n)
    )

    iterations = round(
        math.pi / (4 * theta) - 0.5
    )

    return max(1, iterations)


# ============================================================
# ORACLE FOR MULTIPLE MARKED STATES
# ============================================================

def create_multi_target_oracle(
    num_qubits,
    marked_states
):

    oracle = QuantumCircuit(num_qubits)

    for target_state in marked_states:

        # Convert binary target into the required
        # qubit representation.

        for qubit in range(num_qubits):

            if target_state[
                num_qubits - 1 - qubit
            ] == "0":

                oracle.x(qubit)

        # Phase flip for this marked state.

        if num_qubits == 1:

            oracle.z(0)

        elif num_qubits == 2:

            oracle.cz(0, 1)

        else:

            oracle.h(num_qubits - 1)

            oracle.mcx(
                list(range(num_qubits - 1)),
                num_qubits - 1
            )

            oracle.h(num_qubits - 1)

        # Undo X transformations.

        for qubit in range(num_qubits):

            if target_state[
                num_qubits - 1 - qubit
            ] == "0":

                oracle.x(qubit)

    return oracle


# ============================================================
# DIFFUSER
# ============================================================

def create_diffuser(num_qubits):

    diffuser = QuantumCircuit(
        num_qubits
    )

    diffuser.h(
        range(num_qubits)
    )

    diffuser.x(
        range(num_qubits)
    )

    if num_qubits == 1:

        diffuser.z(0)

    elif num_qubits == 2:

        diffuser.cz(0, 1)

    else:

        diffuser.h(
            num_qubits - 1
        )

        diffuser.mcx(
            list(range(num_qubits - 1)),
            num_qubits - 1
        )

        diffuser.h(
            num_qubits - 1
        )

    diffuser.x(
        range(num_qubits)
    )

    diffuser.h(
        range(num_qubits)
    )

    return diffuser


# ============================================================
# CREATE MULTI-TARGET GROVER CIRCUIT
# ============================================================

def create_multi_target_circuit(
    n,
    marked_targets,
    iterations=None
):

    num_qubits = calculate_qubits(n)

    # Convert user-facing targets 1...N
    # into zero-based binary states.

    marked_states = []

    for target in marked_targets:

        target_index = target - 1

        target_state = format(
            target_index,
            f"0{num_qubits}b"
        )

        marked_states.append(
            target_state
        )

    # Calculate optimal iterations.

    if iterations is None:

        iterations = calculate_iterations(
            n,
            len(marked_states)
        )

    circuit = QuantumCircuit(
        num_qubits,
        num_qubits
    )

    # --------------------------------------------------------
    # INITIAL SUPERPOSITION
    # --------------------------------------------------------

    circuit.h(
        range(num_qubits)
    )

    # --------------------------------------------------------
    # GROVER ITERATIONS
    # --------------------------------------------------------

    oracle = create_multi_target_oracle(
        num_qubits,
        marked_states
    )

    diffuser = create_diffuser(
        num_qubits
    )

    for _ in range(iterations):

        circuit.compose(
            oracle,
            inplace=True
        )

        circuit.compose(
            diffuser,
            inplace=True
        )

    # --------------------------------------------------------
    # MEASUREMENT
    # --------------------------------------------------------

    circuit.measure(
        range(num_qubits),
        range(num_qubits)
    )

    return (
        circuit,
        marked_states,
        iterations
    )


# ============================================================
# RUN MULTI-TARGET GROVER
# ============================================================

def run_multi_target(
    n,
    marked_targets,
    iterations=None,
    shots=1024
):

    (
        circuit,
        marked_states,
        iterations
    ) = create_multi_target_circuit(
        n,
        marked_targets,
        iterations
    )

    simulator = AerSimulator()

    start_transpile = time.perf_counter()

    compiled_circuit = transpile(
        circuit,
        simulator
    )

    end_transpile = time.perf_counter()

    transpilation_time = (
        end_transpile -
        start_transpile
    )

    start_execution = time.perf_counter()

    result = simulator.run(
        compiled_circuit,
        shots=shots
    ).result()

    end_execution = time.perf_counter()

    execution_time = (
        end_execution -
        start_execution
    )

    counts = result.get_counts()

    # --------------------------------------------------------
    # Individual target probabilities
    # --------------------------------------------------------

    target_probabilities = {}

    for state in marked_states:

        count = counts.get(
            state,
            0
        )

        target_probabilities[state] = (
            count / shots
        )

    # --------------------------------------------------------
    # Combined marked-state probability
    # --------------------------------------------------------

    combined_probability = sum(
        target_probabilities.values()
    )

    return {
        "N": n,
        "Qubits": calculate_qubits(n),
        "Marked Targets": marked_targets,
        "Marked States": marked_states,
        "M": len(marked_states),
        "Iterations": iterations,
        "Oracle Queries": iterations,
        "Circuit Depth": compiled_circuit.depth(),
        "Target Probabilities":
            target_probabilities,
        "Combined Probability":
            combined_probability,
        "Transpile Time":
            transpilation_time,
        "Execution Time":
            execution_time,
        "Counts":
            counts,
        "Circuit":
            circuit
    }


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_result(result):

    print("\n")
    print("=" * 70)
    print("MULTI-TARGET GROVER SEARCH")
    print("=" * 70)

    print(
        "Search space size (N):",
        result["N"]
    )

    print(
        "Number of qubits:",
        result["Qubits"]
    )

    print(
        "Number of marked states (M):",
        result["M"]
    )

    print(
        "Marked targets:",
        result["Marked Targets"]
    )

    print(
        "Marked quantum states:",
        [
            "|" + state + ">"
            for state in result["Marked States"]
        ]
    )

    print(
        "Grover iterations:",
        result["Iterations"]
    )

    print(
        "Oracle queries:",
        result["Oracle Queries"]
    )

    print(
        "Circuit depth:",
        result["Circuit Depth"]
    )

    print("\nIndividual Target Probabilities")
    print("-" * 50)

    for state, probability in (
        result["Target Probabilities"].items()
    ):

        print(
            f"|{state}> : "
            f"{probability * 100:.2f}%"
        )

    print("\nCombined Marked-State Probability")
    print("-" * 50)

    print(
        f"{result['Combined Probability'] * 100:.2f}%"
    )

    print("\nExecution Time")
    print("-" * 50)

    print(
        f"{result['Execution Time']:.6f} seconds"
    )

    print("=" * 70)


# ============================================================
# TEST
# ============================================================

def main():

    N = 16

    marked_targets = [
        5,
        16
    ]

    result = run_multi_target(
        N,
        marked_targets,
        shots=1024
    )

    display_result(
        result
    )

    print("\nQuantum Circuit")
    print("-" * 50)

    print(
        result["Circuit"].draw()
    )


if __name__ == "__main__":

    main()