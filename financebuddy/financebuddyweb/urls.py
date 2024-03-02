from django.urls import path
from . import views
from .views import BillCreateView, BillListView, BillUpdateView, ExpenseUpdateView, ExpenseDeleteView, CustomLogoutView, BudgetCreateView, IncomeDeleteView, IncomeUpdateView, budget_list, BudgetUpdateView, BudgetDeleteView, FinancialGoalCreateView, FinancialGoalListView, FinancialGoalUpdateView, FinancialGoalUpdateView, FinancialGoalDeleteView, dashboard_view, AccountCreateView, expense_trends_view, budget_vs_actual_view, add_income, income_list

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('add-expense/', views.add_expense_view, name='add_expense'),
    path('expenses-list/', views.expenses_list_view, name='expenses_list'),
    path('expenses-summary/', views.expenses_summary_view, name='expenses_summary'),
    path('expenses-trends/', expense_trends_view, name='expenses_trends'),
    path('expense/edit/<int:pk>/', ExpenseUpdateView.as_view(), name='edit_expense'),
    path('expense/delete/<int:pk>/', ExpenseDeleteView.as_view(), name='delete_expense'),
    path('budgets/', budget_list, name='budget_list'),
    path('budget-vs-actual/', budget_vs_actual_view, name='budget_vs_actual'),
    path('budget/add/', BudgetCreateView.as_view(), name='budget_add'),
    path('budget/edit/<int:pk>/', BudgetUpdateView.as_view(), name='edit_budget'),
    path('budget/delete/<int:pk>/', BudgetDeleteView.as_view(), name='delete_budget'),
    path('financial-goals/', FinancialGoalListView.as_view(), name='financial_goal_list'),
    path('financial-goal/add/', FinancialGoalCreateView.as_view(), name='financial_goal_add'),
    path('financial-goal/<int:pk>/edit/', FinancialGoalUpdateView.as_view(), name='financial_goal_edit'),
    path('financial-goal/<int:pk>/edit/', FinancialGoalUpdateView.as_view(), name='financial_goal_edit'),
    path('financial-goal/<int:pk>/delete/', FinancialGoalDeleteView.as_view(), name='financial_goal_delete'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('accounts/add/', AccountCreateView.as_view(), name='account_add'),
    path('bills/', BillListView.as_view(), name='bill_list'),
    path('bills/add/', BillCreateView.as_view(), name='bill_add'),
    path('bills/<int:pk>/edit/', BillUpdateView.as_view(), name='bill_edit'),
    path('income/', income_list, name='income_list'),
    path('income/add/', add_income, name='add_income'),
    path('income/edit/<int:pk>/', IncomeUpdateView.as_view(), name='edit_income'),
    path('income/delete/<int:pk>/', IncomeDeleteView.as_view(), name='delete_income'),
]   
