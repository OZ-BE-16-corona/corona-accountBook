# analysis/analyzers.py
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date
from io import BytesIO

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from django.core.files.base import ContentFile
from django.db import transaction as db_tx

from analysis.models import Analysis
from transaction.models import Transaction


AboutType = str
PeriodType = str


@dataclass(frozen=True)
class AnalyzerResult:
    analysis: Analysis
    dataframe: pd.DataFrame


class Analyzer:
    def run(
        self,
        *,
        user,
        about: AboutType,
        type: PeriodType,
        period_start: date,
        period_end: date,
        description: str = "",
    ) -> AnalyzerResult:
        qs = Transaction.objects.filter(
            user=user,
            transaction_date__gte=period_start,
            transaction_date__lte=period_end,
        ).select_related("category", "account")

        rows = qs.values(
            "transaction_date",
            "amount",
            "transaction_type",
            "category__category_name",
        )
        df = pd.DataFrame(list(rows))

        if df.empty:
            df = pd.DataFrame({"message": ["No data in period"]})
            image_file = self._plot_empty(
                f"No transactions ({period_start} ~ {period_end})"
            )
        else:
            image_file = self._plot(
                df,
                about=about,
                type=type,
                period_start=period_start,
                period_end=period_end,
            )

        with db_tx.atomic():
            analysis = Analysis.objects.create(
                user=user,
                about=about,
                type=type,
                period_start=period_start,
                period_end=period_end,
                description=description,
            )
            filename = f"analysis_{user.pk}_{uuid.uuid4().hex}.png"
            analysis.result_image.save(filename, image_file, save=True)

        return AnalyzerResult(analysis=analysis, dataframe=df)

    def _plot(
        self,
        df: pd.DataFrame,
        *,
        about: AboutType,
        type: PeriodType,
        period_start: date,
        period_end: date,
    ) -> ContentFile:
        df["amount"] = df["amount"].astype(float)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])

        # ✅ 기간 전체 날짜(일 단위) 생성: 데이터가 1개/0개여도 축이 이상해지지 않게
        full_days = pd.date_range(
            start=pd.to_datetime(period_start), end=pd.to_datetime(period_end), freq="D"
        )

        # ✅ 총 지출 / 총 수입 (일자별 합계)
        if about in ("TOTAL_EXPENSE", "TOTAL_INCOME"):
            target_type = (
                Transaction.TransactionType.EXPENSE
                if about == "TOTAL_EXPENSE"
                else Transaction.TransactionType.INCOME
            )
            filtered = df[df["transaction_type"] == target_type].copy()

            if filtered.empty:
                # ✅ “축만 있는 빈 그래프” 대신 안내 이미지
                label = "EXPENSE(출금)" if about == "TOTAL_EXPENSE" else "INCOME(입금)"
                return self._plot_empty(
                    f"No {label} in period ({period_start} ~ {period_end})"
                )

            grouped = filtered.groupby(filtered["transaction_date"].dt.date)[
                "amount"
            ].sum()
            # date index로 변환 후 full_days에 맞춰 reindex
            series = pd.Series(grouped.values, index=pd.to_datetime(grouped.index))
            series = series.reindex(full_days, fill_value=0.0)

            fig = plt.figure()
            ax = plt.gca()

            ax.set_title(f"{about} ({period_start} ~ {period_end})")
            ax.set_xlabel("date")
            ax.set_ylabel("amount")

            # ✅ 보기 좋게: bar + marker 느낌(막대가 안정적)
            ax.bar(series.index, series.values)

            # ✅ 축/포맷 정리
            ax.set_xlim(full_days[0], full_days[-1])
            ax.set_ylim(bottom=0)

            ax.xaxis.set_major_locator(
                mdates.DayLocator(interval=max(1, len(full_days) // 7))
            )
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
            plt.xticks(rotation=45)

            return self._save_fig_to_contentfile(fig)

        # ✅ 카테고리별 지출/수입
        if about in ("CATEGORY_EXPENSE", "CATEGORY_INCOME"):
            target_type = (
                Transaction.TransactionType.EXPENSE
                if about == "CATEGORY_EXPENSE"
                else Transaction.TransactionType.INCOME
            )
            filtered = df[df["transaction_type"] == target_type].copy()

            if filtered.empty:
                label = (
                    "EXPENSE(출금)" if about == "CATEGORY_EXPENSE" else "INCOME(입금)"
                )
                return self._plot_empty(
                    f"No {label} in period ({period_start} ~ {period_end})"
                )

            grouped = (
                filtered.groupby("category__category_name")["amount"]
                .sum()
                .sort_values(ascending=False)
            )

            fig = plt.figure()
            ax = plt.gca()
            ax.set_title(f"{about} by category ({period_start} ~ {period_end})")
            ax.set_xlabel("category")
            ax.set_ylabel("amount")

            ax.bar(grouped.index.astype(str), grouped.values)
            ax.set_ylim(bottom=0)
            plt.xticks(rotation=45, ha="right")

            return self._save_fig_to_contentfile(fig)

        return self._plot_empty(f"Unsupported about: {about}")

    def _plot_empty(self, message: str) -> ContentFile:
        fig = plt.figure()
        plt.title("No data")
        plt.text(0.5, 0.5, message, ha="center", va="center")
        plt.axis("off")
        return self._save_fig_to_contentfile(fig)

    def _save_fig_to_contentfile(self, fig) -> ContentFile:
        buf = BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="png", dpi=150)
        plt.close(fig)
        buf.seek(0)
        return ContentFile(buf.getvalue())
