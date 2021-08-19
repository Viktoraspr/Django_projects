from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Deliver(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='todolist', null=True)
    name = models.CharField(max_length=200)
    code = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    customer = models.CharField(max_length=200)
    company_code = models.IntegerField()
    representative = models.CharField(max_length=200)
    adress = models.CharField(max_length=500)
    country = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self) -> str:
        return self.customer


class Scaffolding(models.Model):
    pastolio_numeris = models.CharField(
        max_length=200, unique=True)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    lenght = models.IntegerField(default=0)

    @property
    def volume(self):
        volume = self.height*self.width*self.lenght
        return volume

    def __str__(self) -> str:
        return f'{self.pastolio_numeris}, {self.height}, {self.width}, \
        {self.lenght}, {self.volume}'


class Order(models.Model):
    order = models.CharField(max_length=250, default='')
    deliver = models.ForeignKey(
        Deliver, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    scaffoldig = models.ForeignKey(
        Scaffolding, on_delete=models.CASCADE, null=True)
    order_date = models.DateField(default=timezone.now())
    assembled_date = models.DateField(null=True)
    dismanatled_date = models.DateField(null=True)

    Choices = models.TextChoices('Choices', 'Yes No N//A')
    stable = models.CharField(choices=Choices.choices,
                              max_length=50, default='Yes')
    base_leveled = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')
    number_of_braces = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')
    platform_guardrails_height = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')
    gaps_35mm = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')
    stable_structure = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')
    proper_sideboards = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')
    metal_perforated_grating_completely_covers = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')
    safe_entrance = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')
    stiff_and_secured = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')
    tag_filled = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')
    marked_noticed = models.CharField(
        choices=Choices.choices, max_length=50, default='Yes')

    active = models.BooleanField()

    def __str__(self) -> str:
        return self.order

    class Meta:
        ordering = ['order_date']
