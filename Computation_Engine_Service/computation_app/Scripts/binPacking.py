from ortools.linear_solver import pywraplp

def bin_packing(weights, bin_capacity):
    """Solve the bin packing problem with the given weights and bin capacity."""
    
    # Create the data model.
    data = {}
    data["weights"] = weights
    data["items"] = list(range(len(weights)))
    data["bins"] = data["items"]
    data["bin_capacity"] = bin_capacity

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return {"error": "Solver not created"}

    # Variables
    x = {}
    for i in data["items"]:
        for j in data["bins"]:
            x[(i, j)] = solver.IntVar(0, 1, f"x_{i}_{j}")

    y = {}
    for j in data["bins"]:
        y[j] = solver.IntVar(0, 1, f"y[{j}]")

    # Constraints
    for i in data["items"]:
        solver.Add(sum(x[i, j] for j in data["bins"]) == 1)

    for j in data["bins"]:
        solver.Add(sum(x[(i, j)] * data["weights"][i] for i in data["items"]) <= y[j] * data["bin_capacity"])

    # Objective: minimize the number of bins used.
    solver.Minimize(solver.Sum(y[j] for j in data["bins"]))

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {"num_bins": 0, "bins": []}
        for j in data["bins"]:
            if y[j].solution_value() == 1:
                bin_items = []
                bin_weight = 0
                for i in data["items"]:
                    if x[i, j].solution_value() > 0:
                        bin_items.append(i)
                        bin_weight += data["weights"][i]
                if bin_items:
                    result["num_bins"] += 1
                    result["bins"].append({
                        "bin_number": j,
                        "items_packed": bin_items,
                        "total_weight": bin_weight
                    })
        result["time"] = solver.WallTime()
        return result
    else:
        return {"error": "The problem does not have an optimal solution."}

# # Example usage
# weights = [48, 30, 19, 36, 36, 27, 42, 42, 36, 24, 30]
# bin_capacity = 100
# result = bin_packing(weights, bin_capacity)
# print(result)
