from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, FormView, DeleteView, ListView, UpdateView, DetailView, CreateView
from .forms import CarsForm
from .models import Car


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class HomeView(TemplateView):
    template_name = 'home.html'


class CarCreateView(LoginRequiredMixin, FormView):
    template_name = 'form.html'
    form_class = CarsForm
    success_url = '/cars/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CarUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Car
    form_class = CarsForm
    success_url = '/cars/'


class CarsDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    template_name = 'delete.html'
    model = Car
    success_url = 'home'


class CarsListView(ListView):
    template_name = 'cars_list.html'
    model = Car


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'


class SubmittableLoginView(LoginView):
    template_name = 'form.html'
    next_page = 'home'


class SingUp(CreateView):
    template_name = 'form.html'
    form_class = UserCreationForm
    success_url = '/login/'


class Logout(LogoutView):
    next_page = 'home'
