import importlib


def upgrade(from_dir, to_dir, from_version, to_version):
    """
    Upgrade data from one version to other version
    :param from_version:
    :param to_version:
    :return:
    """
    upgrade_name = '__'.join([k.replace('.', '_') for k in(from_version, to_version)])
    try:
        converter = importlib.import_module('.utils.convert.c%s' % upgrade_name, package='pystacker').Convert(from_dir, to_dir)
        converter.convert()
    except ImportError as e:
        raise ValueError("Upgrade for %s >> %s not found" % (from_version, to_version))