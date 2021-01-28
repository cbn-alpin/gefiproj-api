# https://www.postgresqltutorial.com/postgresql-python/call-stored-procedures/
# https://gspread.readthedocs.io/en/latest/index.html
# https://medium.com/better-programming/integrating-google-sheets-api-with-python-flask-987d48b7674e

from os import path, environ

import gspread
from flask import current_app, Blueprint, jsonify

from src.shared.entity import Session

resources = Blueprint('exports', __name__)


@resources.route('/api/fundings/export', methods=['POST'])
def get_funding_count():
    current_app.logger.debug('In POST /api/projects')
    session = None
    rows = []
    try:
        session = Session()
        result = session.execute('call get_all_fundings(0)')

        for res in result:
            rows.append(dict(res))
            print(dict(res))
    except Exception as e:
        print('exception!!')
        print(e)
    finally:
        if session is not None:
            session.close()

    if rows:
        gspread_action(rows)

    return jsonify(rows), 200


def gspread_action(data):
    config_file = path.join(environ['TC_ROOT_DIR'], 'config/gefiproj-dev-f5d32032f23a.json')
    gc = gspread.service_account(filename=config_file)

    sh = gc.create('A new spreadsheet')
    wks = sh.sheet1

    # Update a range of cells using the top left corner address
    wks.update('A1', [['Nom', 'Nombre'], ['Financement', data[0].get('funding_count')]])

    # Or update a single cell
    wks.update('B42', "it's down there somewhere, let me take another look.")

    # Format the header
    wks.format('A1:B1', {'textFormat': {'bold': True}})

    # share your sheet
    sh.share('cash.develop223@gmail.com', perm_type='user', role='writer')
