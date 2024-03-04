import os
import argparse

from locust import HttpUser, task, constant_throughput
from yarl import URL

from src.loadtest import fake


# MATMUL_URL: str = str(URL('http://' + env.host).with_port(env.port) / 'api' / 'v1' / 'matmul')
MATMUL_URL = ''


class MatMulUser(HttpUser):
    # Maximum request load per second
    wait_time = constant_throughput(40)

    @task
    def matmul(self):
        self.client.post(
            MATMUL_URL,
            json={
                'matrix1': fake.bigmath.square_matrix(n=50),
                'matrix2': fake.bigmath.square_matrix(n=50),
                }
            )


def parse_arguments():
    parser = argparse.ArgumentParser(description='Description of your script.')
    
    # Add arguments
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--tspad', type=int)

    return parser.parse_args()


def main():
    args = parse_arguments()
    print('hello')


if __name__ == '__main__':
    main()
