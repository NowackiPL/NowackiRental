from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


# Create your models here.

class BaseModel(models.Model):
    """Base model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class."""

        abstract = True


class Car(BaseModel):
    type_engines = {
        ('Benzyna', 'Benzyna'),
        ('Diesel', 'Diesel'),
        ('Hybryda', 'Hybryda'),
        ('Elektryczny', 'Elektryczny')
    }
    type_transmission = {
        ('Automatyczna', 'Automatyczna'),
        ('Manuala', 'Manualna')
    }
    number_of_gears = {
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8')
    }
    type_drives = {
        ('Przedni', 'Przedni'),
        ('Tylni', 'Tylni'),
        ('4x4', '4x4')
    }
    type_car = {
        ('Kombi', 'Kombi'),
        ('Sedan', 'Sedan'),
        ('Coupe', 'Coupe'),
        ('Hatchback', 'Hatchback'),
        ('Suv', 'Suv'),
        ('Van', 'Van'),
        ('Shooting brake', 'Shooting brake')
    }
    avatar = models.ImageField(upload_to='media/avatars/', blank=True, null=True)
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 100)],  # Rozmiar miniatury awatara
        format='JPEG',  # Format miniatury awatara
        options={'quality': 80}  # Jakość miniatury awatara
    )
    brand = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    cars_type = models.CharField(max_length=32, choices=type_car)
    engine = models.CharField(max_length=32, choices=type_engines)
    capacity = models.FloatField()
    year = models.CharField(max_length=8)
    number_of_seats = models.IntegerField()
    consumption = models.CharField(max_length=32)
    power = models.CharField(max_length=16)
    car_mileage = models.CharField(max_length=16)
    transmission = models.CharField(max_length=32, choices=type_transmission)
    no_gears = models.CharField(max_length=8, choices=number_of_gears)
    drive = models.CharField(max_length=32, choices=type_drives)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    deposit = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return f"{self.brand}, {self.model}"


class CompanyBranches(BaseModel):
    city = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f"{self.city}"


class Client(BaseModel):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=256, unique=True)
    phone = models.CharField(max_length=32)
    driving_license_no = models.CharField(max_length=32)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"


class Rent(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    period = models.IntegerField(default=0)
    take_from = models.ForeignKey(CompanyBranches, related_name='rents_taken', on_delete=models.CASCADE)
    take_back = models.ForeignKey(CompanyBranches, related_name='rents_returned', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def clean(self):
        if not self.is_car_available():
            raise ValidationError(
                _("This car is not available for the selected dates."),
                params={'value': self},
            )

    def is_car_available(self):
        conflicting_rents = Rent.objects.filter(
            Q(car=self.car),
            Q(start_date__range=(self.start_date, self.end_date)) |
            Q(end_date__range=(self.start_date, self.end_date)) |
            Q(start_date__lte=self.start_date, end_date__gte=self.end_date)
        )

        return not conflicting_rents.exists()

    def save(self, *args, **kwargs):
        # Obliczanie wartości pola 'period' na podstawie różnicy między 'start_date' a 'end_date'
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.period = delta.days

        # Obliczanie wartości pola 'amount' na podstawie ceny samochodu i okresu wynajmu
        if self.car and self.period:
            self.amount = self.car.price * self.period

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rent of {self.car} by {self.client}"


