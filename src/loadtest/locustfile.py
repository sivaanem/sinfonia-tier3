from locust import HttpUser, task, constant_throughput

from src.loadtest import fake


class MatMulUser(HttpUser):
    # Maximum request load per second
    wait_time = constant_throughput(40)

    @task
    def matmul(self):
        self.client.post(
<<<<<<< HEAD
            'http://obelix30.cs.umass.edu:30080/api/v1/matmul',
            json={
                'matrix1': fake.bigmath.square_matrix(n=50),
                'matrix2': fake.bigmath.square_matrix(n=50),
=======
            'http://localhost/api/v1/matmul',
            json={
                'matrix1': fake.bigmath.square_matrix(n=100),
                'matrix2': fake.bigmath.square_matrix(n=100),
>>>>>>> b02f7d67c517d01d3cfdc769030beb99507954dc
                }
            )
        