from rest_framework import serializers
from analysis.models import Analysis


class AnalysisListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = [
            "id",
            "about",
            "type",
            "period_start",
            "period_end",
            "description",
            "image_url",
            "created_at",
            "updated_at",
        ]

    def get_image_url(self, obj):
        if obj.result_image:
            request = self.context.get("request")
            # absolute url로 주고 싶으면 build_absolute_uri 사용
            return (
                request.build_absolute_uri(obj.result_image.url)
                if request
                else obj.result_image.url
            )
        return None
