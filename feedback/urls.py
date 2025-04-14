from django.urls import path
from feedback import views


app_name = 'feedback'

urlpatterns = [
    path('add/',
         views.FeedbackCreateView.as_view(),
         name='add'),
    path('thanks/',
         views.FeedbackThanksView.as_view(),
         name='thanks'),
]
