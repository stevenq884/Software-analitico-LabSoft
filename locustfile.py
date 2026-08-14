from locust import HttpUser, task, between

class AnalistaLabSoft(HttpUser):
    # Simula el tiempo de espera entre 1 y 3 segundos (como si el analista estuviera leyendo la pantalla)
    wait_time = between(1, 3)

    @task
    def consultar_muestras(self):
        # Hace una petición GET a la misma ruta que probaste en Postman
        self.client.get("/api/muestras/")