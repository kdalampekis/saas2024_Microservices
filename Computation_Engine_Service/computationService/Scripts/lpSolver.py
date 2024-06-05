from ortools.linear_solver import pywraplp

def lp_solver(constraints, objective_coeffs):
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return {"error": "Solver not created"}

    num_vars = len(objective_coeffs)
    variables = [solver.NumVar(0, solver.infinity(), f'x{i}') for i in range(num_vars)]

    for coeffs, bound in constraints:
        constraint = solver.Constraint(-solver.infinity(), bound)
        for i in range(num_vars):
            constraint.SetCoefficient(variables[i], coeffs[i])

    objective = solver.Objective()
    for i in range(num_vars):
        objective.SetCoefficient(variables[i], objective_coeffs[i])


    objective.SetMaximization()
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {}
        for i in range(num_vars):
            solution[f'x{i}'] = variables[i].solution_value()
        return {"status": "OPTIMAL", "objective_value": solver.Objective().Value(), "solution": solution}
    else:
        return {"status": "NOT_OPTIMAL", "message": "The problem does not have an optimal solution."}

# # Example usage
# constraints = [
#     ([1,5], 14),
#     ([3, -1], 0),
#     ([1, -1], 2)
# ]
# objective_coeffs = [8, 4]  # Example objective function: Maximize 3x + 4y
#
# # Call the function
# result = lp_solver(constraints, objective_coeffs)
# print(result)
