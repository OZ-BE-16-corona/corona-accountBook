from django.urls import path
from analysis.views import AnalysisCreateView

urlpatterns = [
    # POST /api/analysis/
    path("", AnalysisCreateView.as_view(), name="analysis-create"),
]
