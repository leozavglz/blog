# publicaciones/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Publicacion


class PruebasBlog(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(
            username="usuarioprueba", email="prueba@ejemplo.mx", password="secreto"
        )
        cls.publicacion = Publicacion.objects.create(
            titulo="Un buen título",
            autor=cls.usuario,
            contenido="Un contenido muy interesante.",
        )

    def test_modelo_publicacion(self):
        self.assertEqual(self.publicacion.titulo, "Un buen título")
        self.assertEqual(self.publicacion.autor.username, "usuarioprueba")
        self.assertEqual(self.publicacion.contenido, "Un contenido muy interesante.")
        self.assertEqual(str(self.publicacion), "Un buen título")
        self.assertEqual(self.publicacion.get_absolute_url(), "/publicacion/1/")

    def test_url_existe_en_ubicacion_correcta_vista_lista(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)

    def test_url_existe_en_ubicacion_correcta_vista_detalle(self):
        respuesta = self.client.get("/publicacion/1/")
        self.assertEqual(respuesta.status_code, 200)

    def test_vista_lista(self):
        respuesta = self.client.get(reverse("inicio"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Un contenido muy interesante.")
        self.assertTemplateUsed(respuesta, "inicio.html")

    def test_vista_detalle(self):
        respuesta = self.client.get(
            reverse("publicacion_detalle", kwargs={"pk": self.publicacion.pk})
        )
        sin_respuesta = self.client.get("/publicacion/100000/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(sin_respuesta.status_code, 404)
        self.assertContains(respuesta, "Un buen título")
        self.assertTemplateUsed(respuesta, "publicacion_detalle.html")

    def test_detalle_tiene_enlace_volver(self):
        respuesta = self.client.get(
            reverse("publicacion_detalle", kwargs={"pk": self.publicacion.pk})
        )
        self.assertContains(respuesta, "Volver al inicio")
        self.assertContains(respuesta, f'href="{reverse("inicio")}"')


class PruebasFormularios(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(
            username="leo", password="clave-de-prueba"
        )
        cls.publicacion = Publicacion.objects.create(
            titulo="Original", autor=cls.usuario, contenido="Texto original"
        )

    def test_crear_publicacion_requiere_sesion(self):
        respuesta = self.client.get(reverse("publicacion_nueva"))
        self.assertRedirects(respuesta, "/cuentas/login/?next=/publicacion/nueva/")

    def test_vista_crear_publicacion(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(
            reverse("publicacion_nueva"),
            {"titulo": "Nuevo título", "contenido": "Nuevo texto"},
        )
        self.assertEqual(respuesta.status_code, 302)
        publicacion = Publicacion.objects.get(titulo="Nuevo título")
        self.assertRedirects(respuesta, publicacion.get_absolute_url())
        self.assertEqual(publicacion.contenido, "Nuevo texto")
        self.assertEqual(publicacion.autor, self.usuario)

    def test_vista_crear_publicacion_sin_titulo(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(
            reverse("publicacion_nueva"),
            {"titulo": "", "contenido": "Nuevo texto"},
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Este campo es obligatorio.")
        self.assertEqual(Publicacion.objects.count(), 1)

    def test_vista_editar_publicacion(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(
            reverse("publicacion_editar", kwargs={"pk": self.publicacion.pk}),
            {"titulo": "Editado", "contenido": "Texto editado"},
        )
        self.assertRedirects(respuesta, self.publicacion.get_absolute_url())
        self.publicacion.refresh_from_db()
        self.assertEqual(self.publicacion.titulo, "Editado")

    def test_vista_eliminar_publicacion(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(
            reverse("publicacion_eliminar", kwargs={"pk": self.publicacion.pk})
        )
        self.assertRedirects(respuesta, reverse("inicio"))
        self.assertEqual(Publicacion.objects.count(), 0)

    def test_eliminar_get_pide_confirmacion(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.get(
            reverse("publicacion_eliminar", kwargs={"pk": self.publicacion.pk})
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "¿Seguro que quieres eliminar")
        self.assertEqual(Publicacion.objects.count(), 1)
