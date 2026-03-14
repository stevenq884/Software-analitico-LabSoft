from django.urls import path
from . import views

urlpatterns = [
    path('lista/',               views.muestras,           name='muestras'),
    path('nueva/',               views.nueva_muestra,      name='nueva_muestra'),
    path('agregar/',             views.agregar_muestra,    name='agregar_muestra'),
    path('editar/<int:id>/',     views.editar_muestra,     name='editar_muestra'),
    path('actualizar/<int:id>/', views.actualizar_muestra, name='actualizar_muestra'),
    path('eliminar/<int:id>/',   views.eliminar_muestra,   name='eliminar_muestra'),
    path('delete/<int:id>/',     views.delete_muestra,     name='delete_muestra'),
]