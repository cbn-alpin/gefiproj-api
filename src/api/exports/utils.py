import json
from datetime import date
from os import environ, path

import gspread
import gspread_formatting as gsf
import requests
from flask import current_app


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
    'Recettes après ',
    'Status'
]

DEFAULT_RECEIPTS_HEADER = [
    'annee_recette', 'montant_recette', 'affectation_avant',
    'affectation_a', 'affectation_a2', 'affectation_a3',
    'affectation_a4', 'affectation_a5', 'affectation_apres'
]

from src.shared.config import create_json_config_file


def get_google_service_account():
    credentials_path = path.join(environ['TC_ROOT_DIR'], 'config/google-credentials.json')
    if not path.exists(credentials_path):
        create_json_config_file()
    return gspread.service_account(filename=path.join(environ['TC_ROOT_DIR'], 'config/google-credentials.json'))


def delete_column_by_index(session: str, spreadsheet_id: str, index: int):
    headers = {'Authorization': f'Bearer {session}'}

    json_data = {
        "requests": [
            {
                "deleteDimension": {
                    "range": {
                        "dimension": "COLUMNS",
                        "startIndex": index
                    }
                }
            },
        ]
    }

    r = requests.post(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate', headers=headers,
                      data=json.dumps(json_data))

    return r.status_code


def conditional_formatting_funding(session: str, spreadsheet_id: str, end_row_index: int):
    headers = {'Authorization': f'Bearer {session}'}

    json_data = {
        "requests": [
            {
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [
                            {
                                "startRowIndex": 1,
                                "endRowIndex": end_row_index,
                                "startColumnIndex": 0,
                                "endColumnIndex": 13
                            }
                        ],
                        "booleanRule": {
                            "format": {
                                "backgroundColor": {
                                    "red": 0.94,
                                    "green": 0.60,
                                    "blue": 0.07
                                }
                            },
                            "condition": {
                                "type": "CUSTOM_FORMULA",
                                "values": [
                                    {
                                        "userEnteredValue": "=IFS(O2 = \"ATR\", true)"
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            {
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [
                            {
                                "startRowIndex": 1,
                                "endRowIndex": end_row_index,
                                "startColumnIndex": 0,
                                "endColumnIndex": 13
                            }
                        ],
                        "booleanRule": {
                            "format": {
                                "backgroundColor": {
                                    "red": 1,
                                    "green": 1,
                                    "blue": 0.05
                                }
                            },
                            "condition": {
                                "type": "CUSTOM_FORMULA",
                                "values": [
                                    {
                                        "userEnteredValue": "=IFS(O2 = \"SOLDE\", true)"
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        ]
    }

    r = requests.post(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate', headers=headers,
                      data=json.dumps(json_data))

    return r.status_code


def basic_formatting_funding(session: str, spreadsheet_id: str, datas):
    headers = {'Authorization': f'Bearer {session}'}

    json_data = {"requests": []}

    withe_color = {
        "red": 1,
        "green": 1,
        "blue": 1,
        "alpha": 0
    }

    orange_color = {
        "red": 0.94,
        "green": 0.60,
        "blue": 0.07
    }

    yellow_color = {
        "red": 1,
        "green": 1,
        "blue": 0.05
    }

    cell_i = 0

    for data in datas:
        # current_app.logger.debug(data[len(data)-1])
        if data[len(data) - 1] == 'ATR':
            cell_format = {
                "repeatCell": {
                    "range": {
                        "startRowIndex": cell_i,
                        "endRowIndex": cell_i + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": orange_color
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                }
            }
        elif data[len(data) - 1] == 'SOLDE':
            cell_format = {
                "repeatCell": {
                    "range": {
                        "startRowIndex": cell_i,
                        "endRowIndex": cell_i + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": yellow_color
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                }
            }
        else:
            cell_format = {
                "repeatCell": {
                    "range": {
                        "startRowIndex": cell_i,
                        "endRowIndex": cell_i + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": withe_color
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                }
            }

        cell_i += 1

        json_data["requests"].append(cell_format)

    r = requests.post(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate', headers=headers,
                      data=json.dumps(json_data))

    return r.status_code

    # current_app.logger.debug(f'Zero : {datas[0][len(datas[0])-1]}')
    # current_app.logger.debug(f'Un   : {datas[1][len(datas[0])-1]}')


def write_fundings_to_google_docs(document_tile, header_column_names, data, shares):
    """
    This method creates a google sheet document to export the funding data betweeen two dates
    and shares it with the given emails

    :param document_tile:
    :param header_column_names: Header column names of the sheet
    :param data: Data to be exported minus statut_f (used for background color)
    :param shares: User mails and permissions to share the created document with
    :return:
    """

    try:
        gc = get_google_service_account()
        google_sheet = gc.create(document_tile)

        # Stop Sharing Document
        # => increase quotas limitation : https://developers.google.com/sheets/api/limits
        # for it in shares:
        #    google_sheet.share(it['email'], perm_type=it['type'], role=it['permission'])
        google_sheet.share(value=None, perm_type='anyone', role='writer')

        work_sheet = google_sheet.sheet1
        # Set name current worksheet
        # google_sheet.worksheet('Projets')

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

        return {'title': document_tile, 'lines': len(data), 'url': google_sheet.url, 'spreadsheetId': google_sheet.id,
                'session': gc.auth.token}

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
            row_proxy['recette_apres'],
            row_proxy['statut_f']
            ]


def export_receipt_item_from_row_proxy(row_proxy):
    return [
        row_proxy['annee_recette'], row_proxy['montant_recette'], row_proxy['affectation_avant'],
        row_proxy['affectation_a'], row_proxy['affectation_a2'], row_proxy['affectation_a3'],
        row_proxy['affectation_a4'], row_proxy['affectation_a5'], row_proxy['affectation_apres']
    ]
