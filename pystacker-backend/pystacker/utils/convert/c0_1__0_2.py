import pathlib
import yaml
import shortuuid


class Convert:
    def __init__(self, from_dir: pathlib.Path, to_dir: pathlib.Path):
        self.from_dir = from_dir
        self.to_dir = to_dir

    def convert(self):
        for st_path in self.from_dir.glob('*'):
            if st_path.is_dir() :
                try:
                    self.validate(st_path)
                    text = self.convert_yml((st_path / 'docker-compose.yml').read_text(),
                                            (st_path / 'other.yml').read_text())
                    (self.to_dir / st_path.name).mkdir(parents=True, exist_ok=True)
                    (self.to_dir / st_path.name / 'docker-compose.yml').write_text(text)
                    if (self.to_dir / st_path.name / 'other.yml').exists():
                        (self.to_dir / st_path.name / 'other.yml').unlink()
                except ValueError:
                    pass
        return True

    @staticmethod
    def validate(p: pathlib.Path):
        try:
            has_vars = 'vars:' in (p / 'other.yml').read_text()
            has_stacker_node = 'com.stacker' in (p / 'docker-compose.yml').read_text()
            if not has_vars or not has_stacker_node:
                raise FileNotFoundError
        except FileNotFoundError:
            raise ValueError("Stack at %s not in target version format(already upgraded?)" % p)

    @staticmethod
    def convert_yml(*yamls) -> str:
        # Convert stack to new format
        c_yml = {}
        o_yml = {}
        for y in yamls:
            _yml = yaml.load(y)
            if 'services' in _yml:
                c_yml = _yml
            else:
                o_yml = _yml

        yml = c_yml.copy()
        yml['version'] = '3.7'
        yml['x-stacker'] = o_yml
        yml['x-stacker']['uid'] = shortuuid.ShortUUID(alphabet="qwertyuiopasdfghjklzxcvbnm").random(8)
        yml['x-stacker'].update({k.replace('com.stacker.', ''): v for k, v in c_yml['services']['stacker']['labels'].items()})
        del(yml['services']['stacker'])

        return yaml.dump(yml)