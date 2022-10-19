import socket

_storage = {}


def handle_ping(client: socket.socket, _) -> None:
    """Handle the PING command."""
    client.sendall(b"+PONG\r\n")


def handle_set(client: socket.socket, args: list[str]) -> None:
    """Handle the SET command."""

    if len(args) < 2:
        client.sendall(b"-ERR wrong number of arguments for 'set' command\r\n")
        return

    key, value = args[0], args[1]
    _storage[key] = value

    client.sendall(b"+OK\r\n")


def handle_get(client: socket.socket, args: list[str]) -> None:
    """Handle the GET command."""

    if not args:
        client.sendall(b"-ERR wrong number of arguments for 'get' command\r\n")
        return

    key = args[0]
    value = _storage.get(key)

    if value is None:
        client.sendall(b"$-1\r\n")

    client.sendall(f"${len(value)}\r\n{value}\r\n".encode())


COMMAND_HANDLER_MAP = {
    "ping": handle_ping,
    "set": handle_set,
    "get": handle_get,
}
