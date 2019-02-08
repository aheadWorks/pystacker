import trafaret
import pathlib
import os
from distutils.version import StrictVersion

from trafaret_config import read_and_validate

PATH = pathlib.Path(__file__).parent.parent.parent
settings_file = os.environ.get('SETTINGS_FILE', 'app.yml')
DEFAULT_CONFIG_PATH = PATH / 'config' / settings_file


CONFIG_TRAFARET = trafaret.Dict({
    trafaret.Key('app'):
        trafaret.Dict({
            'host': trafaret.String(),
            'port': trafaret.Int(),
            'listen':  trafaret.String(),
            'id': trafaret.String(),
            trafaret.Key('min_id', optional=True, default=10): trafaret.Int(),
            trafaret.Key('max_id', optional=True, default=99): trafaret.Int()
        }),
    trafaret.Key('workers'):
        trafaret.List(
            trafaret.Dict({
                'name': trafaret.String(),
                'interval': trafaret.Int()
            })
        ),
    trafaret.Key('docker'):
        trafaret.Dict({
            'hub_username': trafaret.String(),
            'hub_password': trafaret.String()
        }),
    trafaret.Key('path'):
        trafaret.Dict({
            'templates_dir': trafaret.String() >> pathlib.Path,
            'frontend_dir': trafaret.String() >> pathlib.Path,
            'data_dir': trafaret.String() >> pathlib.Path
        }),
    trafaret.Key('data_version', optional=True, default='0.1.0'): trafaret.String() >> StrictVersion
})


def get_config():
    return read_and_validate(DEFAULT_CONFIG_PATH.as_posix(), CONFIG_TRAFARET)


def init_config(app):
    config = get_config()
    app['config'] = config
