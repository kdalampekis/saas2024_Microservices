import numpy as np
from ortools.graph.python import linear_sum_assignment


def lin_sum_assignment(costs):
    """Compute the optimal assignment for the given cost matrix using the Linear Sum Assignment problem.

    Args:
        costs (array-like): A 2D array representing the cost matrix.

    Returns:
        dict: A dictionary containing the total cost and the assignment of workers to tasks.
    """



    # Instantiate a SimpleLinearSumAssignment solver.
    assignment = linear_sum_assignment.SimpleLinearSumAssignment()

    # Transform the cost matrix into 3 parallel vectors (start_nodes, end_nodes, arc_costs).
    end_nodes_unraveled, start_nodes_unraveled = np.meshgrid(
        np.arange(costs.shape[1]), np.arange(costs.shape[0])
    )
    start_nodes = start_nodes_unraveled.ravel()
    end_nodes = end_nodes_unraveled.ravel()
    arc_costs = costs.ravel()

    # Add arcs with costs.
    assignment.add_arcs_with_cost(start_nodes, end_nodes, arc_costs)

    # Solve the assignment problem.
    status = assignment.solve()

    if status == assignment.OPTIMAL:
        result = {
            "total_cost": assignment.optimal_cost(),
            "assignments": []
        }
        for i in range(0, assignment.num_nodes()):
            result["assignments"].append({
                "worker": i,
                "task": assignment.right_mate(i),
                "cost": assignment.assignment_cost(i)
            })
        return result
    elif status == assignment.INFEASIBLE:
        raise Exception("No assignment is possible.")
    elif status == assignment.POSSIBLE_OVERFLOW:
        raise Exception("Some input costs are too large and may cause an integer overflow.")

# Example usage:
costs = np.array([
    [90, 76, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 105],
    [45, 110, 95, 115],
])

result = lin_sum_assignment(costs)

print(result)
# print(f"Total cost = {result['total_cost']}\n")
# for assignment in result['assignments']:
#     print(f"Worker {assignment['worker']} assigned to task {assignment['task']}."
#           + f"  Cost = {assignment['cost']}")
