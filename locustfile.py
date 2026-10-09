from locust import HttpUser, task, between
import random
import string
import time

class LaravelApiUser(HttpUser):
    wait_time = between(1, 3)

    @task(4)
    def list_users(self):
        # Validación: Marcar fallo si no responde 200 OK
        with self.client.get("/api/users", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Fallo GET /users: {response.status_code}")

    # Tarea: correos. Ponderación media (3)
    @task(3)
    def list_emails(self):
        with self.client.get("/api/users/emails", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Fallo GET /emails: {response.status_code}")

    @task(2)
    def list_over_twenty(self):
        with self.client.get("/api/users/over-twenty", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Fallo GET /over-twenty: {response.status_code}")

    @task(1)
    def bulk_create_users(self):
        timestamp = str(int(time.time() * 1000))
        random_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
        
        payload = {
            "users": [
                {"name": "Prueba 1", "email": f"usr1_{timestamp}_{random_suffix}@test.com", "birth_date": "1990-05-10", "password": "pwd"},
                {"name": "Prueba 2", "email": f"usr2_{timestamp}_{random_suffix}@test.com", "birth_date": "1995-08-15", "password": "pwd"},
                {"name": "Prueba 3", "email": f"usr3_{timestamp}_{random_suffix}@test.com", "birth_date": "2000-12-20", "password": "pwd"}
            ]
        }

        with self.client.post("/api/users/bulk", json=payload, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Fallo POST bulk: {response.status_code} - {response.text}")