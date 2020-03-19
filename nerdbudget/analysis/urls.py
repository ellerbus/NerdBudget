from django.urls import path

from .views import AnalysisHomeView

urlpatterns = [
    path('', AnalysisHomeView.as_view(), name='analysis-home'),
]
