from typing import Optional, Dict, Any

import time
import toml

from locust import FastHttpUser, task, constant_throughput
from yarl import URL

import src.loadtest.daemon as daemon
from src.loadtest import fake


_CONFIG: Dict[str, Any] = dict()
_MATMUL_URL: Optional[str] = 'http://localhost:8000'


class MatMulUser(FastHttpUser):
    # Maximum request load per second
    wait_time = constant_throughput(50)

    @task
    def matmul(self):
        self.client.post(
            _MATMUL_URL,
            json={
                'matrix1': fake.bigmath.square_matrix(n=50),
                'matrix2': fake.bigmath.square_matrix(n=50),
                }
            )
        
    def on_start(self):
        init_resources()
        start_daemons()
        
        
def init_resources():
    global _CONFIG
    _CONFIG = toml.load('src/loadtest/.locust.toml')
    
    global _MATMUL_URL
    _MATMUL_URL = str(URL(_CONFIG['host']).with_port(_CONFIG['port']) / 'api' / 'v1'/ 'matmul')
        
        
def start_daemons():
    # Carbon report daemon
    j = daemon.carbon_report.job
    c = daemon.carbon_report.CarbonReportConfig(
        bts_unix=int(time.time()),
        sps=_CONFIG['sps'],
        interval_seconds=_CONFIG['carbon_report_interval_seconds'],
        carbon_url=URL(_CONFIG['host']) / _CONFIG['carbon_url_path'],
        report_path=_CONFIG['carbon_report_path'],
        )
    daemon.start(j, c)
        