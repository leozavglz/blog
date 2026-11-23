# publicaciones/views.py
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Publicacion


class VistaInicio(ListView):
    model = Publicacion
    template_name = "inicio.html"
    context_object_name = "publicaciones"


class VistaDetallePublicacion(DetailView):
    model = Publicacion
    template_name = "publicacion_detalle.html"
    context_object_name = "publicacion"


class VistaCrearPublicacion(CreateView):
    model = Publicacion
    template_name = "publicacion_nueva.html"
    fields = ["titulo", "autor", "contenido"]


class VistaEditarPublicacion(UpdateView):
    model = Publicacion
    template_name = "publicacion_editar.html"
    fields = ["titulo", "contenido"]


class VistaEliminarPublicacion(DeleteView):
    model = Publicacion
    template_name = "publicacion_eliminar.html"
    success_url = reverse_lazy("inicio")
