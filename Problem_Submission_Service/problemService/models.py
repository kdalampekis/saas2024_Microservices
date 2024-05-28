from django.db import models

class SolverModel(models.Model):
    model_id = models.AutoField(primary_key=True, help_text="Unique identifier for the solver model")
    title = models.CharField(max_length=200, help_text="Title of the solver model")
    name = models.CharField(max_length=200, help_text="Name of the problem, as it is written in the url")
    notes = models.TextField(help_text="Notes about the solver model")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Solver Model"
        verbose_name_plural = "Solver Models"
        ordering = ['title']

class Metadata(models.Model):
    submission_id = models.AutoField(primary_key=True, help_text="Unique identifier for the submission")
    username = models.CharField(max_length=100, help_text="The username of the user involved in the problem")
    date = models.DateTimeField(auto_now_add=True, help_text="The date and time when the metadata was recorded")
    credit_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="The cost in credits for solving the problem")
    model_id = models.ForeignKey(SolverModel, on_delete=models.CASCADE, help_text="Reference to the Solver Model for problem type")
    is_executed = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.username} - {self.model_id.title} ({self.date.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Metadata"
        verbose_name_plural = "Metadata Records"
        ordering = ['-date']
