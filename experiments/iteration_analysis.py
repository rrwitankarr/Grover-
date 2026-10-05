import os
import csv
import time

import matplotlib.pyplot as plt
from qiskit import transpile
from qiskit_aer import AerSimulator

from grover.single_target import (
    create_grover_circuit,
    calculate_qubits
)


# ============================================================
# CONFIGURATION
# ============================================================

N = 16
TARGET = 16
SHOTS = 1024

MAX_ITERATIONS = 12

OUTPUT_FILE = "results/iteration_analysis.csv"
PLOT_FILE = "results/plots/grover_iteration_analysis.png"


# ============================================================
# RUN GROVER WITH CUSTOM ITERATION COUNT
# ============================================================

def run_iteration_experiment(
    n,
    target,
    iterations,
    shots=1024
):

    circuit, target_state, _ = create_grover_circuit(
        n,
        target,
        iterations=iterations
    )

    simulator = AerSimulator()

    compiled_circuit = transpile(
        circuit,
        simulator
    )

    start = time.perf_counter()

    result = simulator.run(
        compiled_circuit,
        shots=shots
    ).result()

    end = time.perf_counter()

    execution_time = end - start

    counts = result.get_counts()

    target_count = counts.get(
        target_state,
        0
    )

    target_probability = (
        target_count / shots
    )

    return {
        "N": n,
        "Qubits": calculate_qubits(n),
        "Target": target,
        "Target State": target_state,
        "Iterations": iterations,
        "Target Probability": target_probability,
        "Circuit Depth": compiled_circuit.depth(),
        "Execution Time": execution_time
    }


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(results):

    print("\n")
    print("=" * 90)
    print("GROVER ITERATION ANALYSIS")
    print("=" * 90)

    print(
        f"Search space size (N): {N}"
    )

    print(
        f"Target: {TARGET}"
    )

    print(
        f"Shots per experiment: {SHOTS}"
    )

    print()

    print(
        f"{'Iterations':<15}"
        f"{'Target State':<18}"
        f"{'Target Prob.':<18}"
        f"{'Circuit Depth':<18}"
        f"{'Time (s)':<12}"
    )

    print("-" * 90)

    for result in results:

        print(
            f"{result['Iterations']:<15}"
            f"|{result['Target State']}>"
            f"{'':<10}"
            f"{result['Target Probability'] * 100:<18.2f}"
            f"{result['Circuit Depth']:<18}"
            f"{result['Execution Time']:<12.6f}"
        )

    print("=" * 90)


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(results):

    os.makedirs(
        "results",
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "N",
                "Qubits",
                "Target",
                "Target State",
                "Iterations",
                "Target Probability",
                "Circuit Depth",
                "Execution Time"
            ]
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    print(
        f"\nResults saved to: {OUTPUT_FILE}"
    )


# ============================================================
# PLOT
# ============================================================

def plot_results(results):

    os.makedirs(
        "results/plots",
        exist_ok=True
    )

    iterations = [
        result["Iterations"]
        for result in results
    ]

    probabilities = [
        result["Target Probability"] * 100
        for result in results
    ]

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        iterations,
        probabilities,
        marker="o"
    )

    plt.xlabel(
        "Number of Grover Iterations"
    )

    plt.ylabel(
        "Target-State Probability (%)"
    )

    plt.title(
        f"Grover Amplitude Amplification "
        f"(N={N}, Target={TARGET})"
    )

    plt.xticks(
        iterations
    )

    plt.ylim(
        0,
        105
    )

    plt.grid(
        True,
        linestyle=":"
    )

    plt.tight_layout()

    plt.savefig(
        PLOT_FILE,
        dpi=300
    )

    plt.show()

    print(
        f"Plot saved to: {PLOT_FILE}"
    )


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():

    print("=" * 70)
    print("GROVER ITERATION ANALYSIS")
    print("=" * 70)

    print(
        f"\nN = {N}"
    )

    print(
        f"Target = {TARGET}"
    )

    print(
        f"Testing iterations from 0 to "
        f"{MAX_ITERATIONS}"
    )

    results = []

    for iterations in range(
        MAX_ITERATIONS + 1
    ):

        print(
            f"Running {iterations} iteration(s)..."
        )

        result = run_iteration_experiment(
            N,
            TARGET,
            iterations,
            SHOTS
        )

        results.append(
            result
        )

    display_results(
        results
    )

    save_results(
        results
    )

    plot_results(
        results
    )


if __name__ == "__main__":

    main()