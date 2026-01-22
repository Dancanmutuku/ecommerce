from django.shortcuts import render
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order

# Create your views here.
@csrf_exempt
def mpesa_callback(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    data = json.loads(request.body)

    callback = data.get("Body", {}).get("stkCallback", {})
    result_code = callback.get("ResultCode")
    metadata = callback.get("CallbackMetadata", {}).get("Item", [])

    if result_code == 0:
        order_id = None
        mpesa_receipt = None

        for item in metadata:
            if item["Name"] == "AccountReference":
                order_id = item["Value"]
            if item["Name"] == "MpesaReceiptNumber":
                mpesa_receipt = item["Value"]

        if order_id:
            order = Order.objects.filter(id=order_id).first()
            if order:
                order.status = "PAID"
                order.save()

    return HttpResponse(status=200)
