from django.forms import (ModelForm)
from .models import Car


class CarsForm(ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
