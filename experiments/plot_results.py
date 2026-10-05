import csv
import math
import os

import matplotlib.pyplot as plt


# ============================================================
# FILE PATH
# ============================================================

INPUT_FILE = "results/comparison_results.csv"

OUTPUT_DIR = "results/plots"


# ============================================================
# LOAD DATA
# ============================================================

def load_results():

    data = []

    with open(
        INPUT_FILE,
        "r",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            data.append({
                "N": int(row["N"]),
                "Classical Comparisons": int(
                    row["Classical Comparisons"]
                ),
                "Grover Oracle Queries": int(
                    row["Grover Oracle Queries"]
                ),
                "Grover Qubits": int(
                    row["Grover Qubits"]
                ),
                "Grover Circuit Depth": int(
                    row["Grover Circuit Depth"]
                ),
                "Grover Target Probability": float(
                    row["Grover Target Probability"]
                )
            })

    return data


# ============================================================
# GRAPH 1
# CLASSICAL VS GROVER SEARCH OPERATIONS
# ============================================================

def plot_search_operations(data):

    n = [
        row["N"]
        for row in data
    ]

    classical = [
        row["Classical Comparisons"]
        for row in data
    ]

    grover = [
        row["Grover Oracle Queries"]
        for row in data
    ]

    theoretical_grover = [
        (math.pi / 4) * math.sqrt(value)
        for value in n
    ]

    plt.figure(figsize=(10, 6))

    plt.plot(
        n,
        classical,
        marker="o",
        label="Classical Linear Search"
    )

    plt.plot(
        n,
        grover,
        marker="o",
        label="Grover Search"
    )

    plt.plot(
        n,
        theoretical_grover,
        linestyle="--",
        label="Theoretical Grover ≈ π/4√N"
    )

    plt.xlabel(
        "Search Space Size (N)"
    )

    plt.ylabel(
        "Search Operations"
    )

    plt.title(
        "Classical Linear Search vs Grover Search"
    )

    plt.xscale("log", base=2)

    plt.yscale("log")

    plt.xticks(n, n)

    plt.grid(
        True,
        which="both",
        linestyle=":"
    )

    plt.legend()

    plt.tight_layout()

    filename = (
        f"{OUTPUT_DIR}/"
        "classical_vs_grover_operations.png"
    )

    plt.savefig(
        filename,
        dpi=300
    )

    plt.show()

    print(
        f"Saved: {filename}"
    )


# ============================================================
# GRAPH 2
# CIRCUIT DEPTH
# ============================================================

def plot_circuit_depth(data):

    n = [
        row["N"]
        for row in data
    ]

    depth = [
        row["Grover Circuit Depth"]
        for row in data
    ]

    plt.figure(figsize=(10, 6))

    plt.plot(
        n,
        depth,
        marker="o"
    )

    plt.xlabel(
        "Search Space Size (N)"
    )

    plt.ylabel(
        "Transpiled Circuit Depth"
    )

    plt.title(
        "Grover Circuit Depth vs Search Space Size"
    )

    plt.xscale("log", base=2)

    plt.xticks(n, n)

    plt.grid(
        True,
        which="both",
        linestyle=":"
    )

    plt.tight_layout()

    filename = (
        f"{OUTPUT_DIR}/"
        "grover_circuit_depth.png"
    )

    plt.savefig(
        filename,
        dpi=300
    )

    plt.show()

    print(
        f"Saved: {filename}"
    )


# ============================================================
# GRAPH 3
# TARGET PROBABILITY
# ============================================================

def plot_target_probability(data):

    n = [
        row["N"]
        for row in data
    ]

    probability = [
        row["Grover Target Probability"] * 100
        for row in data
    ]

    plt.figure(figsize=(10, 6))

    plt.plot(
        n,
        probability,
        marker="o"
    )

    plt.axhline(
        90,
        linestyle="--",
        label="90% Reference"
    )

    plt.xlabel(
        "Search Space Size (N)"
    )

    plt.ylabel(
        "Target Probability (%)"
    )

    plt.title(
        "Grover Target-State Probability"
    )

    plt.xscale("log", base=2)

    plt.xticks(n, n)

    plt.ylim(
        0,
        105
    )

    plt.grid(
        True,
        which="both",
        linestyle=":"
    )

    plt.legend()

    plt.tight_layout()

    filename = (
        f"{OUTPUT_DIR}/"
        "grover_target_probability.png"
    )

    plt.savefig(
        filename,
        dpi=300
    )

    plt.show()

    print(
        f"Saved: {filename}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    data = load_results()

    print(
        f"Loaded {len(data)} benchmark results."
    )

    plot_search_operations(data)

    plot_circuit_depth(data)

    plot_target_probability(data)


if __name__ == "__main__":

    main()