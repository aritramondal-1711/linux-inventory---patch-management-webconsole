from django.urls import path
from . import views

urlpatterns = [
    path("",views.inventory),
    path("add",views.addserver),
    path("delete",views.delserver),
    path("patch",views.patchjob),
    path("patch/initiate",views.patchinitiate)
]
