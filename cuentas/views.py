# cuentas/views.py
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class VistaRegistro(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("inicio")
    template_name = "registration/registro.html"

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        login(self.request, self.object)
        return respuesta
