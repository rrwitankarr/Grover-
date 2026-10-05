import csv
import os


# ============================================================
# FILE PATHS
# ============================================================

CLASSICAL_FILE = "results/classical_results.csv"
GROVER_FILE = "results/grover_results.csv"
OUTPUT_FILE = "results/comparison_results.csv"


# ============================================================
# LOAD CSV
# ============================================================

def load_csv(filename):

    with open(
        filename,
        "r",
        newline=""
    ) as file:

        return list(
            csv.DictReader(file)
        )


# ============================================================
# CREATE COMPARISON
# ============================================================

def create_comparison():

    classical_results = load_csv(
        CLASSICAL_FILE
    )

    grover_results = load_csv(
        GROVER_FILE
    )

    # --------------------------------------------------------
    # Match results using N
    # --------------------------------------------------------

    grover_by_n = {
        int(row["N"]): row
        for row in grover_results
    }

    comparison = []

    for classical in classical_results:

        n = int(
            classical["N"]
        )

        grover = grover_by_n[n]

        comparison.append({

            "N": n,

            "Classical Comparisons": int(
                classical["Comparisons"]
            ),

            "Classical Time": float(
                classical["Execution Time"]
            ),

            "Grover Qubits": int(
                grover["Qubits"]
            ),

            "Grover Iterations": int(
                grover["Grover Iterations"]
            ),

            "Grover Oracle Queries": int(
                grover["Oracle Queries"]
            ),

            "Grover Circuit Depth": int(
                grover["Circuit Depth"]
            ),

            "Grover Target Probability": float(
                grover["Target Probability"]
            ),

            "Grover Time": float(
                grover["Execution Time"]
            )
        })

    # --------------------------------------------------------
    # Display table
    # --------------------------------------------------------

    print("\n")
    print("=" * 125)
    print("CLASSICAL SEARCH VS GROVER SEARCH")
    print("=" * 125)

    print(
        f"{'N':<8}"
        f"{'Classical':<15}"
        f"{'Grover':<15}"
        f"{'Qubits':<10}"
        f"{'Depth':<10}"
        f"{'Target Prob.':<15}"
        f"{'Classical Time':<18}"
        f"{'Grover Time':<15}"
    )

    print(
        f"{'':<8}"
        f"{'Comparisons':<15}"
        f"{'Oracle Queries':<15}"
    )

    print("-" * 125)

    for row in comparison:

        print(
            f"{row['N']:<8}"
            f"{row['Classical Comparisons']:<15}"
            f"{row['Grover Oracle Queries']:<15}"
            f"{row['Grover Qubits']:<10}"
            f"{row['Grover Circuit Depth']:<10}"
            f"{row['Grover Target Probability'] * 100:<15.2f}"
            f"{row['Classical Time']:<18.8f}"
            f"{row['Grover Time']:<15.8f}"
        )

    print("=" * 125)

    # --------------------------------------------------------
    # Save comparison CSV
    # --------------------------------------------------------

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
                "Classical Comparisons",
                "Classical Time",
                "Grover Qubits",
                "Grover Iterations",
                "Grover Oracle Queries",
                "Grover Circuit Depth",
                "Grover Target Probability",
                "Grover Time"
            ]
        )

        writer.writeheader()

        writer.writerows(
            comparison
        )

    print(
        f"\nComparison results saved to: "
        f"{OUTPUT_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    create_comparison()