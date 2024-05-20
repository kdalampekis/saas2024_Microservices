from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CreditTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user associated with this transaction")
    credits = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount of credits purchased")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The time the transaction was created")

    def __str__(self):
        return f"User {self.user.username} purchased {self.credits} credits"

    class Meta:
        verbose_name = "Credit Transaction"
        verbose_name_plural = "Credit Transactions"
        ordering = ['-created_at']  # Orders the transactions by creation time, newest first



class UserCreditBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="The user associated with this balance")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="The current credit balance of the user")

    def __str__(self):
        return f"User {self.user.username} has a balance of {self.balance} credits"

    class Meta:
        verbose_name = "User Credit Balance"
        verbose_name_plural = "User Credit Balances"

