from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime

from analysis.services import AnalysisService


class AnalysisCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        about = request.data.get("about")
        type_ = request.data.get("type")
        period_start = request.data.get("period_start")
        period_end = request.data.get("period_end")
        description = request.data.get("description", "")

        # 🔥 필수값 체크
        if not all([about, type_, period_start, period_end]):
            return Response(
                {"detail": "about, type, period_start, period_end는 필수입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            period_start = datetime.strptime(period_start, "%Y-%m-%d").date()
            period_end = datetime.strptime(period_end, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"detail": "날짜 형식은 YYYY-MM-DD 이어야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if period_start > period_end:
            return Response(
                {"detail": "period_start는 period_end보다 늦을 수 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = AnalysisService.create_analysis(
            user=request.user,
            about=about,
            type=type_,
            period_start=period_start,
            period_end=period_end,
            description=description,
        )

        return Response(
            {
                "analysis_id": result.analysis.id,
                "image_url": result.analysis.result_image.url
                if result.analysis.result_image
                else None,
            },
            status=status.HTTP_201_CREATED,
        )
