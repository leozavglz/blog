# publicaciones/urls.py
from django.urls import path

from .views import VistaCrearPublicacion, VistaDetallePublicacion, VistaInicio

urlpatterns = [
    path(
        "publicacion/nueva/", VistaCrearPublicacion.as_view(), name="publicacion_nueva"
    ),
    path(
        "publicacion/<int:pk>/",
        VistaDetallePublicacion.as_view(),
        name="publicacion_detalle",
    ),
    path("", VistaInicio.as_view(), name="inicio"),
]
