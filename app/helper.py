import socket
from typing import Tuple


def get_server_ip() -> Tuple[str, str]:
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    return ip_address, host_name
