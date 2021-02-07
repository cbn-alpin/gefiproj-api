from os import environ, path

import gspread
import gspread_formatting as gsf
from flask import current_app

SHEET_COLUMN_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

DEFAULT_FUNDINGS_HEADER = ['id_p', 'code_p', 'nom_p', 'id_u', 'initiales_u', 'id_f', 'date_arrete_f',
                           'date_limite_solde_f',
                           'montant_arrete_f', 'commentaire_admin_f', 'imputation_f', 'numero_titre_f', 'statut_f',
                           'id_financeur', 'nom_financeur', 'recette_avant', 'recette_a', 'recette_a2', 'recette_a3',
                           'recette_a4', 'recette_a5', 'recette_apres']
DEFAULT_RECEIPTS_HEADER = [
    'annee_recette', 'montant_recette', 'affectation_avant',
    'affectation_a', 'affectation_a2', 'affectation_a3',
    'affectation_a4', 'affectation_a5', 'affectation_apres'
]


def get_google_service_account():
    return gspread.service_account(filename=path.join(environ['TC_ROOT_DIR'], 'config/google-credentials.json'))


def write_fundings_to_google_docs(document_tile, header_column_names, data, shares):
    """
    This method creates a google sheet document to export the funding data betweeen two dates
    and shares it with the given emails

    :param document_tile:
    :param header_column_names: Header column names of the sheet
    :param data: Data to be exported
    :param shares: User mails and permissions to share the created document with
    :return:
    """

    try:
        gc = get_google_service_account()
        google_sheet = gc.create(document_tile)

        for it in shares:
            google_sheet.share(it['email'], perm_type=it['type'], role=it['permission'])

        work_sheet = google_sheet.sheet1
        last_column_letter = SHEET_COLUMN_LETTERS[len(header_column_names) - 1]

        data.insert(0, header_column_names)

        work_sheet.batch_update([{
            'range': f'A1:{last_column_letter}{len(data)}',
            'values': data
        }])

        work_sheet.format(f'A1:{last_column_letter}1', {
            'textFormat': {
                'bold': True
            },
        })

        work_sheet.format(f'A1:{last_column_letter}{len(data)}', {
            'borders': {
                'top': {"style": "SOLID"},
                'right': {"style": "SOLID"},
                'bottom': {"style": "SOLID"},
                'left': {"style": "SOLID"},
            },
            "horizontalAlignment": "LEFT",
            "wrapStrategy": "WRAP"
        })

        # Freeze the first (person) column and the top 2 (project) rows
        work_sheet.freeze(cols=1)

        fmt = gsf.cellFormat(
            textFormat=gsf.textFormat(
                bold=True,
                fontSize=12
            )
        )
        gsf.format_cell_range(work_sheet, 'A1:Z1', fmt)

        return {'title': document_tile, 'lines': len(data), 'url': google_sheet.url}
    except Exception as e:
        current_app.logger.error(e)
        return None


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


def export_receipt_item_from_row_proxy(row_proxy):
    return [
        row_proxy['annee_recette'], row_proxy['montant_recette'], row_proxy['affectation_avant'],
        row_proxy['affectation_a'], row_proxy['affectation_a2'], row_proxy['affectation_a3'],
        row_proxy['affectation_a4'], row_proxy['affectation_a5'], row_proxy['affectation_apres']
    ]
