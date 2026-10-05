
import time

from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import (
    QiskitRuntimeService,
    SamplerV2,
)

from grover.single_target import (
    validate_search_space,
    calculate_qubits,
    create_grover_circuit,
)


def run_ibm_grover(
    n,
    target,
    shots=1024,
    backend_name="ibm_fez",
):
    """Execute Grover's algorithm on IBM Quantum hardware."""

    # 1. Validate inputs
    if not validate_search_space(n) or n > 512:
        raise ValueError(
            "N must be a supported power of 2, up to 512."
        )

    if not 1 <= target <= n:
        raise ValueError(
            f"Target must be between 1 and {n}."
        )

    if shots < 1:
        raise ValueError("Shots must be positive.")

    if not backend_name:
        raise ValueError("Select an IBM Quantum backend.")

    # 2. Connect to the saved IBM Quantum account
    service = QiskitRuntimeService(
        instance="open-instance"
    )

    backend = service.backend(backend_name)

    # 3. Generate the circuit dynamically
    circuit, target_state, iterations = (
        create_grover_circuit(n, target)
    )

    # Sampler requires measured classical bits.
    if not circuit.clbits:
        circuit.measure_all()

    # 4. Transpile for the selected physical backend
    start_transpile = time.perf_counter()

    pass_manager = generate_preset_pass_manager(
        backend=backend,
        optimization_level=1,
    )

    isa_circuit = pass_manager.run(circuit)

    transpilation_time = (
        time.perf_counter() - start_transpile
    )

    # 5. Submit the real hardware job
    start_execution = time.perf_counter()

    sampler = SamplerV2(mode=backend)

    job = sampler.run(
        [isa_circuit],
        shots=shots,
    )

    runtime_result = job.result()

    execution_time = (
        time.perf_counter() - start_execution
    )

    # 6. Extract actual hardware measurement counts
    pub_result = runtime_result[0]
    counts = None

    for register in isa_circuit.cregs:
        register_data = getattr(
            pub_result.data,
            register.name,
            None,
        )

        if register_data is not None and hasattr(
            register_data, "get_counts"
        ):
            counts = register_data.get_counts()
            break

    if counts is None:
        raise RuntimeError(
            "IBM job completed, but measurement counts "
            "could not be extracted."
        )

    # 7. Calculate the target probability from real counts
    target_count = counts.get(target_state, 0)
    target_probability = target_count / shots

    # 8. Return the same result structure used by the dashboard
    return {
        "N": n,
        "Qubits": calculate_qubits(n),
        "Target": target,
        "Target State": target_state,
        "Iterations": iterations,
        "Oracle Queries": iterations,
        "Depth": isa_circuit.depth(),
        "Target Probability": target_probability,
        "Transpile Time": transpilation_time,
        "Execution Time": execution_time,
        "Counts": counts,
        "Circuit": isa_circuit,
        "Shots": shots,
        "Environment": "IBM Quantum Hardware",
        "Backend": backend.name,
        "Job ID": job.job_id(),
    }

