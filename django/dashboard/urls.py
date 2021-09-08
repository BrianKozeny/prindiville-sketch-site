from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sketch/', views.showsketch, name='upload'),
    path('edit/<int:id>', views.edit_sketch, name='edit_sketch'),
    path('delete/<int:id>', views.delete_sketch, name='delete_sketch'),
]
