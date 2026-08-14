import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from muestras.models import Muestra

@pytest.mark.django_db
def test_creacion_muestra():

    imagen_falsa=SimpleUploadedFile(name="test_image.jpg", content=b"file_content", content_type="image/jpeg")

    muestra=Muestra.objects.create(nombre="Agua Grifo", tipo="Agua potable", foto=imagen_falsa, codigo="A-0001")

    assert muestra.nombre == "Agua Grifo"
    assert muestra.tipo == "Agua potable"
    assert muestra.codigo == "A-0001"
    assert "test_image" in muestra.foto.name
    assert muestra.foto.name.endswith(".jpg")