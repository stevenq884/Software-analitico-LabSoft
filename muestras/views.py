from django.shortcuts import render, redirect, get_object_or_404
from .models import Muestra
from .serializer import MuestraSerializer
from rest_framework import viewsets

class MuestraViewSet(viewsets.ModelViewSet):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer



def generar_codigo(tipo):
    if 'agua' in tipo.lower():
        prefijo = 'A'
    elif 'alimento' in tipo.lower() or 'bebida' in tipo.lower() or 'superficie' in tipo.lower():
        prefijo = 'AL'
    else:
        prefijo = 'AM'

    # Obtiene todos los números ya usados para ese prefijo
    codigos_existentes = Muestra.objects.filter(
        codigo__startswith=prefijo + '-'
    ).values_list('codigo', flat=True)

    numeros_usados = set()
    for codigo in codigos_existentes:
        try:
            num = int(codigo.split('-')[-1])
            numeros_usados.add(num)
        except ValueError:
            pass

    # Busca el primer número disponible desde 1
    contador = 1
    while contador in numeros_usados:
        contador += 1

    return f"{prefijo}-{str(contador).zfill(4)}"

def muestras(request):
    return render(request, 'muestras/nueva_muestra.html')


def nueva_muestra(request):
    get_muestra = Muestra.objects.all()
    data = {'get_muestra': get_muestra}
    return render(request, 'muestras/nueva_muestra.html', data)


def agregar_muestra(request):
    if request.method == 'POST':
        tipo   = request.POST.get('tipo')
        nombre = request.POST.get('nombre')
        foto   = request.FILES.get('foto')
        codigo = generar_codigo(tipo)
        Muestra.objects.create(nombre=nombre, codigo=codigo, tipo=tipo, foto=foto)
        return redirect('nueva_muestra')
    return render(request, 'muestras/agregar_muestra.html')


def editar_muestra(request, id):
    muestra = get_object_or_404(Muestra, id=id)
    return render(request, 'muestras/editar_muestra.html', {'muestra': muestra})


def actualizar_muestra(request, id):
    muestra = get_object_or_404(Muestra, id=id)
    if request.method == 'POST':
        nuevo_tipo = request.POST.get('tipo')

        if nuevo_tipo != muestra.tipo:
            # Libera el código actual antes de generar el nuevo
            codigo_viejo = muestra.codigo
            muestra.codigo = 'TEMP'
            muestra.save()

            muestra.codigo = generar_codigo(nuevo_tipo)

            # Si el prefijo es el mismo, devuelve el código original
            # para no desperdiciar el consecutivo
            prefijo_viejo = codigo_viejo.split('-')[0]
            prefijo_nuevo = muestra.codigo.split('-')[0]
            if prefijo_viejo == prefijo_nuevo:
                muestra.codigo = codigo_viejo

        muestra.nombre = request.POST.get('nombre')
        muestra.tipo   = nuevo_tipo
        if request.FILES.get('foto'):
            muestra.foto = request.FILES.get('foto')
        muestra.save()
        return redirect('nueva_muestra')
    return redirect('editar_muestra', id=id)


def eliminar_muestra(request, id):
    muestra = get_object_or_404(Muestra, id=id)
    return render(request, 'muestras/confirmar_eliminar.html', {'muestra': muestra})


def delete_muestra(request, id):
    muestra = get_object_or_404(Muestra, id=id)
    if request.method == 'POST':
        muestra.delete()
        return redirect('nueva_muestra')
    return redirect('eliminar_muestra', id=id)