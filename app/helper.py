import re
import socket
from typing import Tuple


def get_server_ip() -> Tuple[str, str]:
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    return ip_address, host_name


def check_ip(ip_address):
    # Regular expression pattern for 127.0.x.x IP addresses
    pattern = r"^127\.0\.\d{1,3}\.\d{1,3}$"

    # Match the pattern with the provided IP address
    match = re.match(pattern, ip_address)

    # If there is a match and the octets are <= 255
    if match:
        octets = [int(octet) for octet in ip_address.split(".")]
        if all(octet <= 255 for octet in octets):
            return True
    return False
