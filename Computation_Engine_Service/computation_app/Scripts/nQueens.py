"""OR-Tools solution to the N-queens problem."""
import sys
from ortools.constraint_solver import pywrapcp

def solve_nqueens(board_size):
    solver = pywrapcp.Solver("n-queens")

    queens = [solver.IntVar(0, board_size - 1, f"x{i}") for i in range(board_size)]

    solver.Add(solver.AllDifferent(queens))
    solver.Add(solver.AllDifferent([queens[i] + i for i in range(board_size)]))
    solver.Add(solver.AllDifferent([queens[i] - i for i in range(board_size)]))

    db = solver.Phase(queens, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

    solutions = []
    solver.NewSearch(db)
    while solver.NextSolution():
        solution = []
        for i in range(board_size):
            row = ""
            for j in range(board_size):
                if queens[j].Value() == i:
                    row += "Q "
                else:
                    row += "_ "
            solution.append(row.strip())
        solutions.append(solution)
    solver.EndSearch()

    stats = {
        "failures": solver.Failures(),
        "branches": solver.Branches(),
        "wall_time": solver.WallTime(),
        "num_solutions": len(solutions)
    }

    return solutions, stats
