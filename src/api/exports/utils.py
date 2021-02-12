from datetime import date
from os import environ, path

import gspread
import gspread_formatting as gsf
from flask import current_app


def export_year_to_str(version: int, value: int):
    if version == 1:
        return str(date.today().year + value)[-2:]
    else:
        return str(date.today().year + value)[-2:]


def export_year_to_str_2(value: int, year_v: int):
    return str(year_v + value)[-2:]


SHEET_COLUMN_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

SHEET_COLUMN_LETTERS_TINY = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
SHEET_COLUMN_LETTERS_TINY_2 = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

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
    "Année de recette", "Recettes de l'année", "Montant affecté avant ",
    "Montant affecté à ", "Montant affecté à ", "Montant affecté à ",
    "Montant affecté à ", "Montant affecté à ", "Montant affecté après "
]

ADDITIONNAL_TABLE_ROW_COL_STARTS = ['Montant affecté de ',
                                    'Montant affecté de n vers  ',
                                    'Bilan ']

RECEIPT_TABLES_HEADER = ['Recettes comptables {}', 'Bilan des affectations à {}', 'Total recettes affectées {}',
                         'Dépenses {}', 'Bilan comptable {}', "Bilan d'activité {}"]


def in_year_range(current_year: int, range_year: []):
    for year in range_year:
        if current_year == year:
            return 1

    return 0


def get_all_year_in_result(datats):
    data_year = []
    for data in datats:
        if data[0] != 0:
            data_year.append(data[0])

    return data_year


def get_data_from_year(year: int, datas: []):
    for data in datas:
        if data[0] != 0 and year == data[0]:
            return data


def insert_empty_data_from_year(year: int):
    return [
        year,
        0,  # montant_recette
        0,  # affectation_avant
        0,  # affectation_a
        0,  # affectation_a2
        0,  # affectation_a3
        0,  # affectation_a4
        0,  # affectation_a5
        0,  # affectation_a6
        0  # affectation_apres
    ]


def create_real_data_export(current_year_range: [], year_ref: int, last_year: int, export_data: []):
    new_export_data = [insert_empty_data_from_year(0)]

    for x in range(year_ref, last_year + 1, 1):
        if in_year_range(x, current_year_range) == 0:
            new_export_data.append(insert_empty_data_from_year(x))
        else:
            new_export_data.append(get_data_from_year(x, export_data))

    return new_export_data


def get_max_year(year_ref: int, result):
    count = 0
    for res in result:
        count += 1

    return year_ref + count - 1


def generate_header_first_tab_0(year_ref: int):
    header_title = ['Année de recette', 'Recettes de l\'année',
                    f'Montant affecté avant {export_year_to_str_2(year_ref, 0)}']
    i = 0
    for x in range(year_ref, year_ref + 6, 1):
        header_title.append(f'Montant affecté à {export_year_to_str_2(year_ref, i)}')
        i += 1

    header_title.append(f'Montant affecté après {export_year_to_str_2(year_ref + 5, 0)}')

    return header_title


def generate_header_other_tab(year_ref: int):
    header_title = [
        'Année n',
        f'Avant {export_year_to_str_2(year_ref, 0)}'
    ]

    i = 0
    for x in range(year_ref, year_ref + 6, 1):
        header_title.append(f'{export_year_to_str_2(year_ref, i)}')
        i += 1

    header_title.append(f'Après {export_year_to_str_2(year_ref, i)}')
    header_title.append('Total')

    return header_title


def generate_header_first_tab_1(year_ref: int, last_year: int):
    header_title = ['Année de recette', 'Recettes comptables',
                    f'Montant affecté avant {export_year_to_str_2(year_ref, 0)}']
    i = 0
    for x in range(year_ref, last_year + 1, 1):
        header_title.append(f'Montant affecté à {export_year_to_str_2(year_ref, i)}')
        i += 1

    header_title.append(f'Montant affecté après {export_year_to_str_2(last_year, 0)}')

    return header_title


def get_google_service_account():
    return gspread.service_account(filename=path.join(environ['TC_ROOT_DIR'], 'config/google-credentials.json'))


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


def write_rececipts_to_google_docs(document_title, header_column_names, data):
    # TODO: use pivot tables https://developers.google.com/sheets/api/samples/pivot-tables
    try:
        data.insert(0, header_column_names)
        sheet_batch_object = build_sheet_batch(data, data[1][0])

        gc = get_google_service_account()
        google_sheet = gc.create(document_title)

        google_sheet.share(value=None, perm_type='anyone', role='writer')

        work_sheet = google_sheet.sheet1

        work_sheet.batch_update(sheet_batch_object)

        return {'title': document_title, 'lines': len(data) + len(data) * 4, 'url': google_sheet.url,
                'spreadsheetId': google_sheet.id, 'session': gc.auth.token}

    except Exception as e:
        current_app.logger.error(f'write_rececipts_to_google_docs: {e}')
        return None


def generate_additional_table_header(header_length, min_year):
    """
    On génère l'entête des tableaux complementaires pour l'utiliser dans toutes les tableaux qui seront générés
    :param header_length: Longueur de la
    :param min_year: Première année du tableau
    :return: Liste de string qui represente l'entête
    """
    header = ['Année n', f'Avant {min_year}']
    for i in range(header_length):
        if i == 0 or i == 1:
            continue
        header.append(f'{int(min_year) + i}')

    return header


def build_sheet_batch(data_table, annee_ref):
    """
    Construit tous les tableaux qui doivent être exportés pour garantir l'insertion en une unique opération
    :param data_table:
    :param annee_ref:
    :return:
    """
    last_column_letter = SHEET_COLUMN_LETTERS[len(data_table[0]) - 1]
    in_out_ref = data_table.pop(1)  # ligne d'entrée sortie, celle qui commence à 0
    table_1_length = len(data_table)
    additional_table_header = generate_additional_table_header(header_length=len(data_table[0]) - 1,
                                                               min_year=data_table[1][0])
    batch_objet = []

    # contruction du tableau principal
    batch_objet += [
        {'range': f'A1:{last_column_letter}{table_1_length}', 'values': data_table},
    ]

    # construction des tableaux annexes
    additional_table_start = table_1_length + 4
    receipt_start_col = SHEET_COLUMN_LETTERS[len(data_table[0]) + 1]
    receipt_end_col = SHEET_COLUMN_LETTERS[len(data_table[0]) + 6]
    for i, row in enumerate(data_table):
        if i == 0:
            # sauter la ligne du header
            continue
        new_table = [
            {
                # titre du tableau complementaire
                'range': f'A{additional_table_start}:A{additional_table_start}',
                'values': [[f'Bilan {row[0]}']],
            },
            {
                # Tableau complementaire
                'range': f'A{additional_table_start + 1}:{last_column_letter}{additional_table_start + 4}',
                'values': generate_additional_table_rows(additional_table_header, target_year=row[0])
            },
            {
                # Tableau des dépenses et des recettes
                'range': f'{receipt_start_col}{additional_table_start + 1}'
                         f':{receipt_end_col}{additional_table_start + 2}',
                'values': generate_receipt_tables_batch()
            }
        ]
        additional_table_start += 6
        batch_objet += new_table

    return batch_objet


def generate_additional_table_rows(additional_table_header, target_year):
    """
        retourne une liste de 3 lignes => [[], [], []]
        chaque ligne a autant de col que additional_table_header
        les 2 premières lignes correspondant à la col target_year sont vides
    """
    table_rows = [additional_table_header]
    for j in range(3):
        table_rows.append(build_additional_single_row(additional_table_header,
                                                      row_formula=f'=formule de row {j}',
                                                      target_year=target_year, row=j))

    return table_rows


def build_additional_single_row(header_row, row_formula, target_year, row):
    """
    Construit une des 3 lignes des tableaux complémentaires.
    Doit laisser les 2 premières colonnes de l'année de référence vides
    :param header_row: Header des tableaux complémentaires
    :param row_formula: Formule à appliquer
    :param target_year: Année cible
    :param row: Ligne du tableau complementaire
    :return: liste de chaines de
    """
    row = [ADDITIONNAL_TABLE_ROW_COL_STARTS[row]]
    for i, header in enumerate(header_row):
        if header == target_year and row != 2:
            row.append('')
            continue
        row.append(row_formula)
    return row


def generate_receipt_tables_batch():
    """
    Génère les linges recettes présents à droite des tableaux complémentaires
    :return: Une liste de string [[]]
    """
    row = []
    for i, col in enumerate(RECEIPT_TABLES_HEADER):
        row.append(i)

    return [RECEIPT_TABLES_HEADER, row]


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
        row_proxy['affectation_a4'], row_proxy['affectation_a5'],row_proxy['affectation_a6']
        , row_proxy['affectation_apres']
    ]
