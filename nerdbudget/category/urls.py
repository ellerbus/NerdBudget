from django.urls import path

from .views import (CategoryCreateView, CategoryDeleteView, CategoryListView,
                    CategoryUpdateView)

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('create/', CategoryCreateView.as_view(), name='category-create'),
    path('update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
]
