import click

from rat.client.viewer import RemoteViewer
from rat.server.stream import ScreenServer


@click.group()
def main():
    """VPS Screen Control System"""
    pass


@main.command()
@click.option('--host', default='0.0.0.0', help='Binding address')
@click.option('--port', default=5555, help='Port to listen on')
def server(host, port):
    """Start the VPS side (Server)"""
    srv = ScreenServer(host, port)
    srv.start()


@main.command()
@click.option('--host', required=True, help='VPS IP address')
@click.option('--port', default=5555, help='VPS Port')
def client(host, port):
    """Start the Local side (Client)"""
    viewer = RemoteViewer(host, port)
    viewer.run()


if __name__ == '__main__':
    main()
