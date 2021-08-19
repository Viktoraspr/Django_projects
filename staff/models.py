from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class Project(models.Model):
    project_number = models.CharField(max_length=20, default='', unique=True)
    name = models.CharField(max_length=150, default='')
    country = models.CharField(default="Lietuva", max_length=150)
    started = models.DateField(
        default=timezone.now().today, blank=True, null=True)
    finished = models.DateField(default='', blank=True, null=True)
    created = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['finished', 'started']
        verbose_name_plural = "Objektai"

    def __str__(self) -> str:
        return f'{self.project_number}, {self.name}, {self.country}'


class ProjectDate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    year_month = models.CharField(
        default='', max_length=7, blank=True, null=True)
    tarrif = models.DecimalField(
        default=0, max_digits=3, decimal_places=2)

    class Meta:
        ordering = ['year_month']
        verbose_name_plural = "Projektai, mėnuo"

    def __str__(self) -> str:
        return f'{self.project}, {self.year_month}, {self.tarrif}'


class Employee(models.Model):
    tabelis = models.IntegerField(default=0)
    name = models.CharField(max_length=120, default='')
    surname = models.CharField(max_length=200, default='')
    kategorija = models.CharField(max_length=100, default='K01')

    class Meta:
        ordering = ['tabelis']
        verbose_name_plural = "Darbuotojai"

    def __str__(self) -> str:
        return f'Nr. {self.tabelis}, {self.name} {self.surname}'

# sita reikia istrinti ir i forma paduoti skirtingus laukus


class EmployeeDate(models.Model):
    employee = models.ForeignKey(Employee, on_delete=CASCADE)
    year_month = models.CharField(
        default='', max_length=7, blank=True, null=True)
    laukas1 = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    laukas2 = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    @property
    def viso(self):
        viso = self.laukas1 + self.laukas2
        return viso

    class Meta:
        ordering = ['employee']
        verbose_name_plural = "Darbuotojo bonusai"

    def __str__(self) -> str:
        return f'Nr. {self.employee}, {self.year_month},\
        {self.laukas1}, {self.laukas2}, {self.viso} '


class Bonus(models.Model):
    project = models.ForeignKey(ProjectDate, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    hours = models.DecimalField(
        default=0, max_digits=5, decimal_places=2)
    priedas_geras_darbas = models.DecimalField(
        default=0, max_digits=6, decimal_places=2)
    apmokymas = models.DecimalField(
        default=0, max_digits=6, decimal_places=2)
    kelione_Lietuva = models.DecimalField(
        default=0, max_digits=6, decimal_places=2)
    kelione_uzsienis = models.DecimalField(
        default=0, max_digits=6, decimal_places=2)
    koordinatoriaus_priedas = models.DecimalField(
        default=0, max_digits=6, decimal_places=2)
    daugiau_nei_12_savaiciu = models.DecimalField(
        default=0, max_digits=6, decimal_places=2)
    klaida_algalapyje = models.DecimalField(
        default=0, max_digits=6, decimal_places=2)
    naujas_darbuotojas = models.DecimalField(
        default=0, max_digits=6, decimal_places=2)
    kita = models.DecimalField(
        default=0, max_digits=6, decimal_places=2)

    @property
    def suma(self):
        suma = self.priedas_geras_darbas + self.apmokymas +\
            self.kelione_Lietuva + self.kelione_uzsienis + \
            self.koordinatoriaus_priedas + self.daugiau_nei_12_savaiciu + \
            self.klaida_algalapyje + self.naujas_darbuotojas + self.kita
        return suma

    class Meta:
        verbose_name_plural = "Lauko bonusai"
        ordering = ['-project']
        unique_together = [['project', 'employee']]

    def __str__(self) -> str:
        return f'{self.employee}, {self.project}, {self.project.year_month}, \
            {self.suma}'
