from django.urls import path

from .views import HomeView, CarsListView, CarCreateView, CarsDeleteView, CarUpdateView, CarDetailView, \
    SubmittableLoginView, Logout, SingUp

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cars/', CarsListView.as_view(), name='cars'),
    path('cars/create/', CarCreateView.as_view(), name='create_car'),
    path('cars/<int:pk>/delete/', CarsDeleteView.as_view(), name='delete'),
    path('cars/update/<pk>', CarUpdateView.as_view(), name='update'),
    path('cars/<int:pk>/car_detail/', CarDetailView.as_view(), name='detail'),
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', SingUp.as_view(), name='register'),
]
