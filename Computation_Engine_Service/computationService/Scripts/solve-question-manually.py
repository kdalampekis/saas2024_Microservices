#!/usr/bin/env python3
import sys
import json
from ortools.linear_solver import pywraplp
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from ortools.graph import pywrapgraph
from ortools.sat.python import cp_model
from ortools.sat.python import CpSolverSolutionCallback
import math

def compute_distance_between_locations(location1, location2):
    x1, y1 = location1
    x2, y2 = location2

def print_solution(manager, routing, assignment):
    solution = {}
    for vehicle_id in range(manager.GetNumberOfVehicles()):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = assignment.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        solution[f'Route {vehicle_id + 1}'] = route
    return solution

def solve_problem(selected_tool, parameters):
    solver = None
    if selected_tool == 'Linear Programming (LP)':
        solver = pywraplp.Solver.CreateSolver('GLOP')
        
        objective_function_coefficients = parameters.get('Objective function coefficients')
        constraints = parameters.get('Constraints (coefficients and bounds)')

        num_vars = len(objective_function_coefficients)
        variables = [solver.NumVar(-solver.infinity(), solver.infinity(), f'x{i}') for i in range(num_vars)]

        objective = solver.Objective()
        for i in range(num_vars):
            objective.SetCoefficient(variables[i], objective_function_coefficients[i])
        objective.SetMinimization()

        for constraint_coeffs, bound in constraints:
            constraint = solver.Constraint(-solver.infinity(), bound)
            for i in range(num_vars):
                constraint.SetCoefficient(variables[i], constraint_coeffs[i])

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            solution = {}
            for i in range(num_vars):
                solution[f'x{i}'] = variables[i].solution_value()
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")
        
    elif selected_tool == 'Mixed Integer Programming (MIP)':
        solver = pywraplp.Solver.CreateSolver('SCIP')
        
        objective_function_coefficients = parameters.get('Objective function coefficients')
        constraints = parameters.get('Constraints (coefficients and bounds)')
        variable_types = parameters.get('Variable types (integer, binary, continuous)')
        
        num_vars = len(objective_function_coefficients)
        variables = [solver.NumVar(-solver.infinity(), solver.infinity(), f'x{i}') for i in range(num_vars)]

        for i, var_type in enumerate(variable_types):
            if var_type == 'integer':
                variables[i].SetInteger()
            elif var_type == 'binary':
                variables[i].SetInteger()
                variables[i].SetBounds(0, 1)
            elif var_type == 'continuous':
                pass  

        objective = solver.Objective()
        for i in range(num_vars):
            objective.SetCoefficient(variables[i], objective_function_coefficients[i])
        objective.SetMinimization()

        for constraint_coeffs, bound in constraints:
            constraint = solver.Constraint(-solver.infinity(), bound)
            for i in range(num_vars):
                constraint.SetCoefficient(variables[i], constraint_coeffs[i])

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            solution = {}
            for i in range(num_vars):
                solution[f'x{i}'] = variables[i].solution_value()
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Constraint Programming (CP)':
        solver = pywrapcp.Solver('CP_SOLVER')

        variables_with_domains = parameters.get('Variables with domains')
        constraints = parameters.get('Constraints')

        variables = {}
        for variable_name, domain in variables_with_domains.items():
            variables[variable_name] = solver.IntVar(domain[0], domain[1], variable_name)

        for constraint_expr in constraints:
            constraint = eval(constraint_expr)  
            solver.Add(constraint)

        db = solver.Phase(list(variables.values()), solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

        solution_collector = solver.AllSolutionCollector()
        solution_collector.Add(list(variables.values()))
        solution_collector.AddObjective(variables["objective_variable"])

        solver.Solve(db, [solution_collector])

        num_solutions = solution_collector.SolutionCount()
        solutions = []
        for i in range(num_solutions):
            solution = {}
            for variable_name, variable in variables.items():
                solution[variable_name] = solution_collector.Value(i, variable)
            solutions.append(solution)

        if num_solutions > 0:
            print("Solutions found:")
            for solution in solutions:
                print(solution)
        else:
            print("No solutions found.")

    elif selected_tool == 'Local Search':
        solver = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH

        initial_solution = parameters.get('Initial solution')
        neighborhood_structure = parameters.get('Neighborhood structure')
        objective_function = parameters.get('Objective function')

        num_locations = len(initial_solution)
        distance_matrix = [[0 for _ in range(num_locations)] for _ in range(num_locations)]

        for i in range(num_locations):
            for j in range(num_locations):
                distance_matrix[i][j] = compute_distance_between_locations(i, j)

        routing = pywrapcp.RoutingModel(num_locations, 1, 0)
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()

        def distance_callback(from_index, to_index):
            from_node = routing.IndexToNode(from_index)
            to_node = routing.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        initial_solution_callback = routing.ReadAssignmentFromString(initial_solution)
        routing.SetFirstSolutionStrategy(neighborhood_structure)
        initial_solution_callback.AddObjective(eval(objective_function))

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            print("Optimal solution found!")
            print("Total distance:", solution.ObjectiveValue())
            
            route = []
            index = routing.Start(0)
            while not routing.IsEnd(index):
                node = routing.IndexToNode(index)
                route.append(node)
                index = solution.Value(routing.NextVar(index))
            print("Route:", route)
        else:
            print("No solution found.")

    elif selected_tool == 'Vehicle Routing Problem (VRP)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demands = parameters.get('Customer demands')
        distance_matrix = parameters.get('Distance matrix')
        
        uniform_capacity = parameters.get('Uniform capacity')
        vehicle_capacities = [uniform_capacity] * num_vehicles

        manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot_location)

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return customer_demands[from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            [int(capacity) for capacity in vehicle_capacities],
            True,  # start cumul to zero
            'Capacity')

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            total_distance = 0
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                plan_output = f'Route for vehicle {vehicle_id}:\n'
                route_distance = 0
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    plan_output += f' {node_index} -> '
                    previous_index = index
                    index = solution.Value(routing.NextVar(index))
                    route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
                node_index = manager.IndexToNode(index)
                plan_output += f'{node_index}\n'
                plan_output += f'Distance of route {vehicle_id}: {route_distance}m\n'
                print(plan_output)
                total_distance += route_distance
            print(f'Total Distance of all routes: {total_distance}m')
        else:
            print('No solution found')

    elif selected_tool == 'Job Shop Scheduling':
        solver = pywrapcp.Solver('jobshop')

        job_durations = parameters.get('Job durations')
        machine_constraints = parameters.get('Machine constraints')
        job_precedence_constraints = parameters.get('Job precedence constraints')

        num_jobs = len(job_durations)
        num_machines = len(machine_constraints)
        all_tasks = []

        for i in range(num_jobs):
            for j in range(len(job_durations[i])):
                start_var = solver.FixedDurationIntervalVar(0, solver.infinity(), job_durations[i][j], False, f'Task_{i}_{j}')
                all_tasks.append(start_var)

        for i in range(num_machines):
            machine = machine_constraints[i]
            machine_intervals = []
            for job_index, task_index in machine:
                machine_intervals.append(all_tasks[job_index * len(machine[0]) + task_index])
            solver.AddNoOverlap(machine_intervals)

        for precedence_constraint in job_precedence_constraints:
            before_task, after_task = precedence_constraint
            solver.Add(all_tasks[before_task[0] * len(machine[0]) + before_task[1]].EndExpr() <=
                    all_tasks[after_task[0] * len(machine[0]) + after_task[1]].StartExpr())

        objective = solver.Max([all_tasks[job_index * len(machine[0]) + len(machine[0]) - 1].EndExpr()
                                for job_index in range(num_jobs)])

        objective_monitor = solver.Minimize(objective, 1)

        sequence_phase = solver.Phase([all_tasks[job_index * len(machine[0]) + task_index]
                                    for job_index in range(num_jobs)
                                    for task_index in range(len(machine[0]))],
                                    solver.SEQUENCE_DEFAULT)

        collector = solver.LastSolutionCollector()
        collector.AddObjective(objective)
        for task in all_tasks:
            collector.Add(task)

        solver.Solve(solver.Phase([objective_monitor, sequence_phase]), [collector])

        if collector.SolutionCount() > 0:
            solution = {}
            solution["Makespan"] = collector.ObjectiveValue(0)
            for job_index in range(num_jobs):
                for task_index in range(len(machine[0])):
                    solution[f'Job_{job_index}_Task_{task_index}'] = {
                        "Start time": collector.StartValue(0, all_tasks[job_index * len(machine[0]) + task_index]),
                        "End time": collector.EndValue(0, all_tasks[job_index * len(machine[0]) + task_index])
                    }
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("No feasible solution found.")

    elif selected_tool == 'Network Flows':
        solver = pywrapgraph.SimpleMaxFlow()
        
        arc_capacities = parameters.get('Arc capacities')
        node_supplies_demands = parameters.get('Node supplies/demands')
        flow_variables = parameters.get('Flow variables')
        
        num_nodes = len(node_supplies_demands)
        num_arcs = len(arc_capacities)

        for supply_demand in node_supplies_demands:
            supply = supply_demand[0]  # Supply or demand value
            solver.AddNode(supply)

        for i in range(num_arcs):
            start_node, end_node = flow_variables[i][0], flow_variables[i][1]  # Start and end nodes of the arc
            capacity = arc_capacities[i]  # Capacity of the arc
            solver.AddArcWithCapacity(start_node, end_node, capacity)

        for i in range(num_nodes):
            supply_demand = node_supplies_demands[i]
            supply = supply_demand[0]  # Supply or demand value
            solver.SetNodeSupply(i, supply)

        status = solver.Solve(0, num_nodes - 1)
        
        if status == pywrapgraph.SimpleMaxFlow.OPTIMAL:
            max_flow_value = solver.OptimalFlow()
            print("Optimal flow value:", max_flow_value)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Bin Packing':
        solver = pywrapcp.Solver('bin_packing')
        
        item_sizes = parameters.get('Item sizes')
        bin_capacities = parameters.get('Bin capacities')
        
        num_items = len(item_sizes)
        num_bins = len(bin_capacities)
        all_bins = list(range(num_bins))
        all_items = list(range(num_items))
        
        bins = [solver.IntVar(0, num_bins - 1, f'bin_{i}') for i in all_items]
        
        assignment = [[solver.BoolVar(f'x_{i}_{j}') for j in all_bins] for i in all_items]

        for i in all_items:
            solver.Add(sum(assignment[i]) == 1)  
        
        for j in all_bins:
            solver.Add(sum(assignment[i][j] * item_sizes[i] for i in all_items) <= bin_capacities[j])  

        objective = solver.Objective()
        for j in all_bins:
            for i in all_items:
                objective.SetCoefficient(assignment[i][j], 1)
        objective.SetMinimization()

        status = solver.Solve()

        if status == pywrapcp.Solver.OPTIMAL:
            solution = {}
            for i in all_items:
                bin_index = int(bins[i].solution_value())
                solution[f'Item_{i+1}'] = f'Bin_{bin_index+1}'
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Knapsack Problem':
        solver = pywrapcp.Solver('knapsack')
        
        item_weights = parameters.get('Item weights')
        item_values = parameters.get('Item values')
        knapsack_capacity = parameters.get('Knapsack capacity')
        
        num_items = len(item_weights)
        variables = [solver.IntVar(0, 1, f'x{i}') for i in range(num_items)]

        objective = solver.Sum([variables[i] * item_values[i] for i in range(num_items)])

        total_weight = solver.Sum([variables[i] * item_weights[i] for i in range(num_items)])
        constraint = solver.Constraint(0, knapsack_capacity)
        constraint.SetCoefficient(total_weight, 1)

        db = solver.Phase(variables, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

        monitor = solver.SearchLog(1000000, objective)

        solver.NewSearch(db, [objective, monitor])
        if solver.NextSolution():
            solution = {}
            total_value = 0
            for i in range(num_items):
                if variables[i].Value() == 1:
                    solution[f'x{i}'] = 1
                    total_value += item_values[i]
                else:
                    solution[f'x{i}'] = 0
            print("Optimal solution found!")
            print("Solution:", solution)
            print("Total value:", total_value)
        else:
            print("No feasible solution found.")

        solver.EndSearch()

    elif selected_tool == 'Linear Assignment Problem':
        solver = pywrapgraph.LinearSumAssignment()
        
        cost_matrix = parameters.get('Cost matrix')
        
        num_tasks = len(cost_matrix)
        num_resources = len(cost_matrix[0])

        for task in range(num_tasks):
            for resource in range(num_resources):
                solver.AddArcWithCost(task, resource, cost_matrix[task][resource])

        status = solver.Solve()

        if status == pywrapgraph.LinearSumAssignment.OPTIMAL:
            solution = {}
            for task in range(num_tasks):
                resource = solver.RightMate(task)
                solution[f'Task {task+1}'] = f'Resource {resource+1}'
            print("Optimal assignment found!")
            print("Assignment:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Traveling Salesman Problem (TSP)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        distance_matrix = parameters.get('Distance matrix')

        num_cities = len(distance_matrix)

        routing = pywrapcp.RoutingModel(num_cities, 1, 0)

        def distance_callback(from_index, to_index):
            from_node = routing.IndexToNode(from_index)
            to_node = routing.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            route = []
            index = routing.Start(0)
            while not routing.IsEnd(index):
                route.append(routing.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            route.append(routing.IndexToNode(index))

            print("Optimal TSP route:", route)
            print("Total distance:", solution.ObjectiveValue())
        else:
            print("No solution found for the TSP problem.")

    elif selected_tool == 'Vehicle Routing Problem with Time Windows (VRPTW)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
        
        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demands = parameters.get('Customer demands')
        time_windows = parameters.get('Time windows')
        distance_matrix = parameters.get('Distance matrix')

        manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot_location)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return customer_demands[from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            [int(demand) for demand in customer_demands],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')

        time_callback = lambda from_index, to_index: (time_windows[from_index][0], time_windows[from_index][1])
        time_callback_index = routing.RegisterTransitCallback(time_callback)
        routing.AddDimension(
            time_callback_index,
            int(1e9), 
            int(1e9),  
            False,  
            'Time')

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            print("Optimal solution found!")
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Vehicle Routing Problem with Pickup and Delivery (VRPPD)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        pickup_delivery_points = parameters.get('Pickup and delivery points')
        distances_between_points = parameters.get('Distances between points')

        routing = pywrapcp.RoutingModel(num_vehicles, 1, depot_location)

        def distance_callback(from_index, to_index):
            from_node = routing.IndexToNode(from_index)
            to_node = routing.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        for i in range(len(pickup_delivery_points)):
            pickup_index = pickup_delivery_points[i][0]
            delivery_index = pickup_delivery_points[i][1]
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            routing.solver().Add(routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
            routing.solver().Add(routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("No solution found.")

    elif selected_tool == 'Quadratic Assignment Problem (QAP)':
        solver = cp_model.CpSolver()

        flow_matrix = parameters.get('Flow matrix')
        distance_matrix = parameters.get('Distance matrix')

        num_facilities = len(flow_matrix)
        num_locations = len(distance_matrix)

        assignment = {}
        for i in range(num_facilities):
            for j in range(num_locations):
                assignment[(i, j)] = solver.IntVar(0, 1, f'assignment_{i}_{j}')

        objective = solver.Sum(
            flow_matrix[i][k] * distance_matrix[j][l] * assignment[(i, j)] * assignment[(k, l)]
            for i in range(num_facilities)
            for j in range(num_locations)
            for k in range(num_facilities)
            for l in range(num_locations)
        )
        solver.Minimize(objective)

        for i in range(num_facilities):
            solver.Add(solver.Sum(assignment[(i, j)] for j in range(num_locations)) == 1)
        for j in range(num_locations):
            solver.Add(solver.Sum(assignment[(i, j)] for i in range(num_facilities)) == 1)

        status = solver.Solve()

        if status == cp_model.OPTIMAL:
            solution = {}
            for i in range(num_facilities):
                for j in range(num_locations):
                    solution[f'assignment_{i}_{j}'] = solver.Value(assignment[(i, j)])
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")
        
    elif selected_tool == 'Maximum Flow':
        solver = pywrapgraph.SimpleMaxFlow()

        arc_capacities = parameters.get('Arc capacities')
        source_node = parameters.get('Source node')
        sink_node = parameters.get('Sink node')

        for i, capacity in enumerate(arc_capacities):
            solver.AddArcWithCapacity(source_node[i], sink_node[i], capacity)

        if solver.Solve(source_node, sink_node) == pywrapgraph.SimpleMaxFlow.OPTIMAL:
            solution = solver.OptimalFlow()
            print("Maximum Flow:", solution)
        else:
            print("There was an issue with finding the maximum flow.")

    elif selected_tool == 'Minimum Cost Flow':
        solver = pywrapgraph.SimpleMinCostFlow()

        arc_capacities = parameters.get('Arc capacities')
        arc_costs = parameters.get('Arc costs')
        source_node = parameters.get('Source node')
        sink_node = parameters.get('Sink node')

        for i in range(len(arc_capacities)):
            solver.AddArcWithCapacityAndUnitCost(
                source_node[i], sink_node[i], arc_capacities[i], arc_costs[i]
            )

        status = solver.Solve()

        if status == solver.OPTIMAL:
            solution = {}
            for i in range(solver.NumArcs()):
                solution[(solver.Tail(i), solver.Head(i))] = solver.Flow(i)
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Set Covering Problem':
        solver = pywrapcp.Solver('set_covering')

        set_elements = parameters.get('Set elements')
        subsets = parameters.get('Subsets')
        costs = parameters.get('Costs')

        num_subsets = len(subsets)
        selected = [solver.BoolVar(f'selected[{i}]') for i in range(num_subsets)]

        for element in set_elements:
            element_covered = solver.Sum([selected[i] for i, subset in enumerate(subsets) if element in subset]) >= 1
            solver.Add(element_covered)

        objective = solver.Sum([selected[i] * costs[i] for i in range(num_subsets)])

        objective_var = solver.Minimize(objective, 1)

        db = solver.Phase(selected, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

        collector = solver.LastSolutionCollector()
        collector.AddObjective(objective_var)
        collector.Add(selected)

        solver.Solve(db, [collector])

        solution = {}
        if collector.SolutionCount() > 0:
            solution['Total cost'] = collector.ObjectiveValue(0)
            for i in range(num_subsets):
                solution[f'Subset {i+1}'] = collector.Value(0, selected[i])
        else:
            print("No solution found!")

    elif selected_tool == 'Set Packing Problem':
        solver = pywrapcp.Solver('set_packing')
        # Define Set Packing Problem and solve
        set_elements = parameters.get('Set elements')
        subsets = parameters.get('Subsets')
        costs = parameters.get('Costs')
        # Use the set_elements, subsets, and costs to define the Set Packing Problem
    
    elif selected_tool == 'Set Partitioning Problem':
        solver = pywrapcp.Solver('set_partitioning')

        set_elements = parameters.get('Set elements')
        subsets = parameters.get('Subsets')
        costs = parameters.get('Costs')

        num_subsets = len(subsets)
        selected = [solver.BoolVar(f'selected_{i}') for i in range(num_subsets)]

        objective = solver.Objective()
        for i in range(num_subsets):
            objective.SetCoefficient(selected[i], costs[i])
        objective.SetMinimization()

        for element in set_elements:
            element_constraint = solver.Constraint(1, 1)  
            for i, subset in enumerate(subsets):
                if element in subset:
                    element_constraint.SetCoefficient(selected[i], 1)

        status = solver.Solve()

        if status == pywrapcp.Solver.OPTIMAL:
            solution = {}
            for i in range(num_subsets):
                if selected[i].solution_value() == 1:
                    solution[f'Subset {i+1}'] = subsets[i]
            print("Optimal solution found!")
            print("Selected subsets:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Graph Coloring':
        solver = pywrapcp.Solver('graph_coloring')

        graph_nodes = parameters.get('Graph nodes')
        adjacent_nodes = parameters.get('Adjacent nodes')
        colors = parameters.get('Colors')

        num_nodes = len(graph_nodes)
        num_colors = len(colors)
        node_colors = [solver.IntVar(0, num_colors - 1, f'color_{i}') for i in range(num_nodes)]

        for node, adj_nodes in adjacent_nodes.items():
            for adj_node in adj_nodes:
                solver.Add(node_colors[node] != node_colors[adj_node])

        objective = solver.Minimize(solver.Max(node_colors))

        decision_builder = solver.Phase(node_colors, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
        solver.NewSearch(decision_builder, [objective])
        if solver.NextSolution():
            solution = {graph_nodes[i]: colors[node_colors[i].Value()] for i in range(num_nodes)}
            print("Optimal solution found!")
            print("Node Colors:", solution)
        else:
            print("No solution found.")

    elif selected_tool == 'Graph Partitioning':
        solver = pywrapcp.Solver('graph_partitioning')

        graph_nodes = parameters.get('Graph nodes')
        adjacent_nodes = parameters.get('Adjacent nodes')

        num_nodes = len(graph_nodes)
        partition = [solver.IntVar(0, 1) for _ in range(num_nodes)]

        for node in range(num_nodes):
            adjacent_partition = [partition[adj_node] for adj_node in adjacent_nodes[node]]
            solver.Add(partition[node] == solver.Max(adjacent_partition) + 1)

        num_edges = 0
        for node in range(num_nodes):
            num_edges += len(adjacent_nodes[node]) * (1 - partition[node])
        objective = solver.Minimize(num_edges, 1)

        decision_builder = solver.Phase(partition, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
        solution_printer = CpSolverSolutionCallback()
        status = solver.Solve(decision_builder, [solution_printer, objective])

        if status == pywrapcp.Solver.OPTIMAL:
            solution = {}
            for node in range(num_nodes):
                solution[graph_nodes[node]] = solution_printer.Value(partition[node])
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Vehicle Routing Problem with Simultaneous Pickup and Delivery (VRPSPD)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        manager = pywrapcp.RoutingIndexManager(len(distances_between_points), num_vehicles, depot_location)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        for pickup, delivery in pickup_delivery_points:
            pickup_index = manager.NodeToIndex(pickup)
            delivery_index = manager.NodeToIndex(delivery)
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            routing.solver().Add(routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
            routing.solver().Add(routing.IsStart(pickup_index) == routing.IsStart(delivery_index))
            routing.solver().Add(routing.IsEnd(pickup_index) == routing.IsEnd(delivery_index))

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        solve = routing.SolveWithParameters(search_parameters)

        if solve:
            solution = []
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                route = [manager.IndexToNode(index)]
                while not routing.IsEnd(index):
                    index = solve.Value(routing.NextVar(index))
                    route.append(manager.IndexToNode(index))
                solution.append(route)
            print("Optimal solution found!")
            print("Routes:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Vehicle Routing Problem with Black Box (VRPB)':
        solver = pywrapcp.Solver('vrpb')

        black_box = parameters.get('Black box')
        solution = black_box.solve()

    elif selected_tool == 'Vehicle Routing Problem with Split Deliveries (VRPSD)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demands = parameters.get('Customer demands')
        distances_between_points = parameters.get('Distances between points')

        manager = pywrapcp.RoutingIndexManager(len(distances_between_points), num_vehicles, depot_location)

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return customer_demands[from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  
            [int(demand) for demand in customer_demands],  
            True,  
            'Capacity')

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        solutions = routing.SolveWithParameters(search_parameters)

        solution = {}
        if solutions:
            total_distance = 0
            routes = []
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                route = []
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route.append(node_index)
                    previous_index = index
                    index = solutions.Value(routing.NextVar(index))
                    total_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
                routes.append(route)
            solution['routes'] = routes
            solution['total_distance'] = total_distance
            print("Optimal solution found!")
            print("Routes:", routes)
            print("Total distance:", total_distance)
        else:
            print("No solution found.")

    elif selected_tool == 'Vehicle Routing Problem with Heterogeneous Fleet (VRPHF)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demands = parameters.get('Customer demands')
        distances_between_points = parameters.get('Distances between points')

        manager = pywrapcp.RoutingIndexManager(len(distances_between_points), num_vehicles, depot_location)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        capacities = [100, 200, 300]  
        for i in range(num_vehicles):
            routing.AddDimensionWithVehicleCapacity(
                transit_callback_index,
                customer_demands[i],  
                capacities[i],      
                True,
                f'Capacity_{i}'
            )

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            routes = []
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                route = []
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route.append(node_index)
                    index = solution.Value(routing.NextVar(index))
                routes.append(route)
            print("Optimal routes found!")
            print("Routes:", routes)
        else:
            print("No solution found.")

    elif selected_tool == 'Vehicle Routing Problem with Multiple Time Windows (VRPMTW)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demands = parameters.get('Customer demands')
        time_windows = parameters.get('Time windows')
        distances_between_points = parameters.get('Distances between points')

        routing = pywrapcp.RoutingModel(num_vehicles, 1, depot_location)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]

        manager = routing.GetCVRPTimeDimension(0)
        routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)

        for i, time_window in enumerate(time_windows):
            index = manager.NodeToIndex(i)
            manager.CumulVar(index).SetRange(time_window[0], time_window[1])

        for i, demand in enumerate(customer_demands):
            index = manager.NodeToIndex(i)
            routing.AddDemand(index, demand)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            print("Optimal solution found!")
            total_distance = solution.ObjectiveValue()
            route = []
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                while not routing.IsEnd(index):
                    route.append(manager.IndexToNode(index))
                    index = solution.Value(routing.NextVar(index))
                route.append(manager.IndexToNode(index))
            print("Solution:", route)
        else:
            print("No solution found.")

    elif selected_tool == 'Vehicle Routing Problem with Stochastic Demand (VRPSD)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
        
        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demand_distribution = parameters.get('Customer demand distribution')
        distances_between_points = parameters.get('Distances between points')
        
        total_demand = sum(customer_demand_distribution)
        
        vehicle_capacity = total_demand
        
        manager = pywrapcp.RoutingIndexManager(len(distances_between_points), num_vehicles, depot_location)
        routing = pywrapcp.RoutingModel(manager)
        
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]
        
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        demands = [0] + customer_demand_distribution 
        
        demand_callback_index = routing.RegisterUnaryTransitCallback(lambda index: demands[manager.IndexToNode(index)])
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index, 
            0, 
            [vehicle_capacity] * num_vehicles, 
            True, 
            'Capacity'
        )
        
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver
        
        solution = routing.SolveWithParameters(search_parameters)
        
        if solution:
            total_distance = solution.ObjectiveValue()
            print("Total distance traveled:", total_distance)
            
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                route = []
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route.append(node_index)
                    index = solution.Value(routing.NextVar(index))
                print(f"Route for vehicle {vehicle_id}: {route}")
        else:
            print("No solution found.")

    elif selected_tool == 'Job Shop Scheduling with Time Windows (JSSP)':
        solver = pywrapcp.Solver('jssp')

        job_durations = parameters.get('Job durations')
        machine_constraints = parameters.get('Machine constraints')
        job_precedence_constraints = parameters.get('Job precedence constraints')
        time_windows = parameters.get('Time windows')

        num_machines = len(machine_constraints)
        num_jobs = len(job_durations)

        all_tasks = {}
        for i in range(num_jobs):
            for j in range(num_machines):
                all_tasks[(i, j)] = solver.FixedDurationIntervalVar(0, solver.infinity(), job_durations[i], False, f'Job_{i}_Machine_{j}')

        for before_job, after_job in job_precedence_constraints:
            for machine_id in range(num_machines):
                solver.Add(all_tasks[(before_job, machine_id)].EndExpr() <= all_tasks[(after_job, machine_id)].StartExpr())

        for machine_id, machine_constraint in enumerate(machine_constraints):
            machine_tasks = [all_tasks[(job_id, machine_id)] for job_id in range(num_jobs) if machine_constraint[job_id] == 1]
            solver.AddNoOverlap(machine_tasks)

        for job_id in range(num_jobs):
            start_var = all_tasks[(job_id, 0)].StartExpr()
            end_var = all_tasks[(job_id, num_machines - 1)].EndExpr()
            time_window_start, time_window_end = time_windows[job_id]
            solver.Add(start_var >= time_window_start)
            solver.Add(end_var <= time_window_end)

        obj_var = solver.Max([all_tasks[(num_jobs - 1, machine_id)].EndExpr() for machine_id in range(num_machines)])
        objective = solver.Minimize(obj_var, 1)

        decision_builder = solver.Phase([all_tasks[(i, j)].StartExpr() for i in range(num_jobs) for j in range(num_machines)], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
        collector = solver.LastSolutionCollector()
        collector.Add(all_tasks.values())
        collector.AddObjective(obj_var)
        solver.Solve(decision_builder, [objective, collector])

        if solver.Objective().Value() != solver.infinity():
            solution = {}
            for job_id in range(num_jobs):
                for machine_id in range(num_machines):
                    start_time = collector.StartValue(0, all_tasks[(job_id, machine_id)])
                    solution[f'Job_{job_id}_Machine_{machine_id}'] = start_time
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("No solution found.")

    elif selected_tool == 'Cumulative Scheduling Problem (CUMULATIVE)':
        solver = pywrapcp.Solver('cumulative')

        tasks = parameters.get('Tasks')
        resources = parameters.get('Resources')
        resource_capacities = parameters.get('Resource capacities')
        task_requirements = parameters.get('Task requirements')

        num_tasks = len(tasks)
        num_resources = len(resources)

        task_starts = [solver.FixedDurationIntervalVar(0, solver.infinity(), task['duration'], False, f'Task_{i}') for i, task in enumerate(tasks)]

        for j in range(num_resources):
            resource_usage = [task_requirements[i][j] for i in range(num_tasks)]
            solver.AddCumulative(task_starts, resource_usage, resource_capacities[j])

        search_parameters = pywrapcp.DefaultPhaseParameters()
        search_parameters.heuristic_period = 500
        search_parameters.log_search_progress = True
        decision_builder = solver.Phase(task_starts,
                                        solver.CHOOSE_FIRST_UNBOUND,
                                        solver.ASSIGN_MIN_VALUE)
        solver.NewSearch(decision_builder)

        solution = {}
        if solver.NextSolution():
            for i, task in enumerate(tasks):
                solution[f'Task_{i}'] = (task_starts[i].StartMin(), task_starts[i].EndMin())
            print("Solution found!")
            print("Solution:", solution)
        else:
            print("No solution found.")

        solver.EndSearch()

    elif selected_tool == 'Resource-Constrained Project Scheduling Problem (RCPSP)':
        solver = pywrapcp.Solver('rcpsp')

        tasks = parameters.get('Tasks')
        precedence_constraints = parameters.get('Precedence constraints')
        resource_capacities = parameters.get('Resource capacities')
        task_durations = parameters.get('Task durations')

        num_tasks = len(tasks)
        num_resources = len(resource_capacities)
        all_tasks = [solver.FixedDurationIntervalVar(0, task_durations[i], True, f'Task_{i}') for i in range(num_tasks)]

        for prec in precedence_constraints:
            before_task = all_tasks[prec[0]]
            after_task = all_tasks[prec[1]]
            solver.Add(before_task.EndExpr() <= after_task.StartExpr())

        for r in range(num_resources):
            resource_usage = [tasks[i][r+2] for i in range(num_tasks)]  
            solver.Add(solver.Cumulative([all_tasks[i] for i in range(num_tasks)], [resource_usage], resource_capacities[r]))

        objective = solver.Max([all_tasks[i].EndExpr() for i in range(num_tasks)])
        objective_monitor = solver.Minimize(objective, 1)

        db = solver.Phase([objective_monitor], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

        solver.NewSearch(db)
        if solver.NextSolution():
            solution = {f'Task_{i}': (all_tasks[i].StartMin(), all_tasks[i].EndMin()) for i in range(num_tasks)}
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("No solution found!")

        solver.EndSearch()

    elif selected_tool == 'Job Shop Scheduling with Alternative Routes (JSSPAR)':
        solver = pywrapcp.Solver('jsspar')

        job_durations = parameters.get('Job durations')
        machine_constraints = parameters.get('Machine constraints')
        job_precedence_constraints = parameters.get('Job precedence constraints')
        alternative_routes = parameters.get('Alternative routes')

        num_jobs = len(job_durations)
        num_machines = len(machine_constraints)

        all_tasks = {}
        for job_id in range(num_jobs):
            for route_id, route in enumerate(alternative_routes[job_id]):
                for task_id, machine_id in enumerate(route):
                    all_tasks[(job_id, route_id, task_id)] = solver.FixedDurationIntervalVar(0, job_durations[job_id], job_durations[job_id], False, f'Job_{job_id}_Route_{route_id}_Task_{task_id}')

        for job_id in range(num_jobs):
            for route_id in range(len(alternative_routes[job_id])):
                for task_id in range(len(alternative_routes[job_id][route_id]) - 1):
                    solver.Add(all_tasks[(job_id, route_id, task_id + 1)].StartsAfterEnd(all_tasks[(job_id, route_id, task_id)]))

        for machine_id in range(num_machines):
            machine_tasks = []
            for job_id in range(num_jobs):
                for route_id in range(len(alternative_routes[job_id])):
                    for task_id in range(len(alternative_routes[job_id][route_id])):
                        if alternative_routes[job_id][route_id][task_id] == machine_id:
                            machine_tasks.append(all_tasks[(job_id, route_id, task_id)])
            solver.AddNoOverlap(machine_tasks)

        obj_var = solver.Max([all_tasks[(job_id, route_id, len(alternative_routes[job_id][route_id]) - 1)].EndExpr() for job_id in range(num_jobs) for route_id in range(len(alternative_routes[job_id]))])
        objective = solver.Minimize(obj_var, 1)

        db = solver.Phase([obj_var], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
        solver.NewSearch(db, [objective])
        if solver.NextSolution():
            solution = {}
            for job_id in range(num_jobs):
                for route_id in range(len(alternative_routes[job_id])):
                    for task_id in range(len(alternative_routes[job_id][route_id])):
                        solution[f'Job_{job_id}_Route_{route_id}_Task_{task_id}'] = {
                            'Start': all_tasks[(job_id, route_id, task_id)].StartValue(),
                            'End': all_tasks[(job_id, route_id, task_id)].EndValue(),
                            'Machine': alternative_routes[job_id][route_id][task_id]
                        }
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("No solution found.")

    elif selected_tool == 'Linear and Mixed Integer Programming with Domain Specific Language (DIMACS)':
        solver = pywraplp.Solver.CreateSolver('GLPK_MIXED_INTEGER_PROGRAMMING')

        model_constraints = parameters.get('Model constraints')

        variables = {}  
        for var_name, var_bounds in model_constraints['variables'].items():
            variables[var_name] = solver.NumVar(var_bounds['lower_bound'], var_bounds['upper_bound'], var_name)

        objective = solver.Objective()
        for var_name, coefficient in model_constraints['objective_function'].items():
            objective.SetCoefficient(variables[var_name], coefficient)
        objective.SetMinimization()

        for constraint_name, constraint_data in model_constraints['constraints'].items():
            constraint_expr = solver.Constraint(constraint_data['lower_bound'], constraint_data['upper_bound'])
            for var_name, coefficient in constraint_data['coefficients'].items():
                constraint_expr.SetCoefficient(variables[var_name], coefficient)

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            solution = {}
            for var_name in variables:
                solution[var_name] = variables[var_name].solution_value()
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Quadratic Assignment Problem with Constraints (QAPC)':
        solver = cp_model.CpSolver()

        flow_matrix = parameters.get('Flow matrix')
        distance_matrix = parameters.get('Distance matrix')
        constraints = parameters.get('Constraints')

        num_facilities = len(flow_matrix)

        assignment = [solver.NewIntVar(0, num_facilities - 1, f'assignment_{i}') for i in range(num_facilities)]

        for constraint in constraints:
            facility1, facility2 = constraint[0], constraint[1]
            distance_constraint = constraint[2]  
            solver.Add(distance_matrix[assignment[facility1]][assignment[facility2]] <= distance_constraint)

        objective = solver.NewIntVar(0, sum(flow_matrix[i][j] * distance_matrix[assignment[i]][assignment[j]] for i in range(num_facilities) for j in range(num_facilities)), 'objective')

        for i in range(num_facilities):
            for j in range(num_facilities):
                solver.Add(flow_matrix[i][j] * distance_matrix[assignment[i]][assignment[j]] == 0)

        solver.Minimize(objective)

        status = solver.Solve()

        if status == cp_model.OPTIMAL:
            solution = [solver.Value(assignment[i]) for i in range(num_facilities)]
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Max-Cut Problem (MAXCUT)':
        solver = pywrapcp.Solver('max_cut')
        
        graph_nodes = parameters.get('Graph nodes')
        adjacent_nodes = parameters.get('Adjacent nodes')
        weights = parameters.get('Weights')
        
        num_nodes = len(graph_nodes)
        partition = [solver.IntVar(0, 1) for _ in range(num_nodes)]

        objective = solver.Sum(weights[i][j] * (partition[i] != partition[j]) for i in range(num_nodes) for j in adjacent_nodes[i])

        solver.Maximize(objective)

        status = solver.Solve()

        if status == pywrapcp.Solver.OPTIMAL:
            solution = {}
            for i in range(num_nodes):
                solution[graph_nodes[i]] = partition[i].solution_value()
            print("Optimal solution found!")
            print("Partition:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Quadratic Knapsack Problem (QKP)':
        solver = cp_model.CpSolver()
        
        item_sizes = parameters.get('Item sizes')
        item_values = parameters.get('Item values')
        item_weights = parameters.get('Item weights')
        quadratic_terms = parameters.get('Quadratic terms')
        knapsack_capacity = parameters.get('Knapsack capacity')
        
        num_items = len(item_sizes)

        items_selected = [solver.BoolVar(f'item_{i}') for i in range(num_items)]

        total_size = solver.ScalProd(items_selected, item_sizes)
        total_weight = solver.ScalProd(items_selected, item_weights)
        capacity_constraint = solver.Add(total_weight <= knapsack_capacity)

        total_value = solver.ScalProd(items_selected, item_values)
        quadratic_value = 0
        for i in range(num_items):
            for j in range(i + 1, num_items):
                quadratic_value += quadratic_terms[i][j] * items_selected[i] * items_selected[j]
        objective = solver.Maximize(total_value + quadratic_value)

        status = solver.Solve()

        if status == cp_model.OPTIMAL:
            solution = {}
            for i in range(num_items):
                if solver.Value(items_selected[i]) == 1:
                    solution[f'item_{i}'] = True
                else:
                    solution[f'item_{i}'] = False
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Knapsack Problem with Conflict Graph (KP)':
        solver = pywrapcp.Solver('knapsack')

        item_sizes = parameters.get('Item sizes')
        item_values = parameters.get('Item values')
        item_weights = parameters.get('Item weights')
        conflict_graph = parameters.get('Conflict graph')

        num_items = len(item_sizes)
        selected = [solver.IntVar(0, 1, f'item_{i}') for i in range(num_items)]

        total_weight = solver.Sum([selected[i] * item_weights[i] for i in range(num_items)])
        knapsack_capacity = sum(item_weights) // 2  
        solver.Add(total_weight <= knapsack_capacity)

        for i in range(num_items):
            for j in range(i + 1, num_items):
                if conflict_graph[i][j]:
                    solver.Add(selected[i] + selected[j] <= 1)  

        total_value = solver.Sum([selected[i] * item_values[i] for i in range(num_items)])
        objective = solver.Maximize(total_value, 1)

        decision_builder = solver.Phase(selected, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MAX_VALUE)
        collector = solver.LastSolutionCollector()
        collector.Add(selected)
        solver.Solve(decision_builder, [objective, collector])

        if solver.Solve():
            solution = {}
            for i in range(num_items):
                solution[f'item_{i}'] = collector.Value(0, selected[i])
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("No solution found.")

    elif selected_tool == 'Vehicle Routing Problem with Time Dependent Matrices (VRPTWM)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demands = parameters.get('Customer demands')
        time_dependent_distances = parameters.get('Time-dependent distances')

        manager = pywrapcp.RoutingIndexManager(len(time_dependent_distances), num_vehicles, depot_location)
        routing = pywrapcp.RoutingModel(manager)

        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return time_dependent_distances[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(time_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return customer_demands[from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, num_vehicles, True, 'Capacity')

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            print("Optimal solution found!")
        else:
            print("No solution found.")

    elif selected_tool == 'Scheduling Problems with Time Lags (SPTL)':
        solver = pywrapcp.Solver('sptl')

        tasks = parameters.get('Tasks')
        precedence_constraints = parameters.get('Precedence constraints')
        time_lags = parameters.get('Time lags')

        num_tasks = len(tasks)
        start_times = [solver.IntVar(0, solver.infinity(), f'start_time_{i}') for i in range(num_tasks)]
        end_times = [solver.IntVar(0, solver.infinity(), f'end_time_{i}') for i in range(num_tasks)]

        for constraint in precedence_constraints:
            predecessor, successor = constraint
            solver.Add(end_times[predecessor] <= start_times[successor])

        for lag_constraint in time_lags:
            predecessor, successor, lag = lag_constraint
            solver.Add(start_times[successor] >= end_times[predecessor] + lag)

        objective = solver.Minimize(solver.Max([end_times[i] for i in range(num_tasks)]))

        db = solver.Phase(start_times + end_times,
                        solver.CHOOSE_FIRST_UNBOUND,
                        solver.ASSIGN_MIN_VALUE)

        solution = solver.Assignment()

        collector = solver.FirstSolutionCollector(solution)
        solver.Solve(db, [collector])

        if collector.SolutionCount() > 0:
            solution_index = 0  # Assuming we want the first solution
            solver_solution = collector.Solution(solution_index)
            solution = {f'Task_{i}': (solver_solution[start_times[i]].Value(), solver_solution[end_times[i]].Value())
                        for i in range(num_tasks)}
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("No feasible solution found.")

    elif selected_tool == 'Generalized Assignment Problem (GAP)':
        solver = pywrapcp.Solver('gap')

        agents = parameters.get('Agents')
        tasks = parameters.get('Tasks')
        resource_constraints = parameters.get('Resource constraints')
        costs = parameters.get('Costs')

        num_agents = len(agents)
        num_tasks = len(tasks)

        assigned = [[solver.BoolVar(f'assigned_{i}_{j}') for j in range(num_tasks)] for i in range(num_agents)]

        for i in range(num_agents):
            solver.Add(sum(assigned[i][j] for j in range(num_tasks)) <= resource_constraints[i])

        objective = solver.Objective()
        for i in range(num_agents):
            for j in range(num_tasks):
                objective.SetCoefficient(assigned[i][j], costs[i][j])
        objective.SetMaximization()

        status = solver.Solve()

        if status == pywrapcp.Solver.OPTIMAL:
            solution = {}
            for i in range(num_agents):
                for j in range(num_tasks):
                    if assigned[i][j].solution_value() == 1:
                        solution[tasks[j]] = agents[i]
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Quadratic Assignment Problem with Sequence Constraints (QAPS)':
        solver = cp_model.CpSolver()

        flow_matrix = parameters.get('Flow matrix')
        distance_matrix = parameters.get('Distance matrix')
        sequence_constraints = parameters.get('Sequence constraints')

        num_facilities = len(flow_matrix)
        num_locations = len(distance_matrix)

        assignments = []
        for i in range(num_facilities):
            assignments.append([solver.IntVar(0, 1, f'x{i}_{j}') for j in range(num_locations)])

        objective = solver.Objective()
        for i in range(num_facilities):
            for j in range(num_locations):
                for k in range(num_facilities):
                    for l in range(num_locations):
                        objective.SetCoefficient(assignments[i][j], assignments[k][l], flow_matrix[i][k] * distance_matrix[j][l])

        objective.SetMinimization()

        for constraint in sequence_constraints:
            for i in range(num_locations - 1):
                solver.Add(assignments[constraint[i]][i] <= assignments[constraint[i + 1]][i + 1])

        status = solver.Solve()

        if status == cp_model.OPTIMAL:
            solution = {}
            for i in range(num_facilities):
                for j in range(num_locations):
                    if solver.Value(assignments[i][j]) == 1:
                        solution[f'Facility {i}'] = f'Location {j}'
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Vehicle Routing Problem with Simultaneous Pickup and Delivery and Time Windows (VRPSDPTW)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        pickup_delivery_points = parameters.get('Pickup and delivery points')
        time_windows = parameters.get('Time windows')
        distances_between_points = parameters.get('Distances between points')

        routing = pywrapcp.RoutingModel(num_vehicles, 1, depot_location)

        def distance_callback(from_index, to_index):
            # Return the distance between the two points
            return distances_between_points[from_index][to_index]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def time_callback(from_index, to_index):
            # Return the travel time between the two points
            return distances_between_points[from_index][to_index]

        time_callback_index = routing.RegisterTransitCallback(time_callback)

        routing.AddDimension(
            time_callback_index,
            100,  # Maximum transit time 
            100,  # Maximum waiting time 
            True,  
            'Time'
        )
        time_dimension = routing.GetDimensionOrDie('Time')

        for location_idx, time_window in enumerate(time_windows):
            index = routing.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

        assignment = routing.SolveWithParameters(pywrapcp.DefaultRoutingSearchParameters())

        if assignment:
            solution = {}
            for vehicle_idx in range(num_vehicles):
                index = routing.Start(vehicle_idx)
                route = []
                while not routing.IsEnd(index):
                    node_idx = routing.IndexToNode(index)
                    route.append(node_idx)
                    index = assignment.Value(routing.NextVar(index))
                solution[f'Vehicle {vehicle_idx + 1}'] = route
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Vehicle Routing Problem with Time Windows and Split Deliveries (VRPTWSD)':
        solver = pywrapcp.RoutingModel()

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demands = parameters.get('Customer demands')
        time_windows = parameters.get('Time windows')
        split_deliveries = parameters.get('Split deliveries')
        distances_between_points = parameters.get('Distances between points')

        locations = []
        for i in range(len(customer_demands)):
            locations.append((split_deliveries[i], time_windows[i][0], time_windows[i][1]))

        def distance_callback(from_index, to_index):
            from_node = locations[from_index]
            to_node = locations[to_index]
            return distances_between_points[from_node][to_node]

        transit_callback_index = solver.RegisterTransitCallback(distance_callback)

        solver.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        demand_callback_index = solver.RegisterUnaryTransitCallback(
            lambda index: customer_demands[index])
        solver.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  
            [int(demand) for demand in customer_demands],
            True,  
            'Capacity')
        for vehicle_id in range(num_vehicles):
            solver.AddVariableMinimizedByFinalizer(
                solver.CumulVar(solver.End(vehicle_id)))

        time_dimension = solver.GetDimensionOrDie('Time')
        for location_idx, time_window in enumerate(time_windows):
            time_dimension.CumulVar(location_idx).SetRange(time_window[0], time_window[1])

        depot_idx = locations.index(depot_location)
        for i in range(num_vehicles):
            solver.AddConstantDimension(1, sys.maxsize, True, 'Depot')

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

        solution = solver.SolveWithParameters(search_parameters)

        if solution:
            print("Optimal solution found!")
            total_distance = 0
            for vehicle_id in range(num_vehicles):
                index = solver.Start(vehicle_id)
                plan_output = f'Route for vehicle {vehicle_id}:\n'
                route_distance = 0
                while not solver.IsEnd(index):
                    node_index = solver.IndexToNode(index)
                    plan_output += f' {node_index} -> '
                    previous_index = index
                    index = solution.Value(solver.NextVar(index))
                    route_distance += solver.GetArcCostForVehicle(previous_index, index, vehicle_id)
                plan_output += f'{solver.IndexToNode(index)}\n'
                plan_output += f'Distance of the route: {route_distance}m\n'
                print(plan_output)
                total_distance += route_distance
            print(f'Total distance of all routes: {total_distance}m')
        else:
            print("No solution found.")

    elif selected_tool == 'Job Shop Scheduling with Time Windows and Alternative Routes (JSSPTAR)':
        solver = pywrapcp.Solver('jssptar')

        job_durations = parameters.get('Job durations')
        machine_constraints = parameters.get('Machine constraints')
        job_precedence_constraints = parameters.get('Job precedence constraints')
        time_windows = parameters.get('Time windows')
        alternative_routes = parameters.get('Alternative routes')

        num_jobs = len(job_durations)
        num_machines = len(machine_constraints)
        num_time_windows = len(time_windows)

        job_starts = [solver.IntVar(0, solver.infinity(), f'job_{i}_start') for i in range(num_jobs)]

        for machine_idx in range(num_machines):
            machine_constraint = machine_constraints[machine_idx]
            machine_tasks = [job_starts[job_idx] + job_durations[job_idx][machine_idx] for job_idx in range(num_jobs) if machine_idx in alternative_routes[job_idx]]
            solver.Add(solver.AllDifferent(machine_tasks))

        for precedence_constraint in job_precedence_constraints:
            job_before, job_after = precedence_constraint
            solver.Add(job_starts[job_before] + job_durations[job_before][machine_constraints[job_before].index(job_after)] <= job_starts[job_after])

        for job_idx in range(num_jobs):
            for window_idx in range(num_time_windows):
                solver.Add(time_windows[job_idx][window_idx][0] <= job_starts[job_idx] <= time_windows[job_idx][window_idx][1])

        obj_var = solver.Max(job_starts) + max([sum(durations) for durations in job_durations])
        objective = solver.Minimize(obj_var)

        solver.Solve()

        solution = {f'Job_{i}': job_starts[i].solution_value() for i in range(num_jobs)}

        print("Optimal solution found!")
        print("Solution:", solution)

    elif selected_tool == 'Vehicle Routing Problem with Time Windows and Split Deliveries and Time Windows (VRPTWSDPTW)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demands = parameters.get('Customer demands')
        time_windows = parameters.get('Time windows')
        split_deliveries = parameters.get('Split deliveries')
        split_delivery_time_windows = parameters.get('Split delivery time windows')
        distances_between_points = parameters.get('Distances between points')

        manager = pywrapcp.RoutingIndexManager(len(distances_between_points), num_vehicles, depot_location)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return (time_windows[to_node][0], time_windows[to_node][1])

        time_callback_index = routing.RegisterTransitCallback(time_callback)
        add_time_window = True  
        if add_time_window:
            routing.AddDimension(time_callback_index,  
                                30,  # maximum time per vehicle
                                30,  # time buffer
                                False,  # start cumul zero
                                'Time')
            time_dimension = routing.GetDimensionOrDie('Time')

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return customer_demands[from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  
            [int(capacity) for capacity in num_vehicles],  
            True,  
            'Capacity')

        add_split_delivery_constraints = True
        if add_split_delivery_constraints:
            for i in range(len(split_deliveries)):
                routing.AddPickupAndDelivery(manager.NodeToIndex(split_deliveries[i][0]),
                                            manager.NodeToIndex(split_deliveries[i][1]))
                routing.solver().Add(routing.VehicleVar(manager.NodeToIndex(split_deliveries[i][0])) ==
                                    routing.VehicleVar(manager.NodeToIndex(split_deliveries[i][1])))

                routing.AddPickupAndDeliveryConstraints(manager.NodeToIndex(split_deliveries[i][0]),
                                                        manager.NodeToIndex(split_deliveries[i][1]),
                                                        manager.NodeToIndex(split_deliveries[i][2]),
                                                        manager.NodeToIndex(split_deliveries[i][3]),
                                                        split_delivery_time_windows[i][0],
                                                        split_delivery_time_windows[i][1])

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        assignment = routing.SolveWithParameters(search_parameters)

        if assignment:
            total_distance = 0
            total_load = 0
            routes = []
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                route_distance = 0
                route_load = 0
                route = []
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route.append(node_index)
                    next_index = assignment.Value(routing.NextVar(index))
                    route_distance += routing.GetArcCostForVehicle(index, next_index, vehicle_id)
                    route_load += customer_demands[node_index]
                    index = next_index
                route.append(manager.IndexToNode(index))
                routes.append(route)
                total_distance += route_distance
                total_load += route_load

            solutions = {
                'routes': routes,
                'total_distance': total_distance,
                'total_load': total_load
            }

            return {'solutions': solutions}
        else:
            print("The problem does not have an optimal solution.")

    elif selected_tool == 'Vehicle Routing Problem with Time Windows and Simultaneous Pickup and Delivery (VRPTWSPD)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        pickup_delivery_points = parameters.get('Pickup and delivery points')
        time_windows = parameters.get('Time windows')
        distances_between_points = parameters.get('Distances between points')

        manager = pywrapcp.RoutingIndexManager(len(distances_between_points), num_vehicles, depot_location)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return time_windows[from_node][to_node]

        time_callback_index = routing.RegisterTransitCallback(time_callback)
        routing.AddDimension(
            time_callback_index,
            300,  # Maximum transit time
            300,  # Maximum time per vehicle
            False,  
            'Time')
        time_dimension = routing.GetDimensionOrDie('Time')

        for request in range(len(pickup_delivery_points)):
            pickup_index = manager.NodeToIndex(pickup_delivery_points[request][0])
            delivery_index = manager.NodeToIndex(pickup_delivery_points[request][1])
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            routing.solver().Add(
                routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
            routing.solver().Add(
                time_dimension.CumulVar(pickup_index) <= time_dimension.CumulVar(delivery_index))

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            routes = []
            for vehicle_id in range(num_vehicles):
                route = []
                index = routing.Start(vehicle_id)
                while not routing.IsEnd(index):
                    route.append(manager.IndexToNode(index))
                    index = solution.Value(routing.NextVar(index))
                routes.append(route)
            print("Optimal solution found!")
            print("Routes:", routes)
        else:
            print("No solution found.")

    elif selected_tool == 'Quadratic Assignment Problem with Quadratic Side Constraints (QAPQ)':
        solver = cp_model.CpSolver()
        
        flow_matrix = parameters.get('Flow matrix')
        distance_matrix = parameters.get('Distance matrix')
        quadratic_side_constraints = parameters.get('Quadratic side constraints')
        
        model = cp_model.CpModel()
        
        num_locations = len(flow_matrix)
        locations = range(num_locations)
        assignments = [[model.NewBoolVar(f'Assignment_{i}_{j}') for j in locations] for i in locations]
        
        objective_expr = sum(
            flow_matrix[i][j] * distance_matrix[p][q] * assignments[i][p] * assignments[j][q]
            for i in locations
            for j in locations
            for p in locations
            for q in locations
        )
        model.Maximize(objective_expr)
        
        for i in locations:
            for j in locations:
                if quadratic_side_constraints[i][j] != 0:
                    model.Add(
                        sum(assignments[i][p] * assignments[j][q] for p in locations for q in locations) == quadratic_side_constraints[i][j]
                    )
        
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL:
            solution = [[solver.Value(assignments[i][j]) for j in locations] for i in locations]
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("The problem does not have an optimal solution.")
    
    elif selected_tool == 'Vehicle Routing Problem with Interdependent Time Windows (VRPITW)':
        solver = pywrapcp.Solver('vrpitw')

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demands = parameters.get('Customer demands')
        interdependent_time_windows = parameters.get('Interdependent time windows')
        distances_between_points = parameters.get('Distances between points')

        num_locations = len(distances_between_points)
        distance_matrix = [[0] * num_locations for _ in range(num_locations)]
        for i in range(num_locations):
            for j in range(num_locations):
                distance_matrix[i][j] = distances_between_points[i][j]

        locations = list(range(1, num_locations)) 
        demands = [0] + customer_demands  

        time_windows = {}
        for location, tw in enumerate(interdependent_time_windows):
            time_windows[location] = (tw[0], tw[1])

        routing = pywrapcp.RoutingModel(num_locations, num_vehicles, depot_location)
        routing.SetArcCostEvaluatorOfAllVehicles(
            routing.RegisterTransitCallback(lambda i, j: distance_matrix[i][j])
        )

        def demand_callback(from_index):
            return demands[from_index]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index, 0, [100] * num_vehicles, True, 'Capacity'
        )

        time = 'Time'
        routing.AddDimension(
            routing.RegisterTransitCallback(lambda i, j: 1),
            30,  
            30,  
            True,
            time
        )

        time_dimension = routing.GetDimensionOrDie(time)
        for location_idx, time_window in time_windows.items():
            time_dimension.CumulVar(location_idx).SetRange(time_window[0], time_window[1])

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
        )

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            print("Optimal solution found!")
        else:
            print("No solution found.")

    elif selected_tool == 'Vehicle Routing Problem with Multiple Time Windows and Split Deliveries (VRPMTWSD)':
        solutions = []

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        customer_demands = parameters.get('Customer demands')
        multiple_time_windows = parameters.get('Multiple time windows')
        split_deliveries = parameters.get('Split deliveries')
        distances_between_points = parameters.get('Distances between points')

        manager = pywrapcp.RoutingIndexManager(len(distances_between_points), num_vehicles, depot_location)

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        time = 'Time'
        routing.AddDimension(
            transit_callback_index,
            30,  # Maximum transit time per vehicle
            30,  # Vehicle maximum time
            False,  
            time)

        for i in range(1, len(distances_between_points)):
            time_window = multiple_time_windows[i]  
            routing.AddToVisitWindow(
                manager.NodeToIndex(i),
                time_window[0],  
                time_window[1])  

        for i in range(num_vehicles):
            routing.AddVariableMinimizedByFinalizer(
                routing.CumulVar(routing.Start(i)))

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            for vehicle_id in range(num_vehicles):
                route = []
                index = routing.Start(vehicle_id)
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route.append(node_index)
                    index = solution.Value(routing.NextVar(index))
                solutions.append(route)
        else:
            print("No solution found.")

    elif selected_tool == 'Linear Programming with Column Generation (LPCG)':
        solver = pywraplp.Solver.CreateSolver('GLPK_LINEAR_PROGRAMMING')
        
        master_problem = parameters.get('Master problem')
        subproblem = parameters.get('Subproblem')

        master_solver = pywraplp.Solver.CreateSolver('GLPK_LINEAR_PROGRAMMING')
        num_vars_master = len(master_problem['Objective function coefficients'])
        master_vars = [master_solver.NumVar(0, solver.infinity(), f'x{i}') for i in range(num_vars_master)]
        master_objective = master_solver.Objective()
        for i in range(num_vars_master):
            master_objective.SetCoefficient(master_vars[i], master_problem['Objective function coefficients'][i])
        for constraint_coeffs, bound in master_problem['Constraints']:
            constraint = master_solver.Constraint(-solver.infinity(), bound)
            for i in range(num_vars_master):
                constraint.SetCoefficient(master_vars[i], constraint_coeffs[i])

        master_status = master_solver.Solve()

        if master_status != pywraplp.Solver.OPTIMAL:
            print("The master problem does not have an optimal solution.")
            solution = None
        else:
            solution = {}
            for i in range(num_vars_master):
                solution[f'x{i}'] = master_vars[i].solution_value()

    elif selected_tool == 'Vehicle Routing Problem with Simultaneous Pickup and Delivery and Time Windows (VRPSDPDTW)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        pickup_delivery_points = parameters.get('Pickup and delivery points')
        time_windows = parameters.get('Time windows')
        distances_between_points = parameters.get('Distances between points')

        routing = pywrapcp.RoutingModel(num_vehicles, 1, depot_location)

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            return distances_between_points[from_index][to_index]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        time = 'Time'
        routing.AddDimension(
            transit_callback_index,
            30,  # allow waiting time
            30,  # maximum time per vehicle
            False,  
            time)

        time_dimension = routing.GetDimensionOrDie(time)
        for location_idx, time_window in enumerate(time_windows):
            if location_idx == depot_location:
                continue
            index = routing.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

        assignment = routing.SolveWithParameters(pywrapcp.RoutingModel.DefaultSearchParameters())

        if assignment:
            solution = {}
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                plan_output = f'Route for vehicle {vehicle_id}:\n'
                route_distance = 0
                while not routing.IsEnd(index):
                    node_index = routing.IndexToNode(index)
                    plan_output += f' {node_index} -> '
                    previous_index = index
                    index = assignment.Value(routing.NextVar(index))
                    route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
                plan_output += f'{routing.IndexToNode(index)}\n'
                plan_output += f'Distance of the route: {route_distance}m\n'
                print(plan_output)
                solution[f'Route for vehicle {vehicle_id}'] = plan_output
            print("Solution found!")
        else:
            print("No solution found.")

    elif selected_tool == 'Vehicle Routing Problem with Time Windows and Simultaneous Pickup and Delivery and Time Windows (VRPTWSPDPTW)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        pickup_delivery_points = parameters.get('Pickup and delivery points')
        time_windows = parameters.get('Time windows')
        distances_between_points = parameters.get('Distances between points')

        manager = pywrapcp.RoutingIndexManager(len(distances_between_points), num_vehicles, depot_location)

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        time = 'Time'
        routing.AddDimension(
            transit_callback_index,
            30,  # allow waiting time
            30,  # maximum time per vehicle
            False,  
            time)
        time_dimension = routing.GetDimensionOrDie(time)

        for location_idx, time_window in enumerate(time_windows):
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

        routing.AddPickupAndDelivery(pickup_delivery_points)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = solver

        sol = routing.SolveWithParameters(search_parameters)

        if sol:
            solution = []
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                route = []
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route.append(node_index)
                    index = sol.Value(routing.NextVar(index))
                node_index = manager.IndexToNode(index)
                route.append(node_index)
                solution.append({'Vehicle': vehicle_id, 'Route': route})
            print("Optimal solution found!")
            print("Solution:", solution)
        else:
            print("No solution found.")
    
    elif selected_tool == 'Vehicle Routing Problem with Simultaneous Pickup and Delivery and Time Windows and Split Deliveries (VRPSDPTWSD)':
        solver = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        num_vehicles = parameters.get('Number of vehicles')
        depot_location = parameters.get('Depot location')
        pickup_delivery_points = parameters.get('Pickup and delivery points')
        time_windows = parameters.get('Time windows')
        split_deliveries = parameters.get('Split deliveries')
        distances_between_points = parameters.get('Distances between points')

        manager = pywrapcp.RoutingIndexManager(len(distances_between_points), num_vehicles, depot_location)

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distances_between_points[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return time_windows[from_node][0]  

        time_callback_index = routing.RegisterTransitCallback(time_callback)

        routing.AddDimension(
            time_callback_index,
            60 * 60 * 9,  # Maximum time per vehicle
            60 * 60 * 10,  # Maximum vehicle delay
            False,  
            'Time'
        )
        time_dimension = routing.GetDimensionOrDie('Time')

        for i in range(len(pickup_delivery_points)):
            pickup_index = manager.NodeToIndex(pickup_delivery_points[i][0])
            delivery_index = manager.NodeToIndex(pickup_delivery_points[i][1])
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            routing.solver().Add(
                routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index)
            )
            routing.solver().Add(
                time_dimension.CumulVar(pickup_index) <= time_dimension.CumulVar(delivery_index)
            )

        for node_index in range(1, manager.GetNumberOfNodes()):
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(node_index)
            )

        assignment = routing.SolveWithParameters(pywrapcp.RoutingModel.DefaultSearchParameters())

        solution = {}
        if assignment:
            solution['routes'] = print_solution(manager, routing, assignment)
        else:
            solution['status'] = 'No solution found'

    elif selected_tool == 'Vehicle Routing Problem with Simultaneous Pickup and Delivery and Time Windows and Split Deliveries and Time Windows (VRPSDPTWSDPTW)':
        routing = pywrapcp.RoutingModel()

        def distance_callback(from_index, to_index):
            return distances_between_points[from_index][to_index]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        depot_index = depot_location

        num_vehicles = num_vehicles

        pickup_delivery_tasks = [(pickup_delivery_points[i], pickup_delivery_points[i + 1], time_windows[i], time_windows[i + 1]) 
                                for i in range(0, len(pickup_delivery_points), 2)]

        split_delivery_tasks = [(split_deliveries[i], split_deliveries[i + 1], split_delivery_time_windows[i]) 
                                for i in range(0, len(split_deliveries), 2)]

        time = 'Time'
        routing.AddDimension(
            transit_callback_index,
            60,    # slack time
            3000,  # maximum time per vehicle
            True,  
            time
        )
        time_dimension = routing.GetDimensionOrDie(time)

        for i in range(num_vehicles):
            routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.Start(i)))
            routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            routes = []
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                route = []
                while not routing.IsEnd(index):
                    node_index = routing.IndexToNode(index)
                    route.append(node_index)
                    index = solution.Value(routing.NextVar(index))
                routes.append(route)

            print("Optimal solution found!")
            print("Routes:", routes)
        else:
            print("No solution found.")

    else:
        print(f"Error: Tool '{selected_tool}' is not supported.")

    # Return the solution
    return solution

data = json.loads(sys.stdin.read())
selected_tool = data.get('selected_tool')
parameters = data.get('parameters')

result = solve_problem(selected_tool, parameters)

print(result)
