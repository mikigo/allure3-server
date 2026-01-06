from allure3_server.cli import cli
import sys
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sys.argv.extend([
        'start',
        "--host-ip", "10.0.20.202"
    ])
    cli()