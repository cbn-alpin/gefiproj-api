from io import StringIO
from os import path, environ

import yaml

environ['TC_ROOT_DIR'] = path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../'))


# TODO: use config like this : https://github.com/kdart/devtest/blob/master/devtest/config.py
def get():
    config_file_path = path.join(environ['TC_ROOT_DIR'], 'config/config.yml')
    with open(config_file_path, 'r') as yml_handle:
        yml_content = yml_handle.read()
        # NOTE: most permissive way with regexp
        # yml_content = re.sub(r'{\s*tc_root_dir\s*}', environ['TC_ROOT_DIR'], yml_content)
        yml_content = yml_content.format(tc_root_dir=environ['TC_ROOT_DIR'])
        yml_content_io = StringIO(yml_content)
        config = yaml.safe_load(yml_content_io)
    return config


def get_engine_uri():
    cfg = get()
    db_cfg = cfg['database']
    engine = db_cfg['engine']
    if (engine == 'sqlite'):
        path = db_cfg['path']
        db_uri = f'{engine}:///{path}'
    elif (engine == 'postgresql'):
        user = db_cfg['user']
        password = db_cfg['password']
        host = db_cfg['host']
        port = db_cfg['port']
        name = db_cfg['name']
        db_uri = f'{engine}://{user}:{password}@{host}:{port}/{name}'
    return db_uri


print('DB URI:' + get_engine_uri())
print('LOADDING CONFIG !')
