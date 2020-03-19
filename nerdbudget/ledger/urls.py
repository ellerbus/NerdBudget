from django.urls import path

from .views import (LedgerCheckView, LedgerDeleteView, LedgerImportView,
                    LedgerListView, LedgerUpdateView)

urlpatterns = [
    path('', LedgerListView.as_view(), name='ledger-list'),
    path('check/', LedgerCheckView.as_view(), name='ledger-check'),
    path('import/', LedgerImportView.as_view(), name='ledger-import'),
    path('update/<int:pk>/', LedgerUpdateView.as_view(), name='ledger-update'),
    path('delete/<int:pk>/', LedgerDeleteView.as_view(), name='ledger-delete'),
]
