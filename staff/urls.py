from django.urls import path

from .views import (EmployeesList, EmployeesListBonuses,
                    ProjectsList, addEmployee, bonuses, deleteBonus,
                    employeeBonusEdit, employeeDetail, index,
                    project_period, updateBonuses, updateTariff)

app_name = 'staff'


urlpatterns = [
    path('', index, name='index'),

    path('projects/', ProjectsList.as_view(), name='projects_list'),
    path('projects/<int:pk>/month/',
         project_period, name='project_detail'),
    path('projects_date/<int:id>/editTarrif/',
         updateTariff, name="project_tarrif"),
    path('projects_date/<int:pk>/<str:action>/employees/',
         bonuses, name='bonuses'),
    path('projects_date/<int:pk>/addEmployee/',
         addEmployee, name='add_employee'),

    path('projects_date/<int:pk>/updatebonuses/',
         updateBonuses, name='update_bonus'),
    path('projects_date/<int:pk>/deletebonuses/',
         deleteBonus, name='delete_bonus'),

    path('employees/', EmployeesList.as_view(), name='employee_list'),
    path('employees/<int:pk>/', employeeDetail, name='employee_detail'),
    path('employeesBonus/edit/<int:pk>/',
         employeeBonusEdit, name='employee_bonus_edit'),
    path('employeesBonusTotal/', EmployeesListBonuses.as_view(),
         name='employees_bonuses'),
]
