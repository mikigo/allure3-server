from allure3_server.cli import cli
import sys

if __name__ == '__main__':
    sys.argv.extend([
        'start',
        "--host-ip", "10.0.20.202"
    ])
    cli()