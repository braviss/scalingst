from django.urls import path
from .views import PaymentCreateView, PaymentListView

app_name = "payments"

urlpatterns = [
    path("create/", PaymentCreateView.as_view(), name="create"),
    path("history/", PaymentListView.as_view(), name="history"),
]