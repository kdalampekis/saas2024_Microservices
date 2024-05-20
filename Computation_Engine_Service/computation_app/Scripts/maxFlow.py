import numpy as np
# from ortools.graph import pywrapgraph
import numpy as np

from ortools.graph.python import max_flow


def max_flow_solver(start_nodes, end_nodes, capacities, source, sink):
    """
    Compute the maximum flow between source and sink in a flow network.
    """
    # Instantiate a SimpleMaxFlow solver.
    smf = max_flow.SimpleMaxFlow()

    # Add arcs with capacities.
    all_arcs = smf.add_arcs_with_capacity(start_nodes, end_nodes, capacities)

    # Find the maximum flow between source and sink.
    status = smf.solve(source, sink)

    if status != smf.OPTIMAL:
        raise Exception(f"There was an issue with the max flow input. Status: {status}")

    # Collect the results
    result = {
        "max_flow": smf.optimal_flow(),
        "flows": [],
        "source_side_min_cut": smf.get_source_side_min_cut(),
        "sink_side_min_cut": smf.get_sink_side_min_cut(),
    }

    # Get the flow for each arc
#     solution_flows = smf.flows(all_arcs)
#     for arc, flow, capacity in zip(all_arcs, solution_flows, capacities):
#         result["flows"].append({
#             "arc": (smf.tail(arc), smf.head(arc)),
#             "flow": flow,
#             "capacity": capacity
#         })

    return result

# Define three parallel arrays: start_nodes, end_nodes, and the capacities
# between each pair. For instance, the arc from node 0 to node 1 has a
# capacity of 20.

# Example usage:



# start_nodes = np.array([0, 0, 0, 1, 1, 2, 2, 3, 3])
# end_nodes = np.array([1, 2, 3, 2, 4, 3, 4, 2, 4])
# capacities = np.array([20, 30, 10, 40, 30, 10, 20, 5, 20])
# source = 1
# sink = 4
#
# result = max_flow_solver(start_nodes, end_nodes, capacities, source, sink)
# print (result)





# print("Max flow:", result["max_flow"])
# print("")
# print(" Arc    Flow / Capacity")
# for arc_info in result["flows"]:
#     arc, flow, capacity = arc_info["arc"], arc_info["flow"], arc_info["capacity"]
#     print(f"{arc[0]} / {arc[1]}   {flow:3}  / {capacity:3}")
# print("Source side min-cut:", result["source_side_min_cut"])
# print("Sink side min-cut:", result["sink_side_min_cut"])

