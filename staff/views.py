from django.db.models import Q
from django.forms import modelformset_factory, inlineformset_factory
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView
from django.forms import TextInput
from django.contrib.auth.decorators import login_required

from .forms import BonusForm, ProjectDateForm, EmployeeDateForm
from .models import Bonus, Employee, Project, ProjectDate, EmployeeDate
from .own_modules import Period


def laikinas(request):
    bonuses = Bonus.objects.all()
    context = {'bonuses': bonuses}
    return render(request, 'staff/laikinas.html', context=context)


@login_required
def bonuses(request, pk, action='all'):
    project_date = ProjectDate.objects.get(pk=pk)
    bonuses = Bonus.objects.filter(project=pk)

    context = {'bonuses': bonuses, 'action': action,
               'project_date': project_date}

    if action == 'all':
        return render(request, 'staff/bonus_all.html', context=context)
    elif action == 'details':
        return render(request, 'staff/bonus_details.html', context=context)
    elif action == 'edit':
        dydis = {'size': '3'}
        widgets = {
            'hours': TextInput(attrs=dydis),
            'priedas_geras_darbas': TextInput(attrs=dydis),
            'apmokymas': TextInput(attrs=dydis),
            'kelione_Lietuva': TextInput(attrs=dydis),
            'kelione_uzsienis': TextInput(attrs=dydis),
            'koordinatoriaus_priedas': TextInput(attrs=dydis),
            'daugiau_nei_12_savaiciu': TextInput(attrs=dydis),
            'klaida_algalapyje': TextInput(attrs=dydis),
            'naujas_darbuotojas': TextInput(attrs=dydis),
            'kita': TextInput(attrs=dydis),
        }
        BonusFormSet = modelformset_factory(
            Bonus, fields='__all__', exclude=('project',),
            widgets=widgets, extra=0)

        if request.method == "POST":
            formset = BonusFormSet(
                request.POST, request.FILES, queryset=bonuses)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect(reverse('staff:bonuses',
                                                    args=(pk, 'all')))
            else:
                print(formset.errors)
        else:
            formset = BonusFormSet(queryset=bonuses)

        context['formset'] = formset
        return render(request, 'staff/bonus_edit.html', context=context)


# @login_required
class ProjectsList(ListView):
    model = Project
    template_name = 'staff/projects.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query = self.request.GET.get('q')
            object_list = Project.objects.filter(Q(name__icontains=query))
            return object_list
        else:
            return Project.objects.all()


@login_required
def updateTariff(request, id):
    projectDate = ProjectDate.objects.get(id=id)
    form = ProjectDateForm(instance=projectDate)
    if request.method == 'POST':
        form = ProjectDateForm(request.POST, instance=projectDate)
        if form.is_valid():
            form.save()

            bonuses = Bonus.objects.filter(project=id)
            for b in bonuses:
                b.priedas_geras_darbas = b.hours * b.project.tarrif
                b.save()

            return HttpResponseRedirect(reverse('staff:project_detail',
                                                args=(projectDate.project.id,)
                                                )
                                        )
        else:
            form = ProjectDateForm(instance=projectDate)

    context = {"form": form}
    return render(request, 'staff/updateTarrif.html', context=context)


@login_required
def project_period(request, pk, edit=None):
    try:
        project = get_object_or_404(Project, id=pk)
        period = Period()
        project_date = ProjectDate.objects.filter(project=pk)

        three_months = [period.two_months_ago,
                        period.last_month, period.current_month]
        tarrifs = []
        project_date_id = []
        for month in three_months:
            try:
                tarrifs.append(project_date.filter(year_month=month)[0])
            except IndexError:
                proj = ProjectDate(
                    project=project, year_month=month, tarrif=0)
                proj.save()
                project_date_id.append(proj.id)
                tarrifs.append(proj)

        context = {'project': project, 'project_date': project_date}

        return render(request, 'staff/project.html', context=context)
    except Project.DoesNotExist:
        raise Http404


@login_required
def addEmployee(request, pk):
    BonusFormSet = inlineformset_factory(ProjectDate, Bonus, fields=[
                                         'employee', 'hours',
                                         'priedas_geras_darbas', 'apmokymas',
                                         'kelione_Lietuva', 'kelione_uzsienis',
                                         'koordinatoriaus_priedas',
                                         'daugiau_nei_12_savaiciu',
                                         'klaida_algalapyje',
                                         'naujas_darbuotojas',
                                         'kita'], extra=1)
    project_date = ProjectDate.objects.get(id=pk, )
    formset = BonusFormSet(queryset=Bonus.objects.none(),
                           instance=project_date)
    if request.method == "POST":
        formset = BonusFormSet(request.POST, instance=project_date)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('staff:bonuses',
                                                args=(project_date.id,
                                                      'all')))
        else:
            formset = BonusFormSet(queryset=Bonus.objects.none(),
                                   instance=project_date)
    context = {'formset': formset, 'project_date': project_date}

    return render(request, 'staff/addEmployee.html', context=context)


@login_required
def updateBonuses(request, pk):
    bonus = Bonus.objects.get(id=pk)
    form = BonusForm(instance=bonus)
    if request.method == 'POST':
        form = BonusForm(request.POST, instance=bonus)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('staff:bonuses',
                                                args=(bonus.project.id,
                                                      'all')))
        else:
            form = BonusForm(instance=bonus)

    context = {"form": form, 'action': 'all'}
    return render(request, 'staff/addEmployee.html', context=context)


@login_required
def deleteBonus(request, pk):
    bonus = Bonus.objects.get(id=pk)
    if request.method == "POST":
        bonus.delete()
        return HttpResponseRedirect(reverse('staff:bonuses',
                                            args=(bonus.project.id, 'all')))
    context = {"bonus": bonus, 'action': 'all'}
    return render(request, 'staff/deleteBonuses.html', context=context)


@login_required
def index(request):
    return render(request, 'staff/base.html', {})


# @login_required
class EmployeesList(ListView):
    model = Employee
    template_name = 'staff/employees.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query = self.request.GET.get('q')
            object_list = Employee.objects.filter(
                Q(name__icontains=query) | Q(
                    surname__icontains=query) | Q(tabelis__icontains=query)
            )
            return object_list
        else:
            return Employee.objects.all()

    def post(self, request):
        Employee.object.create()


@login_required
def employeeDetail(request, pk):
    employee = Employee.objects.get(id=pk)
    employee_month = EmployeeDate.objects.filter(employee=pk)
    context = {"employee_months": employee_month, 'employee': employee}
    return render(request, 'staff/employee.html', context=context)


@login_required
def employeeBonusEdit(request, pk):
    employeeDate = EmployeeDate.objects.get(id=pk)
    form = EmployeeDateForm(instance=employeeDate)
    context = {'employeeDate': employeeDate, 'form': form}
    if request.method == 'POST':
        form = EmployeeDateForm(request.POST, instance=employeeDate)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('staff:employee_detail',
                                                args=(
                                                    employeeDate.employee.id,)
                                                ))
        else:
            form = EmployeeDateForm(instance=employeeDate)

    return render(request, 'staff/employeeEdit.html', context=context)


class EmployeesListBonuses(ListView):
    model = Employee
    template_name = 'staff/employeesBonuses.html'
    context_object_name = 'employees'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query = self.request.GET.get('q')
            object_list = Employee.objects.filter(
                Q(name__icontains=query) | Q(
                    surname__icontains=query) | Q(tabelis__icontains=query)
            )
            return object_list
        else:
            return Employee.objects.all()
