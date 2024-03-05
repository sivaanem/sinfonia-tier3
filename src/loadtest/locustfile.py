from typing import Optional

import toml

from locust import HttpUser, task, constant_throughput
from yarl import URL

from src.loadtest import fake


MATMUL_URL: Optional[str] = 'http://localhost:8000'


class MatMulUser(HttpUser):
    # Maximum request load per second
    wait_time = constant_throughput(1)

    @task
    def matmul(self):
        self.client.post(
            MATMUL_URL,
            json={
                'matrix1': fake.bigmath.square_matrix(n=50),
                'matrix2': fake.bigmath.square_matrix(n=50),
                }
            )
        
    def on_start(self):
        init_resources()
        
        
def init_resources():
    config = toml.load('src/loadtest/.locust.toml')
    
    global MATMUL_URL
    MATMUL_URL = str(URL(config['host']).with_port(config['port']) / 'api' / 'v1'/ 'matmul')
        