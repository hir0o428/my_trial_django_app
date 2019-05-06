from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import resolve_url
from django.utils import timezone

from .models import Demand
from .forms import LoginForm, DemandCreateForm, DemandUpdateForm


# Create your views here.
class DemandLoginView(LoginView):
    form_class = LoginForm
    template_name = "demand_manager/demand_login.html"


class DemandLogoutView(LogoutView):
    template_name = "demand_manager/demand_logout.html"


class DemandTopView(LoginRequiredMixin, ListView):
    model = Demand
    template_name = "demand_manager/demand_top.html"


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
