import click

from allure3_server.__version__ import __version__ as version


@click.group()
@click.help_option('-h', '--help', help="查看帮助信息")
@click.version_option(version, '-v', '--version', help="查看版本信息")
def cli():
    """Allure3 Server CLI"""

@cli.command('start', help="启动 Allure3 Server")
def start():
    from allure3_server.main import Allure3Server
    Allure3Server().start()


if __name__ == '__main__':
    cli()