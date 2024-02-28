import requests

from sinfonia_tier3.src.loadtest import fake

requests.post(
    'http://10.42.0.35/api/v1/matmul',
    data={
        'matrix1': fake.bigmath.square_matrix(n=10),
        'matrix2': fake.bigmath.square_matrix(n=10),
        }
    )
