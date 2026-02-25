from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Transaction
from .serializers import TransactionSerializer
from .services import create_transaction


class TransactionListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Transaction.objects.filter(user=request.user)

        t_type = request.query_params.get('type')
        account_id = request.query_params.get('account')

        if t_type:
            queryset = queryset.filter(transaction_type=t_type)
        if account_id:
            queryset = queryset.filter(account_id=account_id)

        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            result = create_transaction(
                user_id=request.user.id,
                account_id=request.data.get('account'),
                amount=request.data.get('amount'),
                currency=request.data.get('currency', 'KRW'),
                transaction_type=request.data.get('transaction_type'),
                memo=request.data.get('memo', ''),
                transaction_date=request.data.get('transaction_date'),
                category_id=request.data.get('category')
            )
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Transaction, pk=pk, user=user)

    def get(self, request, pk):
        tx = self.get_object(pk, request.user)
        return Response(TransactionSerializer(tx).data)

    def delete(self, request, pk):
        # Mission 5: 삭제
        tx = self.get_object(pk, request.user)
        tx.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)