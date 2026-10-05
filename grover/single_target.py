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
    """
    Standard Grover implementation requires:

        N = 2^number_of_qubits
    """

    if n < 2:
        return False

    return (n & (n - 1)) == 0


# ============================================================
# NUMBER OF QUBITS
# ============================================================

def calculate_qubits(n):
    return int(math.log2(n))


# ============================================================
# NUMBER OF GROVER ITERATIONS
# ============================================================

def calculate_iterations(n):
    """
    Calculate the approximately optimal number of Grover
    iterations for one marked state.

    theta = asin(1 / sqrt(N))

    k ≈ pi / (4*theta) - 1/2
    """

    theta = math.asin(1 / math.sqrt(n))

    iterations = round(
        math.pi / (4 * theta) - 0.5
    )

    return max(1, iterations)


# ============================================================
# ORACLE
# ============================================================

def create_oracle(target_state):

    num_qubits = len(target_state)

    oracle = QuantumCircuit(num_qubits)

    # Convert target state into |111...1>
    #
    # Qiskit's qubit ordering is little-endian, therefore
    # target_state[num_qubits - 1 - qubit] is used.

    for qubit in range(num_qubits):

        if target_state[num_qubits - 1 - qubit] == "0":
            oracle.x(qubit)

    # Multi-controlled Z
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

    # Undo the X gates
    for qubit in range(num_qubits):

        if target_state[num_qubits - 1 - qubit] == "0":
            oracle.x(qubit)

    return oracle


# ============================================================
# DIFFUSER
# ============================================================

def create_diffuser(num_qubits):

    diffuser = QuantumCircuit(num_qubits)

    # H
    diffuser.h(range(num_qubits))

    # X
    diffuser.x(range(num_qubits))

    # Multi-controlled Z
    if num_qubits == 1:

        diffuser.z(0)

    elif num_qubits == 2:

        diffuser.cz(0, 1)

    else:

        diffuser.h(num_qubits - 1)

        diffuser.mcx(
            list(range(num_qubits - 1)),
            num_qubits - 1
        )

        diffuser.h(num_qubits - 1)

    # Undo X
    diffuser.x(range(num_qubits))

    # Undo H
    diffuser.h(range(num_qubits))

    return diffuser


# ============================================================
# CREATE GROVER CIRCUIT
# ============================================================
def create_grover_circuit(n, target, iterations=None):

    num_qubits = calculate_qubits(n)

    # Convert user-facing target 1...N to zero-based index
    target_index = target - 1

    # Convert to binary
    target_state = format(
        target_index,
        f"0{num_qubits}b"
    )

    # Calculate optimal iterations
    # Calculate optimal iterations unless a custom
    # iteration count was provided
    if iterations is None:
        iterations = calculate_iterations(n)

    circuit = QuantumCircuit(
        num_qubits,
        num_qubits
    )

    # --------------------------------------------------------
    # INITIAL SUPERPOSITION
    # --------------------------------------------------------

    circuit.h(range(num_qubits))

    # --------------------------------------------------------
    # GROVER ITERATIONS
    # --------------------------------------------------------

    for _ in range(iterations):

        oracle = create_oracle(target_state)

        circuit.compose(
            oracle,
            inplace=True
        )

        diffuser = create_diffuser(num_qubits)

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

    return circuit, target_state, iterations


# ============================================================
# RUN GROVER
# ============================================================

def run_grover(n, target, shots=1024):

    circuit, target_state, iterations = (
        create_grover_circuit(n, target)
    )

    simulator = AerSimulator()

    # --------------------------------------------------------
    # Transpile
    # --------------------------------------------------------

    start_transpile = time.perf_counter()

    compiled_circuit = transpile(
        circuit,
        simulator
    )

    end_transpile = time.perf_counter()

    transpilation_time = (
        end_transpile - start_transpile
    )

    # --------------------------------------------------------
    # Simulation
    # --------------------------------------------------------

    start_execution = time.perf_counter()

    result = simulator.run(
        compiled_circuit,
        shots=shots
    ).result()

    end_execution = time.perf_counter()

    execution_time = (
        end_execution - start_execution
    )

    counts = result.get_counts()

    # --------------------------------------------------------
    # Circuit depth
    # --------------------------------------------------------

    circuit_depth = compiled_circuit.depth()

    # --------------------------------------------------------
    # Target probability
    # --------------------------------------------------------

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
        "Oracle Queries": iterations,
        "Depth": circuit_depth,
        "Target Probability": target_probability,
        "Transpile Time": transpilation_time,
        "Execution Time": execution_time,
        "Counts": counts,
        "Circuit": circuit
    }


# ============================================================
# DISPLAY BENCHMARK TABLE
# ============================================================

def display_benchmark_table(results):

    print("\n")
    print("=" * 115)
    print("GROVER'S ALGORITHM - SINGLE TARGET BENCHMARK")
    print("=" * 115)

    print(
        f"{'N':<8}"
        f"{'Qubits':<10}"
        f"{'Target':<10}"
        f"{'Iterations':<13}"
        f"{'Oracle':<10}"
        f"{'Depth':<10}"
        f"{'Target Prob.':<15}"
        f"{'Time (s)':<12}"
    )

    print("-" * 115)

    for result in results:

        print(
            f"{result['N']:<8}"
            f"{result['Qubits']:<10}"
            f"{result['Target']:<10}"
            f"{result['Iterations']:<13}"
            f"{result['Oracle Queries']:<10}"
            f"{result['Depth']:<10}"
            f"{result['Target Probability'] * 100:<15.2f}"
            f"{result['Execution Time']:<12.6f}"
        )

    print("=" * 115)


# ============================================================
# DISPLAY DETAILED RESULT
# ============================================================

def display_detailed_result(result, show_measurements=True):

    print("\nGrover Search Result")
    print("-" * 55)

    print("Search space size (N):", result["N"])
    print("Number of qubits:", result["Qubits"])
    print("Target:", result["Target"])
    print(
        "Target quantum state: |"
        + result["Target State"]
        + ">"
    )
    print("Grover iterations:", result["Iterations"])
    print("Oracle queries:", result["Oracle Queries"])
    print("Transpiled circuit depth:", result["Depth"])
    print("Shots:", 1024)
    print(
        "Transpilation time:",
        f"{result['Transpile Time']:.6f}",
        "seconds"
    )
    print(
        "Execution time:",
        f"{result['Execution Time']:.6f}",
        "seconds"
    )

    # --------------------------------------------------------
    # Target probability
    # --------------------------------------------------------

    print("\nTarget Probability")
    print("-" * 55)

    print(
        f"|{result['Target State']}> : "
        f"{result['Target Probability'] * 100:.2f}%"
    )

    # --------------------------------------------------------
    # Measurement distribution
    # --------------------------------------------------------

    if show_measurements:

        print("\nMeasurement Distribution")
        print("-" * 55)

        counts = result["Counts"]

        sorted_counts = sorted(
            counts.items(),
            key=lambda item: item[1],
            reverse=True
        )

        for state, count in sorted_counts:

            probability = count / 1024

            print(
                f"|{state}> : "
                f"{count} shots "
                f"({probability * 100:.2f}%)"
            )

# ============================================================
# SAVE BENCHMARK RESULTS
# ============================================================

def save_benchmark_results(results):

    os.makedirs("results", exist_ok=True)

    filename = "results/grover_results.csv"

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "N",
            "Qubits",
            "Target",
            "Target State",
            "Grover Iterations",
            "Oracle Queries",
            "Circuit Depth",
            "Target Probability",
            "Transpile Time",
            "Execution Time"
        ])

        for result in results:

            writer.writerow([
                result["N"],
                result["Qubits"],
                result["Target"],
                result["Target State"],
                result["Iterations"],
                result["Oracle Queries"],
                result["Depth"],
                result["Target Probability"],
                result["Transpile Time"],
                result["Execution Time"]
            ])

    print(
        f"\nBenchmark results saved to: {filename}"
    )
# ============================================================
# BENCHMARK
# ============================================================

def benchmark():

    sizes = [
        4,
        8,
        16,
        32,
        64,
        128,
        256,
        512
    ]

    results = []

    print("\nRunning Grover benchmark...")
    print("Please wait as the larger circuits are simulated.")

    for n in sizes:

        print(
            f"\nRunning N = {n}..."
        )

        # Worst-case target
        target = n

        result = run_grover(
            n,
            target,
            shots=1024
        )

        results.append(result)

    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    display_benchmark_table(results)

    # --------------------------------------------------------
    # Detailed results
    # --------------------------------------------------------

    print("\n\n")
    print("=" * 70)
    print("DETAILED BENCHMARK RESULTS")
    print("=" * 70)

    for result in results:
        display_detailed_result(
            result,
            show_measurements=False
        )

    save_benchmark_results(results)
    return results


# ============================================================
# CUSTOM SEARCH
# ============================================================

def custom_search():

    print("\n")
    print("=" * 60)
    print("CUSTOM GROVER SEARCH")
    print("=" * 60)

    # --------------------------------------------------------
    # N
    # --------------------------------------------------------

    while True:

        try:

            n = int(
                input(
                    "\nEnter search space size N: "
                )
            )

            if not validate_search_space(n):

                print(
                    "N must be a power of 2 "
                    "and at least 2."
                )

                continue

            if n > 512:

                print(
                    "For this project, maximum N is 512."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter a valid integer."
            )

    # --------------------------------------------------------
    # Target
    # --------------------------------------------------------

    while True:

        try:

            target = int(
                input(
                    f"Enter target (1-{n}): "
                )
            )

            if 1 <= target <= n:
                break

            print(
                f"Target must be between 1 and {n}."
            )

        except ValueError:

            print(
                "Please enter a valid integer."
            )

    # --------------------------------------------------------
    # Run
    # --------------------------------------------------------

    result = run_grover(
        n,
        target,
        shots=1024
    )

    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    display_benchmark_table(
        [result]
    )

    # --------------------------------------------------------
    # Detailed result
    # --------------------------------------------------------

    display_detailed_result(
        result
    )

    # --------------------------------------------------------
    # Circuit
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Quantum Circuit
    # --------------------------------------------------------

    if n <= 16:

        print("\nQuantum Circuit")
        print("-" * 55)

        print(
            result["Circuit"].draw()
        )

    else:

        print("\nQuantum Circuit")
        print("-" * 55)

        print(
            f"Circuit not displayed for N = {n} "
            f"because the circuit is large."
        )

        print(
            f"Transpiled circuit depth: {result['Depth']}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 65)
    print("GROVER'S ALGORITHM - SINGLE TARGET")
    print("=" * 65)

    print("\nStarting Stage 2 benchmark...")

    # ========================================================
    # BENCHMARK
    # ========================================================

    benchmark()

    # ========================================================
    # CUSTOM SEARCH
    # ========================================================

    print("\n\n")
    print("=" * 70)

    choice = input(
        "Would you like to test Grover with custom data? (y/n): "
    ).strip().lower()

    if choice == "y":

        custom_search()

    else:

        print("\nProgram finished.")


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    main()