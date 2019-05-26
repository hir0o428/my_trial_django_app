from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.shortcuts import resolve_url
from django.utils import timezone

from .models import Demand
from .forms import LoginForm, DemandCreateForm, DemandUpdateForm
from .filters import DemandFilter, DemandAnalysisFilter
from demand_manager.utils.demand_summary import DemandFeature

# Create your views here.
class DemandLoginView(LoginView):
    form_class = LoginForm
    template_name = "demand_manager/demand_login.html"


class DemandLogoutView(LogoutView):
    template_name = "demand_manager/demand_logout.html"


class DemandTopView(LoginRequiredMixin, ListView):
    model = Demand
    template_name = "demand_manager/demand_top.html"


class DemandTopFilterView(LoginRequiredMixin, FilterView):
    model = Demand
    filterset_class = DemandFilter
    template_name = "demand_manager/demand_top_filter.html"

    # paginate_by = 10

    '''
    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]
        return super().get(request, **kwargs)
    '''

    def get_queryset(self):
        return Demand.objects.all().order_by('start_date')


class DemandDetailView(LoginRequiredMixin, DetailView):
    model = Demand
    template_name = 'demand_manager/demand_detail.html'


class DemandCreateView(LoginRequiredMixin, CreateView):
    model = Demand
    template_name = 'demand_manager/demand_create.html'
    form_class = DemandCreateForm
    success_url = '/demand_manager'

    def form_valid(self, form):
        """

        :param form:
        :return:
        """
        demand = form.save(commit=False)
        demand.user_create = self.request.user
        demand.time_create = timezone.now()
        demand.user_update = self.request.user
        demand.time_update = timezone.now()
        demand.save()

        return super().form_valid(form)


class DemandUpdateView(LoginRequiredMixin, UpdateView):
    model = Demand
    template_name = 'demand_manager/demand_update.html'
    form_class = DemandUpdateForm

    def get_success_url(self):
        return resolve_url('demand_manager:detail', pk=self.kwargs['pk'])

    def form_valid(self, form):
        """

        :param form:
        :return:
        """
        demand = form.save(commit=False)
        demand.user_update = self.request.user
        demand.time_update = timezone.now()
        demand.save()

        return super().form_valid(form)


class DemandDeleteView(LoginRequiredMixin, DeleteView):
    model = Demand
    success_url = '/demand_manager'


class DemandAnalysisView(LoginRequiredMixin, FilterView):
    model = Demand
    filterset_class = DemandAnalysisFilter
    template_name = 'demand_manager/demand_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calc Demand Feature
        demand_feature = DemandFeature()
        demand_feature.demand_summary()
        context['df_demand_feature'] = demand_feature.df_demand_feature
        context['ser_pct_demand'] = demand_feature.ser_pct_max_demand
        context['ser_num_demand'] = demand_feature.ser_num_max_demand
        context['ser_num_release'] = demand_feature.df_release_feature.max().astype('int64')
        context['ser_required_lic'] = demand_feature.ser_required_lic
        context['df_png_path'] = demand_feature.df_png_path
        return context
