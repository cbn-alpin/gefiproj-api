from datetime import date
from os import environ, path

import gspread
import gspread_formatting as gsf
from flask import current_app
from gspread import Worksheet


def export_year_to_str(version: int, value: int):
    if version == 1:
        return str(date.today().year + value)[-2:]
    else:
        return str(date.today().year + value)[-2:]


SHEET_COLUMN_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

DEFAULT_FUNDINGS_HEADER = [
    'Code projet',
    'Nom projet',
    'Financeur',
    'Responsable',
    'Date arrêté ou commande',
    'Date limite de solde',
    'Montant arrêté ou commande',
    'Recettes avant ',
    'Recettes ',
    'Recettes ',
    'Recettes ',
    'Recettes ',
    'Recettes ',
    'Recettes après '
]

DEFAULT_RECEIPTS_HEADER = [
    "Année de recette", "Recettes de l'année", "Montant affecté avant ",
    "Montant affecté à ", "Montant affecté à ", "Montant affecté à ",
    "Montant affecté à ", "Montant affecté à ", "Montant affecté après "
]


def get_google_service_account():
    return gspread.service_account(filename=path.join(environ['TC_ROOT_DIR'], 'config/google-credentials.json'))


def set_cells_format(worksheet: Worksheet):
    requests = [{
        "repeatCell": {
            "range": {
                "startColumnIndex": 5,
                "endColumnIndex": 6,
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {
                        "type": "DATE",
                        "pattern": "dd/mm/yyyy"
                    }
                }
            },
            "fields": "userEnteredFormat.numberFormat"
        }
    }]
    body = {
        'requests': requests
    }
    return worksheet.batch_update(body)


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
            "verticalAlignment": "MIDDLE",
            "wrapStrategy": "WRAP"
        })

        # Set Column as DATE format
        work_sheet.format(f'E1:F{len(data)}', {
            'numberFormat': {
                'type': 'DATE',
                'pattern': 'dd/mm/yyyy'
            }
        })

        # Set Column as DATE format
        # Source : https://developers.google.com/sheets/api/guides/formats#number_format_examples
        work_sheet.format(f'G1:N{len(data)}', {
            'numberFormat': {
                'type': 'CURRENCY',
                'pattern': '[Black][>0]### ### ### €;[Color15][<=0]0 €;[Red]"0 €"'
            },
            "horizontalAlignment": "RIGHT",
        })

        work_sheet.set_basic_filter(name=(f'A:{last_column_letter}'))

        # Freeze the first (person) column and the top 2 (project) rows
        work_sheet.freeze(cols=1)

        fmt = gsf.cellFormat(
            textFormat=gsf.textFormat(
                bold=True,
                fontSize=10
            )
        )
        gsf.format_cell_range(work_sheet, 'A1:Z1', fmt)
        gsf.set_column_width(work_sheet, 'B', 400)
        gsf.set_column_width(work_sheet, 'D', 120)
        gsf.set_column_width(work_sheet, 'E', 200)
        gsf.set_column_width(work_sheet, 'F', 200)

        return {'title': document_tile, 'lines': len(data), 'url': google_sheet.url}
    except Exception as e:
        current_app.logger.error(e)
        return None


def write_rececipts_to_google_docs(document_title, header_column_names, data, shares):
    # TODO: use pivot tables https://developers.google.com/sheets/api/samples/pivot-tables
    try:
        data.insert(0, header_column_names)
        sheet_batch_object = build_sheet_batch(data, data[1][0])
        # return sheet_batch_object
        gc = get_google_service_account()
        google_sheet = gc.create(document_title)

        for it in shares:
            google_sheet.share(it['email'], perm_type=it['type'], role=it['permission'])

        work_sheet = google_sheet.sheet1

        work_sheet.batch_update(sheet_batch_object)

        return {'title': document_title, 'lines': len(data) + len(data) * 4, 'url': google_sheet.url}
    except Exception as e:
        current_app.logger.error(f'write_rececipts_to_google_docs: {e}')
        return None


def build_sheet_batch(data, annee_ref):
    last_column_letter = SHEET_COLUMN_LETTERS[len(data[0]) - 1]
    in_out_ref = data.pop(1)
    table_1_length = len(data)
    batch_objet = []
    additional_table_header = generate_additional_table_header(header_length=len(data[0]) - 1, min_year=data[1][0])

    batch_objet += [
        {'range': f'A1:{last_column_letter}{table_1_length}', 'values': data},
    ]

    additional_table_start = table_1_length + 4
    for i, it in enumerate(data):
        if i == 0:
            continue
        new_table = [
            {
                'range': f'A{additional_table_start}:A{additional_table_start}', 'values': [[f'Bilan {it[0]}']],
            },
            {
                'range': f'A{additional_table_start + 1}:{last_column_letter}{additional_table_start + 4}',
                'values': generate_additional_table_rows(additional_table_header, target_year=it[0])
            }
        ]
        additional_table_start += 6
        batch_objet += new_table

    return batch_objet


def generate_additional_table_header(header_length, min_year):
    header = [f'Avant {min_year}']
    for i in range(header_length):
        if i == 0:
            continue
        header.append(f'{int(min_year) + i}')
    return header


def generate_additional_table_rows(additional_table_header, target_year):
    """
        retourne une liste de 3 lignes => [[], [], []]
        chaque ligne a autant de col que additional_table_header
        les 2 premières lignes correspondant à la col target_year sont vides
    """
    table_rows = [additional_table_header]
    for j in range(3):
        table_rows.append(build_additional_single_row(additional_table_header,
                                                      row_formula=f'=formule de {j}',
                                                      target_year=target_year))

    return table_rows


def build_additional_single_row(header_row, row_formula, target_year):
    row = []
    for i, header in enumerate(header_row):
        if header_row[i] == target_year:
            row.append('')
            continue
        row.append(row_formula)
    return row


def export_funding_item_from_row_proxy(row_proxy):
    date_arrete_f = row_proxy['date_arrete_f']
    date_limite_solde_f = row_proxy['date_limite_solde_f']

    if 'date_arrete_f' in row_proxy and row_proxy['date_arrete_f']:
        date_arrete_f = row_proxy['date_arrete_f'].strftime("%d/%m/%Y")
    if 'date_limite_solde_f' in row_proxy and row_proxy['date_limite_solde_f']:
        date_limite_solde_f = row_proxy['date_limite_solde_f'].strftime("%d/%m/%Y")

    return [row_proxy['code_p'],
            row_proxy['nom_p'],
            row_proxy['nom_financeur'],
            row_proxy['initiales_u'],
            date_arrete_f,
            date_limite_solde_f,
            row_proxy['montant_arrete_f'],
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
