import time
import schedule

from . import daemon


def job():
    bt = int(time.time())

    def _tell_time(bt):
        ct = int(time.time())

    s = schedule.Scheduler()
    s.every(3).seconds.do(_tell_time, bt)

    while True:
        s.run_pending()
        time.sleep(1)


class ClockConfig(daemon.Config):
    """Settings for clock daemon
    
    Fields:
        sps -- int: Number of seconds this clock ticks per 1 second in real-time [default = 1].
    """
    sps: int = 1  # Seconds per seconds
