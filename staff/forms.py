from django import forms
from .models import Bonus, ProjectDate, EmployeeDate


class BonusLaikinas(forms.ModelForm):
    laukas1 = forms.DecimalField(
        required=False, widget=forms.TextInput(attrs={'size': '2'}))
    laukas2 = forms.DecimalField(
        required=False, widget=forms.TextInput(attrs={'size': '2'}))

    class Meta:
        model = EmployeeDate
        exclude = ('employee', 'year_month')


class BonusForm(forms.ModelForm):
    hours = forms.DecimalField(widget=forms.TextInput(attrs={'size': '2'}))
    priedas_geras_darbas = forms.DecimalField(
        widget=forms.TextInput(attrs={'size': '2'}))
    apmokymas = forms.DecimalField(
        widget=forms.TextInput(attrs={'size': '2'}))

    class Meta:
        model = Bonus
        fields = '__all__'
        # exclude = ('project',)


class ProjectDateForm(forms.ModelForm):
    class Meta:
        model = ProjectDate
        fields = '__all__'


class EmployeeDateForm(forms.ModelForm):
    class Meta:
        model = EmployeeDate
        fields = '__all__'
