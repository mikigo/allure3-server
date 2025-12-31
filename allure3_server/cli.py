import click

from allure3_server.__version__ import __version__ as version


@click.group()
@click.help_option('-h', '--help', help="查看帮助信息")
@click.version_option(version, '-v', '--version', help="查看版本信息")
def cli():
    """Allure3 Server CLI"""


@cli.command('start', help="启动 Allure3 Server")
@click.option('--results-dir', default=None, type=click.STRING, help="服务 IP")
@click.option('--reports-dir', default=None, type=click.STRING, help="服务 IP")
@click.option('--host-ip', default=None, help="服务 IP")
@click.option('--port', default=None, help="服务端口")
@click.option('--allure2', is_flag=True, default=False, help="allure2风格")
def start(
        results_dir,
        reports_dir,
        host_ip,
        port,
        allure2):
    from allure3_server.main import Allure3Server
    Allure3Server(
        results_dir=results_dir,
        reports_dir=reports_dir,
        host_ip=host_ip,
        port=port,
        allure2=allure2,
    ).start()


if __name__ == '__main__':
    cli()
