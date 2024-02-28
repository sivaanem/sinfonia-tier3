from locust import HttpUser, task, constant_throughput

from src.loadtest import fake


class MatMulUser(HttpUser):
    # Maximum request load per second
    wait_time = constant_throughput(100)

    @task
    def matmul(self):
        self.client.post(
            'http://10.42.0.35/api/v1/matmul',
            data={
                'matrix1': fake.bigmath.square_matrix(n=10),
                'matrix2': fake.bigmath.square_matrix(n=10),
                }
            )
