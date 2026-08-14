from django.http import HttpResponseForbidden
from django.core.cache import cache

class BloqueoIPMiddleware:
    """
    Middleware en proceso (ERR-03) para prevenir ataques de fuerza bruta.
    Bloquea la IP del usuario por 15 minutos después de 5 intentos fallidos.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/login/' and request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR')
            # Obtener el número de intentos desde la memoria caché
            intentos = cache.get(f'intentos_{ip}', 0)
            
            if intentos >= 5:
                # Bloqueo activo
                return HttpResponseForbidden("Acceso denegado. IP bloqueada por 15 minutos debido a múltiples intentos fallidos.")
            
        response = self.get_response(request)
        return response