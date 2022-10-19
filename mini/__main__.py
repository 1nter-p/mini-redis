import socket
from threading import Thread

from .cmd_handlers import COMMAND_HANDLER_MAP
from .parser import parse_redis

SERVER_ADDRESS = ("localhost", 6969)


def handle_client(client: socket.socket) -> None:
    """Handle a client."""

    while True:
        # Receive data from the client
        try:
            data = client.recv(1024)
        except ConnectionResetError:
            client.close()
            break

        # Parse the data
        parsed_data = parse_redis(data)
        cmd, args = parsed_data[0].lower(), parsed_data[1:]

        # Handle commands
        if cmd in COMMAND_HANDLER_MAP:
            COMMAND_HANDLER_MAP[cmd](client, args)
            continue

        # If we don't know the command, send an error
        client.sendall(b"-ERR unknown command\r\n")


def main() -> None:
    with socket.create_server(SERVER_ADDRESS) as server:
        # Accept clients and create a thread to handle each one
        while True:
            client, _ = server.accept()
            Thread(target=handle_client, args=(client,)).start()


if __name__ == "__main__":
    main()
