from django.urls import path
from .views import department_tree_view

urlpatterns = [
    path("", department_tree_view, name="employees-list"),
]
