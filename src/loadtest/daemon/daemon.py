from dataclasses import dataclass, asdict

from typing import List, Callable

import threading


# List of of active daemons
_D: List[threading.Thread] = []
_MAX_DAEMON = 10  # Maximum number of concurrent daemons


@dataclass
class Config:
    def to_dict(self):
        return asdict(self)


def start(j: Callable, c: Config) -> int:
    """Start daemon
    
    Args:
        j -- Callable: Daemon job, which is simply a function
        c -- Config: Config 
        
    Return:
        int -- Daemon ID
    """
    if len(_D) >= _MAX_DAEMON:
        raise AssertionError("maximum number of concurrent daemon reached")
    
    t = threading.Thread(target=j, kwargs=c.to_dict(), daemon=True)
    t.start()
    
    _D.append(t)
    
    return len(_D)


def stop(daemon_id: int):
    # As of writing there is no use case for stopping a daemon
    raise NotImplementedError()
