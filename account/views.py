from django.http import JsonResponse


def account_detail(request, account_id):
    return JsonResponse({"account_id": account_id, "message": "계좌 상세 조회"})


def account_count(request):
    return JsonResponse({"total": 3})
