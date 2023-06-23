import socket


def get_server_ip() -> str:
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    return ip_address
