import click

from allure3_server.__version__ import __version__ as version


@click.group()
@click.help_option('-h', '--help', help="查看帮助信息")
@click.version_option(version, '-v', '--version', help="查看版本信息")
def cli():
    """Allure3 Server CLI"""


@cli.command('start', help="启动 Allure3 Server")
@click.option('--results-dir', '--results', default=None, type=click.STRING, help="result 目录")
@click.option('--reports-dir', '--reports', default=None, type=click.STRING, help="report 目录")
@click.option('-h', '--host-ip', default=None, help="服务 IP")
@click.option('-p', '--port', default=None, help="服务端口")
@click.option('-c', '--config', default=None, help="配置文件路径")
def start(
        results_dir,
        reports_dir,
        host_ip,
        port,
        config,
):
    from allure3_server.main import Allure3Server
    from allure3_server.check_env import check_npm_env
    check_npm_env()
    Allure3Server(
        results_dir=results_dir,
        reports_dir=reports_dir,
        host_ip=host_ip,
        port=port,
        config_file=config,
    ).start()


if __name__ == '__main__':
    cli()
