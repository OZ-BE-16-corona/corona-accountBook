from django.urls import path
from analysis.views import AnalysisCreateView, AnalysisListView

urlpatterns = [
    # POST /api/analysis/
    path("", AnalysisCreateView.as_view(), name="analysis-create"),
    path("list/", AnalysisListView.as_view(), name="analysis-list"),
]
