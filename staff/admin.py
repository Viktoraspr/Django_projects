from django.contrib import admin
from .models import Project, Employee, Bonus, ProjectDate, EmployeeDate


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_number', 'name', 'country', 'started',
                    'finished', 'created')
    exclude = ('created', )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Employee)
admin.site.register(Bonus)
admin.site.register(ProjectDate)
admin.site.register(EmployeeDate)
