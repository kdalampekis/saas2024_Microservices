from ortools.sat.python import cp_model

def bin_packing_solver(data):
    """
    Solves a bin packing problem.

    Parameters:
    - data (dict): A dictionary containing:
        - 'weights': List of weights for each item.
        - 'values': List of values for each item.
        - 'bin_capacity': Capacity of each bin.
        - 'num_bins': Number of bins available.

    Returns:
    - dict: A dictionary containing the solution if an optimal solution is found.
    - str: A message indicating no optimal solution if one is not found.
    """
    model = cp_model.CpModel()
    num_items = len(data["weights"])
    num_bins = data["num_bins"]

    # Variables
    x = {}
    for i in range(num_items):
        for b in range(num_bins):
            x[i, b] = model.NewBoolVar(f"x_{i}_{b}")

    # Constraints
    for i in range(num_items):
        model.Add(sum(x[i, b] for b in range(num_bins)) == 1)

    for b in range(num_bins):
        model.Add(
            sum(x[i, b] * data["weights"][i] for i in range(num_items)) <= data["bin_capacity"]
        )

    # Objective
    model.Maximize(
        sum(x[i, b] * data["values"][i] for i in range(num_items) for b in range(num_bins))
    )

    # Solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {
        "status": "No solution found.",
        "total_packed_value": None,
        "bins": [],
        "total_packed_weight": None
    }

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result["status"] = "Optimal" if status == cp_model.OPTIMAL else "Feasible"
        result["total_packed_value"] = solver.ObjectiveValue()

        total_weight = 0
        for b in range(num_bins):
            bin_weight = 0
            bin_value = 0
            bin_items = []

            for i in range(num_items):
                if solver.Value(x[i, b]) > 0:
                    item = {
                        "item_index": i,
                        "weight": data["weights"][i],
                        "value": data["values"][i]
                    }
                    bin_items.append(item)
                    bin_weight += data["weights"][i]
                    bin_value += data["values"][i]

            result["bins"].append({
                "bin_index": b,
                "bin_weight": bin_weight,
                "bin_value": bin_value,
                "items": bin_items
            })

            total_weight += bin_weight

        result["total_packed_weight"] = total_weight

    return result

# # Example usage
# data = {
#     "weights": [48, 30, 42, 36, 36, 27, 19, 42, 24, 30],
#     "values": [10, 40, 30, 50, 35, 40, 30, 20, 25, 15],
#     "bin_capacity": 100,
#     "num_bins": 5
# }
#
# result = bin_packing_solver(data)
# print(result)
