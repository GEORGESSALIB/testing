from django.urls import path
from . import views

urlpatterns = [
    path('', views.computer_list, name='computer_list'),
    path('assign/<int:computer_id>/', views.assign_computer, name='assign_computer'),
    path('return/<int:computer_id>/', views.return_computer, name='return_computer'),
    path('computer/<int:computer_id>/history/', views.computer_history, name='computer_history'),
    path('export/csv/', views.export_computers_csv, name='export_computers_csv'),
path('computer/<int:computer_id>/export/history/csv/', views.export_computer_history_csv, name='export_computer_history_csv'),
]