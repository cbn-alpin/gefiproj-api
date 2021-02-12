import json
from io import StringIO
from os import path, environ

import yaml

environ['TC_ROOT_DIR'] = path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../'))


def create_json_config_file():
    data = {
        "type": "" + environ.get("GS_TYPE"),
        "project_id": "" + environ.get("GS_PROJECT_ID"),
        "private_key_id": "" + environ.get("GS_PRIVATE_KEY_ID"),
        "private_key": "" + environ.get("GS_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": "" + environ.get("GS_CLIENT_EMAIL"),
        "client_id": "" + environ.get("GS_CLIENT_ID"),
        "auth_uri": "" + environ.get("GS_AUTH_URI"),
        "token_uri": "" + environ.get("GS_TOKEN_URI"),
        "auth_provider_x509_cert_url": "" + environ.get("GS_AUTH_PROVIDER"),
        "client_x509_cert_url": "" + environ.get("GS_CLIENT")
    }

    with open('config/google-credentials.json', 'w') as outfile:
        json.dump(data, outfile)
        print('config json created')


def create_yml_config_file():
    data = dict(
        pathes=dict(
            root="{tc_root_dir}",
            config="{tc_root_dir}/config",
            database="{tc_root_dir}/resources/database"
        ),
        database=dict(
            host=environ.get('DATABASE_PROD_IP'),
            port=environ.get('DATABASE_PROD_PORT'),
            name=environ.get('DATABASE_PROD_NAME'),
            user=environ.get('DATABASE_PROD_USER'),
            password=environ.get('DATABASE_PROD_PASSWORD'),
            engine='postgresql'
        ),
        dev_database=dict(
            host=environ.get('DATABASE_DEV_IP'),
            port=environ.get('DATABASE_DEV_PORT'),
            name=environ.get('DATABASE_DEV_NAME'),
            user=environ.get('DATABASE_DEV_USER'),
            password=environ.get('DATABASE_DEV_PASSWORD'),
            engine='postgresql'
        ),
        test_database=dict(
            host=environ.get('DATABASE_TEST_IP'),
            port=environ.get('DATABASE_TEST_PORT'),
            name=environ.get('DATABASE_TEST_NAME'),
            user=environ.get('DATABASE_TEST_USER'),
            password=environ.get('DATABASE_DEV_PASSWORD'),
            engine='postgresql'
        ),
        jwt=dict(
            secret=("" + environ.get('JWT_SECRET') + ""),
            expires_in=("" + environ.get('JWT_EXPIRES_IN') + "")
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

    with open('config/config.yml', 'w', encoding='utf-8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
        print('config yml created')


def get():
    config_file_path = path.join(environ['TC_ROOT_DIR'], 'config/config.yml')
    if not path.exists(config_file_path):
        create_yml_config_file()

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

    return int(jwt_exp_cfg['expires_in'])


# print('DB URI:' + get_engine_uri())
print('LOADDING CONFIG !')
