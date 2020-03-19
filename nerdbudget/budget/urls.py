from django.urls import path

from .views import (BudgetCreateView, BudgetDeleteView, BudgetListView,
                    BudgetUpdateView)

urlpatterns = [
    path('', BudgetListView.as_view(), name='budget-list'),
    path('create/', BudgetCreateView.as_view(), name='budget-create'),
    path('update/<int:pk>/', BudgetUpdateView.as_view(), name='budget-update'),
    path('delete/<int:pk>/', BudgetDeleteView.as_view(), name='budget-delete'),
]
