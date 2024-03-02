from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category.name} - ${self.amount} on {self.date}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.category} - ${self.amount}"
    
class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_goals')
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Optional

    def __str__(self):
        return f"{self.name} - ${self.balance}"

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    
def calculate_total_savings(user):
    return Account.objects.filter(user=user).aggregate(total_savings=models.Sum('balance'))['total_savings'] or 0

def get_upcoming_bills(user):
    today = timezone.now().date()
    return Bill.objects.filter(user=user, paid=False, due_date__gte=today).order_by('due_date')

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    reminder_date = models.DateField()

    @classmethod
    def create_reminders(cls):
        today = timezone.now().date()
        upcoming_bills = Bill.objects.filter(due_date__gte=today)
        for bill in upcoming_bills:
            reminder_date = bill.due_date - timezone.timedelta(days=3)  # Example: Reminder 3 days before due date
            Reminder.objects.create(user=bill.user, bill=bill, reminder_date=reminder_date)