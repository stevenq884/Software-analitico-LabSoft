from django.http import HttpResponseForbidden
from django.core.cache import cache


class BloqueoIPMiddleware:
    """
    Middleware que previene ataques de fuerza bruta (ERR-03).
    Bloquea la IP del usuario por 15 minutos después de 5 intentos fallidos.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/login/' and request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR')
            clave_intentos = f'intentos_{ip}'
            intentos = cache.get(clave_intentos, 0)

            if intentos >= 5:
                return HttpResponseForbidden(
                    "Acceso denegado. IP bloqueada por 15 minutos debido a múltiples intentos fallidos."
                )

            response = self.get_response(request)

            # Si el login fue rechazado (código 401/403), se registra el intento fallido
            if response.status_code in (401, 403):
                cache.set(clave_intentos, intentos + 1, timeout=900)  # 15 minutos
            elif response.status_code == 200:
                cache.delete(clave_intentos)  # login exitoso: se reinicia el contador

            return response

        return self.get_response(request)
