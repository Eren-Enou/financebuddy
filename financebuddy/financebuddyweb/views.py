from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic import UpdateView, DeleteView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Sum
from django.utils import timezone

from django.utils.decorators import method_decorator

from .models import Expense, Category, Budget, FinancialGoal, Expense, Account, Bill, calculate_total_savings, get_upcoming_bills, Account
from .forms import BillForm, ExpenseForm, BudgetForm, FinancialGoalForm, AccountForm  

def homepage_view(request):
    return render(request, 'financebuddyweb/homepage.html')

def logout_view(request):
    return render(request, 'financebuddyweb/homepage.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']  # Make sure your form includes an email field
        
        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("This username is already taken.", status=400)
        if User.objects.filter(email=email).exists():
            return HttpResponse("This email is already registered.", status=400)
        
        user = User.objects.create_user(username, email, password)
        login(request, user)  # Automatically log in the user after sign up
        return redirect(reverse('homepage'))  # Redirect to homepage or another appropriate view
        
    return render(request, 'financebuddyweb/signup.html')

def profile_view(request):
    return render(request, 'financebuddyweb/profile.html')

@login_required
def add_expense_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Set the user before saving
            expense.save()
            return redirect('expenses_list')
    else:
        form = ExpenseForm()
    return render(request, 'financebuddyweb/add_expense.html', {'form': form})

@login_required
def expenses_list_view(request):
    expenses = Expense.objects.filter(user=request.user)
    
    # Apply filters
    date_filter = request.GET.get('date', None)
    category_filter = request.GET.get('category', None)
    min_amount_filter = request.GET.get('min_amount', None)
    max_amount_filter = request.GET.get('max_amount', None)
    
    if date_filter:
        expenses = expenses.filter(date=date_filter)
    
    if category_filter:
        expenses = expenses.filter(category=category_filter)
    
    if min_amount_filter:
        expenses = expenses.filter(amount__gte=min_amount_filter)
    
    if max_amount_filter:
        expenses = expenses.filter(amount__lte=max_amount_filter)
    
    return render(request, 'expense_list.html', {'expenses': expenses})

@login_required
def expenses_summary_view(request):
    expenses_by_category = Expense.objects.filter(user=request.user).values('category__name').annotate(total=Sum('amount')).order_by('-total')
    return render(request, 'financebuddyweb/expenses_summary.html', {'expenses_by_category': expenses_by_category})

class ExpenseUpdateView(UpdateView):
    model = Expense
    fields = ['category', 'amount', 'date', 'description']
    template_name = 'financebuddyweb/edit_expense.html'
    success_url = reverse_lazy('expenses_list')  # Redirect to the expenses list after editing

class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'financebuddyweb/confirm_delete.html'
    success_url = reverse_lazy('expenses_list')  # Redirect to the expenses list after deleting
    
class CustomLogoutView(LogoutView):
    template_name = 'financebuddyweb/logout.html'
    
@method_decorator(login_required, name='dispatch')
class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    success_url = reverse_lazy('budget_list')  # Adjust as needed

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'financebuddyweb/budget_list.html', {'budgets': budgets})

class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'financebuddyweb/budget_edit.html'
    success_url = reverse_lazy('budget_list')
    
class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'financebuddyweb/budget_confirm_delete.html'
    success_url = reverse_lazy('budget_list')
    
class FinancialGoalCreateView(LoginRequiredMixin, CreateView):
    model = FinancialGoal
    form_class = FinancialGoalForm
    template_name = 'financebuddyweb/financial_goal_form.html'
    success_url = reverse_lazy('financial_goal_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FinancialGoalListView(ListView):
    model = FinancialGoal
    template_name = 'financebuddyweb/financial_goal_list.html'
    context_object_name = 'financial_goals'

    def get_queryset(self):
        """Return financial goals for the current user."""
        return FinancialGoal.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add progress percentages to the financial goals."""
        context = super().get_context_data(**kwargs)
        for goal in context['financial_goals']:
            goal.progress_percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
        return context
    
class FinancialGoalUpdateView(LoginRequiredMixin, UpdateView):
    model = FinancialGoal
    form_class = FinancialGoalForm
    template_name = 'financebuddyweb/financial_goal_form.html'
    success_url = reverse_lazy('financial_goal_list')
    
class FinancialGoalDeleteView(DeleteView):
    model = FinancialGoal
    template_name = 'financebuddyweb/financial_goal_confirm_delete.html'
    success_url = reverse_lazy('financial_goal_list')
    
@login_required
def dashboard_view(request):
    total_savings = calculate_total_savings(request.user)
    upcoming_bills = get_upcoming_bills(request.user)
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]
    financial_goals = FinancialGoal.objects.filter(user=request.user)
    accounts = Account.objects.filter(user=request.user)
    
    context = {
        'accounts': accounts,
        'total_savings': total_savings,
        'upcoming_bills': upcoming_bills,
        'recent_expenses': recent_expenses,
        'financial_goals': financial_goals,
    }
    
    return render(request, 'financebuddyweb/dashboard.html', context)

class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    success_url = reverse_lazy('dashboard')  # Adjust as necessary

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'financebuddyweb/account_form.html'
    success_url = reverse_lazy('dashboard')  # Adjust as necessary

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class BillListView(ListView):
    model = Bill
    context_object_name = 'bills'

    def get_queryset(self):
        return Bill.objects.filter(user=self.request.user)

class BillCreateView(CreateView):
    model = Bill
    form_class = BillForm
    success_url = reverse_lazy('bill_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BillUpdateView(UpdateView):
    model = Bill
    form_class = BillForm
    success_url = reverse_lazy('bill_list')