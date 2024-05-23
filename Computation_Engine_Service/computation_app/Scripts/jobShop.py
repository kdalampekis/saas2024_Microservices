import collections
from ortools.sat.python import cp_model

def job_shop_solver(jobs_data):
    """Minimal jobshop problem."""
    # Data.
    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)
    # Computes horizon dynamically as the sum of all durations.
    horizon = sum(task[1] for job in jobs_data for task in job)

    # Create the model.
    model = cp_model.CpModel()

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple("task_type", "start end interval")
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple(
        "assigned_task_type", "start job index duration"
    )

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine, duration = task
            suffix = f"_{job_id}_{task_id}"
            start_var = model.NewIntVar(0, horizon, "start" + suffix)
            end_var = model.NewIntVar(0, horizon, "end" + suffix)
            interval_var = model.NewIntervalVar(
                start_var, duration, end_var, "interval" + suffix
            )
            all_tasks[job_id, task_id] = task_type(
                start=start_var, end=end_var, interval=interval_var
            )
            machine_to_intervals[machine].append(interval_var)

    # Create and add disjunctive constraints.
    for machine in all_machines:
        model.AddNoOverlap(machine_to_intervals[machine])

    # Precedences inside a job.
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(
                all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end
            )

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, "makespan")
    model.AddMaxEquality(
        obj_var,
        [all_tasks[job_id, len(job) - 1].end for job_id, job in enumerate(jobs_data)],
    )
    model.Minimize(obj_var)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    result = {
        "status": "No solution found.",
        "optimal_schedule_length": None,
        "assigned_jobs": {},
        "statistics": {
            "conflicts": solver.NumConflicts(),
            "branches": solver.NumBranches(),
            "wall_time": solver.WallTime()
        }
    }

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(
                        start=solver.Value(all_tasks[job_id, task_id].start),
                        job=job_id,
                        index=task_id,
                        duration=task[1],
                    )
                )

        result["status"] = "Optimal" if status == cp_model.OPTIMAL else "Feasible"
        result["optimal_schedule_length"] = solver.ObjectiveValue()

        for machine, tasks in assigned_jobs.items():
            tasks.sort()
            result["assigned_jobs"][machine] = [
                {
                    "job": task.job,
                    "task_index": task.index,
                    "start": task.start,
                    "duration": task.duration,
                }
                for task in tasks
            ]

    return result

# jobs_data = [  # task = (machine_id, processing_time).
#     [(0, 3), (1, 2), (2, 2)],  # Job0
#     [(0, 2), (2, 1), (1, 4)],  # Job1
#     [(1, 4), (2, 3)],  # Job2
#     [(1,2),(2,5)]
# ]
#
# results=job_shop_solver(jobs_data)
# print(results)

