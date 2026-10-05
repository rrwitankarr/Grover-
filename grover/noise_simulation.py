
import math
import time

from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from grover.single_target import (
    validate_search_space,
    calculate_qubits,
    calculate_iterations,
    create_grover_circuit,
)


def create_noise_model(noise_level):
    """Create a depolarizing noise model for one- and two-qubit gates."""

    if not 0.0 <= noise_level <= 1.0:
        raise ValueError("Noise level must be between 0 and 1.")

    noise_model = NoiseModel()

    # Apply the selected error probability to single-qubit gates.
    single_qubit_error = depolarizing_error(noise_level, 1)

    # Apply the selected error probability to two-qubit gates.
    two_qubit_error = depolarizing_error(noise_level, 2)

    noise_model.add_all_qubit_quantum_error(
        single_qubit_error, ["u"]
    )
    noise_model.add_all_qubit_quantum_error(
        two_qubit_error, ["cx"]
    )

    return noise_model


def run_noisy_grover(n, target, shots=1024, noise_level=0.001):
    """Run Grover's algorithm using a configurable noise model."""

    if not validate_search_space(n):
        raise ValueError("N must be a power of 2 and at least 2.")

    if n > 512:
        raise ValueError("The maximum supported search space is 512.")

    if not 1 <= target <= n:
        raise ValueError(f"Target must be between 1 and {n}.")

    if shots < 1:
        raise ValueError("Shots must be at least 1.")

    if not 0.0 <= noise_level <= 1.0:
        raise ValueError("Noise level must be between 0 and 1.")

    # Reuse the existing, dynamically generated Grover circuit.
    circuit, target_state, iterations = create_grover_circuit(
        n, target
    )

    noise_model = create_noise_model(noise_level)

    simulator = AerSimulator(noise_model=noise_model)

    # Compile the circuit into gates supported by our noise model.
    start_transpile = time.perf_counter()

    compiled_circuit = transpile(
        circuit,
        basis_gates=noise_model.basis_gates,
    )

    transpilation_time = time.perf_counter() - start_transpile

    # Execute the circuit with the selected noise model.
    start_execution = time.perf_counter()

    result = simulator.run(
        compiled_circuit,
        shots=shots,
    ).result()

    execution_time = time.perf_counter() - start_execution

    counts = result.get_counts()

    target_count = counts.get(target_state, 0)
    target_probability = target_count / shots

    return {
        "N": n,
        "Qubits": calculate_qubits(n),
        "Target": target,
        "Target State": target_state,
        "Iterations": iterations,
        "Oracle Queries": iterations,
        "Depth": compiled_circuit.depth(),
        "Target Probability": target_probability,
        "Transpile Time": transpilation_time,
        "Execution Time": execution_time,
        "Counts": counts,
        "Circuit": circuit,
        "Shots": shots,
        "Environment": "Noisy Simulator",
        "Noise Level": noise_level,
    }