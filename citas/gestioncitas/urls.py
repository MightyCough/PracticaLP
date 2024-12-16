from rest_framework import routers
from . import views
from django.urls import path,include
from .views import *

router = routers.DefaultRouter()

router.register('clientes',views.ClienteViewSet)
router.register('vendedores',views.VendedorViewSet)
router.register('vehiculos',views.VehiculoViewSet)
router.register('citas',views.CitaViewSet)
router.register('usuarios',views.UsuarioViewSet)

router = routers.DefaultRouter()

router.register('clientes',views.ClienteViewSet)
router.register('vendedores',views.VendedorViewSet)
router.register('vehiculos',views.VehiculoViewSet)
router.register('citas',views.CitaViewSet)
router.register('usuarios',views.UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/',views.CustomAuthToken.as_view(),name='login')
]

