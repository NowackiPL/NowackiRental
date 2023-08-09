from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Car, Client, Rent, CompanyBranches


# Register your models here.


class CarAdmin(ModelAdmin):
    ordering = ["id"]
    list_display = [
        "id", 'avatar', "brand", "model", "cars_type", "engine", "capacity", "year", "number_of_seats", "consumption",
        "power",
        "car_mileage", "transmission", 'no_gears', "drive", "price", "deposit"]


class RentAdmin(ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "client", 'car', 'start_date', 'end_date', 'take_from', 'take_back', 'amount']


class CompanyBranchesAdmin(ModelAdmin):
    ordering = ["id"]
    list_display = ['id', 'city']


class ClientAdmin(ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "first_name", "last_name", 'email', 'phone', 'driving_license_no', 'user']


admin.site.register(Car, CarAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Rent, RentAdmin)
admin.site.register(CompanyBranches, CompanyBranchesAdmin)
