from django import forms
from .models import Bill, Expense, Budget, FinancialGoal, Account


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class FinancialGoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ['name', 'target_amount', 'current_amount', 'completion_date']
        widgets = {
            'completion_date': forms.DateInput(attrs={'type':'date'}),
        }
        
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance', 'interest_rate']  # Adjust fields as needed
        widgets = {
            'balance': forms.NumberInput(attrs={'step': '0.01'}),
            'interest_rate': forms.NumberInput(attrs={'step': '0.01'}),
        }
        
class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['name', 'amount', 'due_date', 'paid']
        widgets = {
            'due_date': forms.DateInput(attrs={'type':'date'}),
        }