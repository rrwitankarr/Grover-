import sys
import os
import csv

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(PROJECT_ROOT)

from grover.multi_target import run_multi_target

def validate_search_space(n):

    if n < 2:
        return False

    return (n & (n - 1)) == 0


def validate_targets(targets, n):

    if len(targets) == 0:
        return False

    # Targets must be within 1...N
    for target in targets:

        if target < 1 or target > n:
            return False

    # No duplicate targets
    if len(targets) != len(set(targets)):
        return False

    return True
# ============================================================
# MULTI-TARGET ANALYSIS
# ============================================================

def run_analysis():

    print("=" * 80)
    print("GROVER MULTI-TARGET ANALYSIS")
    print("=" * 80)

    # --------------------------------------------------------
    # TEST CASES
    # --------------------------------------------------------
    #
    # Format:
    # (Search Space N, [Marked Targets])
    #
    # Targets are user-facing values from 1 to N.
    # --------------------------------------------------------

    test_cases = [

        # N = 8
        (8, [2]),
        (8, [2, 5]),
        (8, [2, 5, 7]),

        # N = 16
        (16, [5]),
        (16, [5, 16]),
        (16, [2, 5, 9, 16]),

        # N = 32
        (32, [5, 16]),
        (32, [2, 7, 15, 25]),

        # N = 64
        (64, [10, 30]),
        (64, [5, 15, 25, 40, 55]),
    ]

    results = []

    # --------------------------------------------------------
    # RUN EXPERIMENTS
    # --------------------------------------------------------

    for n, targets in test_cases:

        print("\n" + "-" * 80)
        print(f"Running N = {n}")
        print(f"Targets = {targets}")
        print("-" * 80)

        result = run_multi_target(
            n=n,
            marked_targets=targets,
            shots=1024
        )

        results.append(result)

        # ----------------------------------------------------
        # DISPLAY RESULT
        # ----------------------------------------------------

        print(f"N                  : {result['N']}")
        print(f"Qubits              : {result['Qubits']}")
        print(f"Marked Targets      : {result['Marked Targets']}")
        print(f"Number of Targets M : {result['M']}")
        print(f"Grover Iterations   : {result['Iterations']}")
        print(f"Oracle Queries      : {result['Oracle Queries']}")
        print(f"Circuit Depth       : {result['Circuit Depth']}")

        print(
            f"Combined Probability: "
            f"{result['Combined Probability'] * 100:.2f}%"
        )

        print(
            f"Execution Time      : "
            f"{result['Execution Time']:.6f} seconds"
        )

        print("\nIndividual Target Probabilities:")

        for state, probability in result["Target Probabilities"].items():

            print(
                f"    |{state}> : "
                f"{probability * 100:.2f}%"
            )

    # --------------------------------------------------------
    # SUMMARY TABLE
    # --------------------------------------------------------

    print("\n\n")
    print("=" * 100)
    print("MULTI-TARGET GROVER SUMMARY")
    print("=" * 100)

    print(
        f"{'N':<8}"
        f"{'Qubits':<10}"
        f"{'M':<8}"
        f"{'Targets':<25}"
        f"{'Iterations':<12}"
        f"{'Depth':<10}"
        f"{'Probability':<15}"
    )

    print("-" * 100)

    for result in results:

        targets = str(result["Marked Targets"])

        print(
            f"{result['N']:<8}"
            f"{result['Qubits']:<10}"
            f"{result['M']:<8}"
            f"{targets:<25}"
            f"{result['Iterations']:<12}"
            f"{result['Circuit Depth']:<10}"
            f"{result['Combined Probability'] * 100:<15.2f}"
        )

    print("=" * 100)

    return results

def custom_search():

    print("\n")
    print("=" * 70)
    print("CUSTOM MULTI-TARGET GROVER SEARCH")
    print("=" * 70)

    # ========================================================
    # SEARCH SPACE
    # ========================================================

    while True:

        try:

            n = int(
                input("\nEnter search space size N: ")
            )

            if not validate_search_space(n):

                print(
                    "N must be a power of 2 and at least 2."
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

    # ========================================================
    # NUMBER OF TARGETS
    # ========================================================

    while True:

        try:

            m = int(
                input(
                    f"\nEnter number of target states M (1-{n}): "
                )
            )

            if m < 1 or m > n:

                print(
                    f"M must be between 1 and {n}."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter a valid integer."
            )

    # ========================================================
    # TARGET VALUES
    # ========================================================

    while True:

        try:

            target_input = input(
                f"\nEnter {m} target values "
                f"(1-{n}) separated by spaces: "
            )

            targets = [
                int(x)
                for x in target_input.split()
            ]

            if len(targets) != m:

                print(
                    f"Please enter exactly {m} targets."
                )

                continue

            if not validate_targets(targets, n):

                print(
                    "Targets must be unique and "
                    f"between 1 and {n}."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter valid integers."
            )

    # ========================================================
    # RUN GROVER
    # ========================================================

    print("\nRunning multi-target Grover...")

    result = run_multi_target(
        n=n,
        marked_targets=targets,
        shots=1024
    )

    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("MULTI-TARGET GROVER RESULT")
    print("=" * 70)

    print(
        f"Search Space (N)       : {result['N']}"
    )

    print(
        f"Number of Qubits       : {result['Qubits']}"
    )

    print(
        f"Marked Targets          : "
        f"{result['Marked Targets']}"
    )

    print(
        f"Number of Targets (M)  : {result['M']}"
    )

    print(
        f"Grover Iterations      : "
        f"{result['Iterations']}"
    )

    print(
        f"Oracle Queries         : "
        f"{result['Oracle Queries']}"
    )

    print(
        f"Circuit Depth          : "
        f"{result['Circuit Depth']}"
    )

    print(
        f"Combined Probability   : "
        f"{result['Combined Probability'] * 100:.2f}%"
    )

    print(
        f"Transpile Time         : "
        f"{result['Transpile Time']:.6f} seconds"
    )

    print(
        f"Execution Time         : "
        f"{result['Execution Time']:.6f} seconds"
    )

    # ========================================================
    # INDIVIDUAL TARGET PROBABILITIES
    # ========================================================

    print("\nIndividual Target Probabilities")
    print("-" * 50)

    for state, probability in (
        result["Target Probabilities"].items()
    ):

        print(
            f"|{state}> : "
            f"{probability * 100:.2f}%"
        )

    # ========================================================
    # MEASUREMENT RESULTS
    # ========================================================

    print("\nMeasurement Distribution")
    print("-" * 50)

    sorted_counts = sorted(
        result["Counts"].items(),
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

    # ========================================================
    # CIRCUIT
    # ========================================================

    if n <= 16:

        print("\nQuantum Circuit")
        print("-" * 50)

        print(
            result["Circuit"].draw()
        )

    else:

        print(
            f"\nQuantum circuit not displayed "
            f"for N = {n} because it is large."
        )
# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(results):

    results_directory = os.path.join(
        PROJECT_ROOT,
        "results"
    )

    os.makedirs(results_directory, exist_ok=True)

    filename = os.path.join(
        results_directory,
        "multi_target_results.csv"
    )

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "N",
            "Qubits",
            "Marked Targets",
            "M",
            "Iterations",
            "Oracle Queries",
            "Circuit Depth",
            "Combined Probability",
            "Transpile Time",
            "Execution Time"
        ])

        for result in results:

            writer.writerow([
                result["N"],
                result["Qubits"],
                str(result["Marked Targets"]),
                result["M"],
                result["Iterations"],
                result["Oracle Queries"],
                result["Circuit Depth"],
                result["Combined Probability"],
                result["Transpile Time"],
                result["Execution Time"]
            ])

    print(
        f"\nResults saved to:\n{filename}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("GROVER'S ALGORITHM - MULTI-TARGET ANALYSIS")
    print("=" * 70)

    # ========================================================
    # BENCHMARK
    # ========================================================

    print("\nStarting multi-target benchmark...")

    results = run_analysis()

    save_results(results)

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


if __name__ == "__main__":

    main()