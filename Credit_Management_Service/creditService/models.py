from django.db import models

# Create your models here.
class CreditTransaction(models.Model):
    user_id = models.BigIntegerField(help_text="The ID of the user from the authentication service")
    credits = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount of credits purchased")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The time the transaction was created")

    def __str__(self):
        return f"User {self.user_id} purchased {self.credits} credits"

    class Meta:
        verbose_name = "Credit Transaction"
        verbose_name_plural = "Credit Transactions"
        ordering = ['-created_at']  # Orders the transactions by creation time, newest first