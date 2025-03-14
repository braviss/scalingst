from django.urls import path
from notifications.views import mark_notifications_as_read
from notifications import views


app_name = 'notifications'  # Это важно для работы namespace

urlpatterns = [
    path('mark-as-read/', mark_notifications_as_read, name='mark_as_read'),
    path('all/',
         views.NotificationListView.as_view(),
         name='notification_list'),

    path('delete/',
         views.NotificationDeleteAllView.as_view(),
         name='notification_delete'),
]
