import time
import csv
import os

def linear_search(data, target):
    comparisons = 0

    for i in range(len(data)):
        comparisons += 1

        if data[i] == target:
            return i, comparisons

    return -1, comparisons

def save_classical_benchmark():

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

    print("\nRunning classical linear search benchmark...")
    print("Please wait...\n")

    for n in sizes:

        target = n

        # Create search space
        data = list(range(1, n + 1))

        start = time.perf_counter()

        index, comparisons = linear_search(
            data,
            target
        )

        end = time.perf_counter()

        execution_time = end - start

        results.append({
            "N": n,
            "Target": target,
            "Index": index,
            "Comparisons": comparisons,
            "Execution Time": execution_time
        })

        print(f"N = {n} completed")

    # --------------------------------------------------------
    # Display table
    # --------------------------------------------------------

    print("\n")
    print("=" * 75)
    print("CLASSICAL LINEAR SEARCH BENCHMARK")
    print("=" * 75)

    print(
        f"{'N':<10}"
        f"{'Target':<10}"
        f"{'Index':<10}"
        f"{'Comparisons':<15}"
        f"{'Time (s)':<15}"
    )

    print("-" * 75)

    for result in results:

        print(
            f"{result['N']:<10}"
            f"{result['Target']:<10}"
            f"{result['Index']:<10}"
            f"{result['Comparisons']:<15}"
            f"{result['Execution Time']:<15.8f}"
        )

    print("=" * 75)

    # --------------------------------------------------------
    # Save CSV
    # --------------------------------------------------------

    os.makedirs("results", exist_ok=True)

    filename = "results/classical_results.csv"

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "N",
            "Target",
            "Index",
            "Comparisons",
            "Execution Time"
        ])

        for result in results:

            writer.writerow([
                result["N"],
                result["Target"],
                result["Index"],
                result["Comparisons"],
                result["Execution Time"]
            ])

    print(
        f"\nBenchmark results saved to: {filename}"
    )

    return results

def display_detailed_result(n, target, index, comparisons, execution_time):
    print("\nSearch Result")
    print("-" * 35)
    print("Search space size (N):", n)
    print("Target:", target)
    print("Index:", index)
    print("Comparisons:", comparisons)
    print("Execution time:", execution_time, "seconds")


def display_table(results, title):
    print("\n" + title)
    print("-" * 70)
    print(
        f"{'N':<10}"
        f"{'Target':<15}"
        f"{'Index':<15}"
        f"{'Comparisons':<15}"
        f"{'Time (s)':<15}"
    )
    print("-" * 70)

    for result in results:
        print(
            f"{result['N']:<10}"
            f"{result['Target']:<15}"
            f"{result['Index']:<15}"
            f"{result['Comparisons']:<15}"
            f"{result['Time']:<15.10f}"
        )


def benchmark():
    sizes = [4, 8, 16, 32, 64, 128, 256, 512]

    results = []

    for n in sizes:

        # Search space: 1, 2, 3, ..., N
        data = list(range(1, n + 1))

        # Worst-case target
        target = n

        start = time.perf_counter()

        index, comparisons = linear_search(data, target)

        end = time.perf_counter()

        execution_time = end - start

        results.append({
            "N": n,
            "Target": target,
            "Index": index,
            "Comparisons": comparisons,
            "Time": execution_time
        })

    # --------------------------------------------------
    # TABLE FORMAT
    # --------------------------------------------------

    display_table(
        results,
        "CLASSICAL LINEAR SEARCH - BENCHMARK RESULTS"
    )

    # --------------------------------------------------
    # DETAILED FORMAT
    # --------------------------------------------------

    print("\n\nDETAILED BENCHMARK RESULTS")
    print("=" * 70)

    for result in results:
        display_detailed_result(
            result["N"],
            result["Target"],
            result["Index"],
            result["Comparisons"],
            result["Time"]
        )


def interactive_search():
    while True:

        try:
            n = int(input("\nEnter search space size N: "))

            if n <= 0:
                print("N must be greater than 0.")
                continue

            target = int(input(f"Enter target (1 to {n}): "))

            if target < 1 or target > n:
                print("Target must be between 1 and N.")
                continue

            break

        except ValueError:
            print("Please enter valid integer values.")

    # Search space: 1, 2, 3, ..., N
    data = list(range(1, n + 1))

    start = time.perf_counter()

    index, comparisons = linear_search(data, target)

    end = time.perf_counter()

    execution_time = end - start

    result = {
        "N": n,
        "Target": target,
        "Index": index,
        "Comparisons": comparisons,
        "Time": execution_time
    }

    # --------------------------------------------------
    # TABLE FORMAT
    # --------------------------------------------------

    display_table(
        [result],
        "CUSTOM SEARCH - TABLE RESULT"
    )

    # --------------------------------------------------
    # DETAILED FORMAT
    # --------------------------------------------------

    display_detailed_result(
        n,
        target,
        index,
        comparisons,
        execution_time
    )


def main():

    # ==================================================
    # STAGE 1: BENCHMARK
    # ==================================================

    benchmark()

    # ==================================================
    # CUSTOM SEARCH OPTION
    # ==================================================

    print("\n\n" + "=" * 70)
    choice = input(
        "Would you like to test the linear search with custom data? (y/n): "
    ).strip().lower()

    if choice == "y":
        interactive_search()
    else:
        print("\nProgram finished.")


if __name__ == "__main__":
    save_classical_benchmark()