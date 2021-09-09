from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sketch/', views.showsketch, name='upload'),
    path('edit/<int:id>', views.edit_sketch, name='edit_sketch'),
    path('delete/<int:id>', views.delete_sketch, name='delete_sketch'),
    path('delete_script/<int:sketch_id>/<int:script_id>', views.delete_script, name='delete_script'),
    path('delete_footage/<int:sketch_id>/<int:footage_id>', views.delete_footage, name='delete_footage'),
    path('delete_final/<int:sketch_id>/<int:final_id>', views.delete_final, name='delete_final'),
]
