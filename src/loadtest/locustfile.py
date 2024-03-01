from locust import HttpUser, task, constant_throughput

from src.loadtest import fake


class MatMulUser(HttpUser):
    # Maximum request load per second
    wait_time = constant_throughput(100)

    @task
    def matmul(self):
        self.client.post(
            'http://localhost/api/v1/matmul',
            json={
                'matrix1': fake.bigmath.square_matrix(n=100),
                'matrix2': fake.bigmath.square_matrix(n=100),
                }
            )
