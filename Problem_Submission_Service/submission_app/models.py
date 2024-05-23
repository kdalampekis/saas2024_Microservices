from django.db import models

class SolverModel(models.Model):
    VRP_PROBLEM = "VRP"
    LP_PROBLEM = 'LP'
    N_QUEENS = 'NQ'
    BIN_PACKING = 'BP'
    SOLVING_MIP = 'MIP'

    SOLVER_CHOICES = [
        (VRP_PROBLEM, 'Vehicle Routing Problem'),
        (LP_PROBLEM, 'Linear Programming Problem'),
        (N_QUEENS, 'N Queens Problem'),
        (BIN_PACKING, 'Bin Packing Problem'),
        (SOLVING_MIP, 'Mixed-Integer Programming Problem'),
    ]

    model_id = models.AutoField(primary_key=True, help_text="Unique identifier for the solver model")
    title = models.CharField(max_length=100, choices=SOLVER_CHOICES, unique=True, help_text="Type of solver model")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes regarding the solver model")

    def __str__(self):
        solver_type = self.get_title_display()
        return f"{solver_type} - Model ID {self.model_id}"

    class Meta:
        verbose_name = "Solver Model"
        verbose_name_plural = "Solver Models"
        ordering = ['-model_id']

class Metadata(models.Model):
    submission_id = models.AutoField(primary_key=True, help_text="Unique identifier for the submission")
    username = models.CharField(max_length=100, help_text="The username of the user involved in the problem")
    date = models.DateTimeField(auto_now_add=True, help_text="The date and time when the metadata was recorded")
    credit_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="The cost in credits for solving the problem")
    problem_type = models.ForeignKey(SolverModel, on_delete=models.CASCADE, related_name='metadata_problem_type', help_text="Reference to the Solver Model for problem type")
    is_ready = models.BooleanField(default=False)
    is_executed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.problem_type.title} ({self.date.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Metadata"
        verbose_name_plural = "Metadata Records"
        ordering = ['-date']
