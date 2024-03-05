"""Quick and dirty dependency injection"""
from typing import Optional, List

import toml
from pathlib import Path


class Config:
    def __init__(
            self, 
            local: bool,
            config_path: Path | str, 
    ):
        c = toml.load(config_path)
        
        self.cli = c['cli']
        _c = self.cli['local'] if local else self.cli['global']
        self.cli.update(_c)
        del self.cli['local']
        del self.cli['global']
        
        self.locust = c['locust']

    def to_locust_args(self) -> str:
        a = []
        
        if self.locust['headless']:
            a.append('--headless')
            
        a.extend(['--locustfile', self.locust['locustfile']])
        a.extend(['--host', self.locust['host']])
        a.extend(['--users', self.locust['users']])
        
        if 'run-time' in self.locust:
            a.extend(['--run-time', self.locust['run-time']])
        
        if 'processes' in self.locust:
            a.extend(['--processes', self.locust['processes']])
        
        return a
    
    def export_cli_to_toml(self, path: Path | str):
        with open(path, 'w') as f:
            toml.dump(self.cli, f)

    def _repr(self, d):
        r = ""
        for k, v in d.items():
            r += f" * {k}: {v}\n"
        return r[:-1]

    def __repr__(self):        
        return f"CLI:\n{self._repr(self.cli)}\nLocust:\n{self._repr(self.locust)}"    
