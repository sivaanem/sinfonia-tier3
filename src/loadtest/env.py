"""Quick dependency injection"""
from typing import Optional, List

import time
import pprint

from pydantic import BaseModel, ConfigDict, Field, validator


class Env(BaseModel):
    # Locust
    locustfile: str
    num_users: int = Field(gt=0)
    run_time: str
    num_workers: Optional[int] = Field(default=None, ge=1)
    expected_workers: Optional[int] = Field(default=None, ge=1)
    
    # CLI
    host: str
    port: int
    tspad_seconds: Optional[int] = Field(default=None, ge=0)
    rps_per_user: List[int]
    
    model_config = ConfigDict(
        extra='ignore',
        case_sensitive=False,
        frozen=True
        )
    
    @validator('rps_per_user', each_item=True)
    def _check_positive_integer_list(cls, v):
        if type(v) != int or v <= 0:
            raise ValueError(f'invalid rps_per_user value {v}')
        return v
    
    def __repr__(self):        
        r = ""
        for k, v in self.dict().items():
            if k != 'model_config':
                r += f" * {k}: {v}\n"
            
        return r[:-1]
    
    def to_locust_args(self) -> List:
        # https://docs.locust.io/en/2.24.0/configuration.html
        a = []
        a.append('--headless')
        a.extend(['--locustfile', self.locustfile])
        a.extend(['--users', self.num_users])
        a.extend(['--run-time', self.run_time])
        
        if self.num_workers:
            a.extend(['--processes', self.num_workers])
            a.extend(['--expect-workers', self.expected_workers])
            
        return a
    
        
# _env: Optional[Env] = None


# def set_env(e: Env) -> Env:
#     global _env
#     assert not _env
#     _env = e
#     return _env
    

# def get_env() -> Env:
#     global _env
#     return _env
