def get_total_gates(experiment):

    circuit = experiment["Circuit"]

    return sum(
        circuit.count_ops().values()
    )


def get_gate_counts(experiment):

    circuit = experiment["Circuit"]

    return dict(
        circuit.count_ops()
    )


def get_shots(experiment):

    if "Shots" in experiment:
        return experiment["Shots"]

    counts = experiment.get("Counts", {})

    return sum(
        counts.values()
    )


def get_target_probability(
    experiment,
    state
):

    counts = experiment.get(
        "Counts",
        {}
    )

    shots = get_shots(experiment)

    if shots == 0:
        return 0

    return counts.get(
        state,
        0
    ) / shots

EXCLUDED_OPERATIONS = {"measure", "barrier"}


def get_computational_gate_counts(experiment):
    """Return computational gate counts, excluding measurement and barriers."""
    circuit = experiment.get("Circuit")

    if circuit is None:
        return {}

    operations = circuit.count_ops()

    return {
        str(gate): int(count)
        for gate, count in operations.items()
        if str(gate).lower() not in EXCLUDED_OPERATIONS
    }


def get_total_computational_gates(experiment):
    """Return the total number of computational gates."""
    return sum(get_computational_gate_counts(experiment).values())