from django.urls import path
from payments.views import (
    PaymentCreateAPI,
    PaymentListAPI,
    PaymentDetailAPI,
    PaymentUpdateAPI,
    PaymentDeleteAPI,
)

app_name = 'payments'

urlpatterns = [
    path('', PaymentListAPI.as_view(), name='payment-list'),
    path('create/', PaymentCreateAPI.as_view(), name='payment-create'),
    path('<uuid:id>/', PaymentDetailAPI.as_view(), name='payment-detail'),
    path('<uuid:id>/update/', PaymentUpdateAPI.as_view(), name='payment-update'),
    path('<uuid:id>/delete/', PaymentDeleteAPI.as_view(), name='payment-delete'),
]

