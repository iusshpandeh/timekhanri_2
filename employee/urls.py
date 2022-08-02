from django.urls import path
from . import views

urlpatterns = [
    path('add_employee',views.add_employee, name = 'add_employee'),
    path('login_employee', views.login_employee, name = 'login_employee'),
    path('delete_employee',views.delete_employee, name = 'delete_employee'),
    path('details_employee', views.details_employee, name='details_employee'),
    path('reports_employee', views.reports_employee, name='reports_employee')
]
