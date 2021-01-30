# https://www.postgresqltutorial.com/postgresql-python/call-stored-procedures/
# https://gspread.readthedocs.io/en/latest/index.html
# https://medium.com/better-programming/integrating-google-sheets-api-with-python-flask-987d48b7674e
from datetime import datetime
from os import path, environ

import gspread
from flask import current_app, Blueprint, jsonify, request

from src.shared.entity import Session

resources = Blueprint('exports', __name__)


@resources.route('/api/fundings/export/count', methods=['POST'])
def get_funding_count():
    current_app.logger.debug('In POST /api/projects')
    session = None
    rows = []
    try:
        session = Session()
        result = session.execute('call get_all_fundings(0)')

        for res in result:
            rows.append(dict(res))

    except Exception as e:
        print('exception!!')
        current_app.logger.error(e)
        return '', 500
    finally:
        if session is not None:
            session.close()

    if rows:
        gspread_action(rows)

    return jsonify(rows), 200


@resources.route('/api/fundings/export', methods=['POST'])
def export_fundings():
    current_app.logger.debug('In POST /api/projects')

    post_data = request.get_json()
    if not post_data or 'annee' not in post_data:
        return jsonify(), 400

    annee = post_data['annee']
    # validate posted annee

    session = None
    rows = []

    try:
        session = Session()
        result = session.execute("select * from test(:annee)", {'annee': annee})

        for res in result:
            rows.append(export_funding_item_from_row_proxy(res))
    except Exception as e:
        print(e)
        current_app.logger.error(e)
        return 'fatal server error', 500
    finally:
        if session is not None:
            session.close()

    if rows:
        write_to_google_docs(rows, annee,
                             ['cash.develop223@gmail.com', 'hanh16101998@gmail.com', 'tempor.05@gmail.com'])

    return jsonify({'message': 'successfully created google sheet'}), 200  # TODO: Return the url of created doc


def export_funding_item_from_row_proxy(row_proxy):
    date_arrete_f = row_proxy['date_arrete_f']
    date_limite_solde_f = row_proxy['date_limite_solde_f']

    if 'date_arrete_f' in row_proxy and row_proxy['date_arrete_f']:
        date_arrete_f = row_proxy['date_arrete_f'].strftime("%d/%m/%Y")
    if 'date_limite_solde_f' in row_proxy and row_proxy['date_limite_solde_f']:
        date_limite_solde_f = row_proxy['date_limite_solde_f'].strftime("%d/%m/%Y")

    return [row_proxy['id_p'],
            row_proxy['code_p'],
            row_proxy['nom_p'],
            row_proxy['id_u'],
            row_proxy['initiales_u'],
            row_proxy['id_f'],
            date_arrete_f,
            date_limite_solde_f,
            row_proxy['montant_arrete_f'],
            row_proxy['commentaire_admin_f'],
            row_proxy['imputation_f'],
            row_proxy['numero_titre_f'],
            row_proxy['statut_f'],
            row_proxy['id_financeur'],
            row_proxy['nom_financeur'],
            row_proxy['recette_avant'],
            row_proxy['recette_a'],
            row_proxy['recette_a2'],
            row_proxy['recette_a3'],
            row_proxy['recette_a4'],
            row_proxy['recette_a5'],
            row_proxy['recette_apres']
            ]


def get_google_cloud():
    config_file = path.join(environ['TC_ROOT_DIR'], 'config/gefiproj-dev-f5d32032f23a.json')
    return gspread.service_account(filename=config_file)


def gspread_action(data):
    gc = get_google_cloud()

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


def write_to_google_docs(data, year, shares):
    gc = get_google_cloud()
    google_sheet = gc.create(f'Export financement année {year} - {datetime.today().strftime("%d/%m/%Y %H:%M:%S")}')

    for email in shares:
        google_sheet.share(email, perm_type='user', role='writer')

    work_sheet = google_sheet.sheet1

    work_sheet.insert_row(['id_p',
                           'code_p',
                           'nom_p',
                           'id_u',
                           'initiales_u',
                           'id_f',
                           'date_arrete_f',
                           'date_limite_solde_f',
                           'montant_arrete_f',
                           'commentaire_admin_f',
                           'imputation_f',
                           'numero_titre_f',
                           'statut_f',
                           'id_financeur',
                           'nom_financeur',
                           'recette_avant',
                           'recette_a',
                           'recette_a2',
                           'recette_a3',
                           'recette_a4',
                           'recette_a5',
                           'recette_apres'], 1)
    work_sheet.format('A1:W1', {'textFormat': {'bold': True}, "horizontalAlignment": "CENTER", })

    for i, d in enumerate(data, start=2):
        work_sheet.insert_row(d, i)
