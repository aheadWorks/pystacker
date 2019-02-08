from .utils.config import get_config
from .utils.convert import upgrade as cmd_upgrade
from distutils.version import StrictVersion
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('from_version', type=StrictVersion)
@click.argument('to_version', type=StrictVersion)
def upgrade(from_version, to_version):
    """
    Upgrade data from one version to another version
    """
    cfg = get_config()
    d = cfg['path']['data_dir'] / 'stacks'
    if not click.prompt("Will run upgrade from %s to %s in %s, sure?" % (from_version, to_version, d), type=bool):
        return
    try:
        cmd_upgrade(d, d, str(from_version), str(to_version))
    except ValueError as e:
        click.echo(e, err=True)

if __name__ == '__main__':
    cli()