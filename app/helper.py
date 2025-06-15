import re
import socket
from typing import Tuple


def get_server_ip() -> Tuple[str, str]:
    host_name = socket.gethostname()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
    except Exception:
        ip_address = socket.gethostbyname(host_name)

    return ip_address, host_name