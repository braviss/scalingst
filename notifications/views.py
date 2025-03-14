from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from view_breadcrumbs import (
    ListBreadcrumbMixin,
    DeleteBreadcrumbMixin,
)
from django.views.generic import (
    ListView
)
from django.views import View
from django.urls import reverse_lazy


@login_required
def mark_notifications_as_read(request):
    request.user.notifications.update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


class NotificationListView(LoginRequiredMixin,
                    ListView):
    model = Notification
    template_name = 'notification_list.html'
    context_object_name = 'notif'
    ordering = '-created_at'
    paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')



class NotificationDeleteAllView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        Notification.objects.filter(user=request.user).delete()
        return redirect(reverse_lazy('notifications:notification_list'))