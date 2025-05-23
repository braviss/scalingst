from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView,
    DeleteView
)
from django.contrib.auth.models import User
from django_countries import countries
from users.utils import get_country_from_ip
from django.conf import settings
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from offers.models import (
    Offer,
    Category,
    Complaint
)
from view_breadcrumbs import (
    ListBreadcrumbMixin,
    DetailBreadcrumbMixin,
    CreateBreadcrumbMixin,
    BaseBreadcrumbMixin, DeleteBreadcrumbMixin,
)
from offers.forms import (
    OfferForm,
    ComplaintForm
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from offers.mixins import CustomLoginRequiredMixin
from django.http import Http404
from django.shortcuts import render

from cities_light.models import City, Region
from django.http import JsonResponse

class HomePageView(TemplateView):
    template_name = 'home.html'


class OfferListView(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    model = Offer
    template_name = 'offer_list.html'
    context_object_name = 'offers'
    ordering = '-created_at'
    paginate_by = 8

    def get_queryset(self):
        queryset = Offer.objects.filter(status='pu').order_by(
            '-is_premium',
            'premium_at',
            'created_at'
        )

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search),
            )

        country_code = self.request.GET.get('country', get_country_from_ip(self.request))
        if country_code:
            queryset = queryset.filter(country=country_code)


        # locale

        region_slug = self.request.GET.get('region')
        if region_slug:
            queryset = queryset.filter(region__slug=region_slug)



        offer_type = self.request.GET.get('type')  # Например, ?type=premium

        if offer_type == 'premium':
            queryset = queryset.filter(is_premium=True)
        elif offer_type == 'regular':
            queryset = queryset.filter(is_premium=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['countries'] = countries
        context['regions'] = Region.objects.all()
        context['offer_type'] = self.request.GET.get('type', 'all')

        return context


class OfferDetailView(LoginRequiredMixin,
                        DetailBreadcrumbMixin,
                        DetailView):
    model = Offer
    breadcrumb_use_pk = False
    template_name = 'offer_detail.html'
    count_hit = True

    def get_object(self, queryset=None):
        obj = super().get_object()

        if obj.status == "re" and obj.author != self.request.user:
            raise Http404("This offer is not available")

        return obj






class OfferCreateView(LoginRequiredMixin,
                        CreateBreadcrumbMixin,
                        CreateView):
    model = Offer
    form_class = OfferForm
    template_name = 'offer_form.html'
    success_url = reverse_lazy('offers:offer_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request,
                         'Ваш офер добавлен, после подтверждения модератора он появиться в списке!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TINYMCE_API_KEY'] = settings.TINYMCE_API_KEY  # Добавляем API-ключ в контекст
        return context




class OfferUpdateView(LoginRequiredMixin,
                      BaseBreadcrumbMixin,
                      UpdateView):
    model = Offer
    form_class = OfferForm
    template_name = 'offer_form.html'
    crumbs = [("Offer update", reverse_lazy('offers:offer_list'))]

    def form_valid(self, form):
        form.instance.status = 'pe'
        messages.success(self.request,
                         'Успешно изменено, оффер будет доступен после проверки модератора.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('offers:offer_list')


class OfferDeleteView(LoginRequiredMixin,
                        DeleteBreadcrumbMixin,
                        DeleteView):
    model = Offer
    template_name = 'offer_confirm_delete.html'
    success_url = reverse_lazy('offers:offer_list')




class UserOfferListView(ListView):
    model = Offer
    template_name = 'profile_view.html'
    context_object_name = 'offers'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        self.user_profile = user
        if self.request.user == user:
            return Offer.objects.filter(author=user).order_by('-created_at')
        return Offer.objects.filter(author=user, status='pu').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.user_profile
        return context


class ComplaintCreateView(
    CustomLoginRequiredMixin,
    CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaint_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.offer = get_object_or_404(Offer, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.offer = self.offer
        messages.success(self.request, 'Ваша жалоба успешно отправлена!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('offers:offer_list')



class CategoryListView(CustomLoginRequiredMixin,
                      ListBreadcrumbMixin,
                      ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    ordering = '-created_at'
    paginate_by = 10



def external_link_warning(request):
    external_url = request.GET.get("url", "")
    return render(request, "external_warning.html", {"external_url": external_url})



def get_cities(request, country_code):
    print(f"Получен код страны: {country_code}")
    if country_code == '1':
        # Оптимизируем запрос с помощью select_related
        cities = City.objects.select_related('region__country').filter(region__country__id='1')
        print(f"Найдено {len(cities)} городов.")
        city_data = [{'id': city.id, 'name': city.name} for city in cities]
        return JsonResponse({'cities': city_data})
    return JsonResponse({'cities': []})