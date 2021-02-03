from io import StringIO
from os import path, environ

import yaml

environ['TC_ROOT_DIR'] = path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../'))


def write_to_yml():
    data = dict(
        pathes=dict(
            root="{tc_root_dir}",
            config="{tc_root_dir}/config",
            database="{tc_root_dir}/resources/database"
        ),
        database=dict(
            host=environ.get('DATABASE_PROD_IP'),
            port=environ.get('SQL_PORT'),
            name=environ.get('DATABASE_PROD_NAME'),
            user=environ.get('DATABASE_PROD_USER'),
            password=environ.get('DATABASE_PROD_PASSWORD'),
            engine='postgresql'
        ),
        test_database=dict(
            host=environ.get('DATABASE_DEV_IP'),
            port=environ.get('SQL_PORT'),
            name=environ.get('DATABASE_DEV_NAME'),
            user=environ.get('DATABASE_DEV_USER'),
            password=environ.get('DATABASE_DEV_PASSWORD'),
            engine='postgresql'
        ),
        jwt=dict(
            secret=("" + environ.get('JWT_SECRET') + ""),
            expires_in=28800
        ),
        test_token=dict(
            token=("" + environ.get('JWT_TEST_TOKEN') + "")
        ),
        logging=dict(
            pathes=dict(
                config="{tc_root_dir}/config/logging.yml",
                storage="{tc_root_dir}/var/log/api.log"
            )
        )
    )

    print(data)

    with open('config/config.yml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


# TODO: use config like this : https://github.com/kdart/devtest/blob/master/devtest/config.py
# TODO : Mehdi : The link not work anymore
def get():
    # Create config.yml file before export params
    write_to_yml()

    config_file_path = path.join(environ['TC_ROOT_DIR'], 'config/config.yml')
    with open(config_file_path, 'r') as yml_handle:
        yml_content = yml_handle.read()
        # NOTE: most permissive way with regexp
        # yml_content = re.sub(r'{\s*tc_root_dir\s*}', environ['TC_ROOT_DIR'], yml_content)
        yml_content = yml_content.format(tc_root_dir=environ['TC_ROOT_DIR'])
        yml_content_io = StringIO(yml_content)
        config = yaml.safe_load(yml_content_io)
    return config


def get_engine_uri(env):
    db_uri = ''
    cfg = get()

    if env == 'test':
        db_cfg = cfg['test_database']
    else:
        db_cfg = cfg['database']

    user = db_cfg['user']
    password = db_cfg['password']
    host = db_cfg['host']
    port = db_cfg['port']
    name = db_cfg['name']
    db_uri = f'postgresql://{user}:{password}@{host}:{port}/{name}'
    return db_uri


def get_jwt_secret():
    cfg = get()
    jwt_cfg = cfg['jwt']

    return jwt_cfg['secret']


def get_test_token():
    cfg = get()
    return cfg['test_token']['token']


def get_jwt_expirationt():
    cfg = get()
    jwt_exp_cfg = cfg['jwt']

    return jwt_exp_cfg['expires_in']


# print('DB URI:' + get_engine_uri())
print('LOADDING CONFIG !')
