from typing import Optional, Dict, Any

import time
import toml

import locust.stats
from locust import FastHttpUser, events, task, constant_throughput
from locust.runners import WorkerRunner
from yarl import URL

import src.loadtest.daemon as daemon
from src.loadtest import fake


# locust.stats.CSV_STATS_INTERVAL_SEC = 10 # default is 1 second
# locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 10 # Determines how often the data is flushed to disk, default is 10 seconds

_RPS_PER_USER: float = 0
_CONFIG: Dict[str, Any] = dict()
_TIER2_ROOT_URL: Optional[str] = None
_APP_ROOT_URL: Optional[str] = None
_MATMUL_URL: Optional[str] = None


class MatMulUser(FastHttpUser):
    # Maximum request load per second
    # wait_time = constant_throughput(1)
    
    # Number of allowed concurrent requests
    concurrency = 1000000

    @task
    def matmul(self):
        self.client.post(
            _MATMUL_URL,
            json={
                'matrix1': fake.bigmath.square_matrix(n=100),
                'matrix2': fake.bigmath.square_matrix(n=100),
                }
            )

        
@events.test_start.add_listener
def on_startup(environment, **kw):
    environment.stats.use_response_times_cache = True
    MatMulUser.wait_time = _RPS_PER_USER
    
    init_resources()
    
    if isinstance(environment.runner, WorkerRunner):
        return
    
    start_daemons()
    print('Starting master runner')
        
        
def init_resources():
    global _CONFIG
    _CONFIG = toml.load('src/loadtest/.locust.toml')
    
    global _RPS_PER_USER
    _RPS_PER_USER = _CONFIG['rps_per_user']
    MatMulUser.wait_time = constant_throughput(_RPS_PER_USER)
    
    global _APP_ROOT_URL
    _APP_ROOT_URL = _CONFIG['app_root_url']
    
    global _TIER2_ROOT_URL
    _TIER2_ROOT_URL = _CONFIG['tier2_root_url']
    
    global _MATMUL_URL
    _MATMUL_URL = str(URL(_APP_ROOT_URL) / 'matmul')
        
        
def start_daemons():
    # Carbon report daemon
    j = daemon.carbon_report.job
    c = daemon.carbon_report.CarbonReportConfig(
        bts_unix=_CONFIG['bts_unix'],
        num_users=_CONFIG['num_users'],
        rps=_RPS_PER_USER * _CONFIG['num_users'],
        sps=_CONFIG['sps'],
        interval_seconds=_CONFIG['carbon_report_interval_seconds'],
        carbon_url=str(URL(_TIER2_ROOT_URL) / _CONFIG['carbon_url_path']),
        report_root_path=_CONFIG['carbon_report_root_path'],
        )
    daemon.start(j, c)
        