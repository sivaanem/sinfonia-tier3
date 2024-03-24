import socket

from yarl import URL


def get_localhost_addr() -> URL:
    """Lookup localhost IPv4 address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    lh = URL("http://" + s.getsockname()[0])
    print("localhost", lh)
    s.close()
    return lh
