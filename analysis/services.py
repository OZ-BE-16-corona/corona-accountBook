from analysis.analyzers import Analyzer


class AnalysisService:
    @staticmethod
    def create_analysis(*, user, about, type, period_start, period_end, description=""):
        analyzer = Analyzer()
        return analyzer.run(
            user=user,
            about=about,
            type=type,
            period_start=period_start,
            period_end=period_end,
            description=description,
        )
