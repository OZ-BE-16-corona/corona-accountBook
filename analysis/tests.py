from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from decimal import Decimal
from rest_framework.test import APITestCase

from analysis.analyzers import Analyzer
from analysis.models import Analysis
from transaction.models import Transaction
from account.models import Account
from category.models import Category


class AnalyzerTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="test@test.com", user_name="testuser", password="1234"
        )

        # 테스트용 Account / Category 생성
        self.account = Account.objects.create(
            user=self.user, account_name="테스트 계좌", balance=0
        )

        self.category = Category.objects.create(category_name="테스트 카테고리")

        # 테스트용 거래 데이터 생성 (출금 1개, 입금 1개)
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            amount=Decimal("5000"),
            currency="KRW",
            transaction_type="EXPENSE",
            transaction_date=date(2026, 2, 10),
        )

        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            amount=Decimal("10000"),
            currency="KRW",
            transaction_type="INCOME",
            transaction_date=date(2026, 2, 11),
        )

    def test_total_expense_analysis(self):
        analyzer = Analyzer()

        result = analyzer.run(
            user=self.user,
            about="TOTAL_EXPENSE",
            type="DAILY",
            period_start=date(2026, 2, 8),
            period_end=date(2026, 2, 12),
            description="지출 테스트",
        )

        self.assertIsInstance(result.analysis, Analysis)
        self.assertTrue(result.analysis.result_image)

    def test_total_income_analysis(self):
        analyzer = Analyzer()

        result = analyzer.run(
            user=self.user,
            about="TOTAL_INCOME",
            type="DAILY",
            period_start=date(2026, 2, 8),
            period_end=date(2026, 2, 12),
            description="수입 테스트",
        )

        self.assertIsInstance(result.analysis, Analysis)
        self.assertTrue(result.analysis.result_image)


class AnalysisListAPITest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="u1@test.com",
            user_name="u1",
            password="1234",
        )
        self.other = User.objects.create_user(
            email="u2@test.com",
            user_name="u2",
            password="1234",
        )

        self.client.force_authenticate(user=self.user)

        Analysis.objects.create(
            user=self.user,
            about="TOTAL_INCOME",
            type="MONTHLY",
            period_start=date(2026, 2, 1),
            period_end=date(2026, 2, 29),
            description="월간 수입",
        )
        Analysis.objects.create(
            user=self.user,
            about="TOTAL_EXPENSE",
            type="WEEKLY",
            period_start=date(2026, 2, 1),
            period_end=date(2026, 2, 7),
            description="주간 지출",
        )

        Analysis.objects.create(
            user=self.other,
            about="TOTAL_EXPENSE",
            type="MONTHLY",
            period_start=date(2026, 2, 1),
            period_end=date(2026, 2, 29),
            description="다른유저 데이터",
        )
