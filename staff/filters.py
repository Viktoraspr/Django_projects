from models import Project
from django_filters import FilterSet

"""
https://django-filter.readthedocs.io/en/stable/guide/install.html
https://www.youtube.com/watch?v=G-Rct7Na0UQ
"""


class ProjectFilter(FilterSet):
    class Meta:
        model = Project
        fields = ['project_number__name']
