import requests
import json

# Deleting last column (status) for fundings export
from sqlalchemy import false, true


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


# conditional formatting funding
# finally not used
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


# Formatting table for fundings export
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


def get_title_button_left_tabs(line: int, celle: str):
    return [
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=CONCATENATE(\"Montant affecté de \", MID(" + celle + ",3,2), \" vers n\")"
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line + 1,
                    "endRowIndex": line + 2,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=CONCATENATE(\"Montant affecté de n vers \", MID(" + celle + ",3,2))"
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line + 2,
                    "endRowIndex": line + 3,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=CONCATENATE(\"Bilan \", MID(" + celle + ",3,2), \"/n\")"
                    }
                },
                "fields": "userEnteredValue"
            }
        }
    ]


def get_title_button_tabs(line: int):
    return [
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 1,
                    "endColumnIndex": 10
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=CONCATENATE(\"Avant \", MID(A$2,3,2))"
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=MID(A$2,3,2)"
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 3,
                    "endColumnIndex": 4
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=MID(A$2+1,3,2)"
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 4,
                    "endColumnIndex": 5
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=MID(A$2+2,3,2)"
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 5,
                    "endColumnIndex": 6
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=MID(A$2+3,3,2)"
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 6,
                    "endColumnIndex": 7
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=MID(A$2+4,3,2)"
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 7,
                    "endColumnIndex": 8
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=MID(A$2+5,3,2)"
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 8,
                    "endColumnIndex": 9
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=CONCATENATE(\"Après \", MID(A$2+5,3,2))"
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 9,
                    "endColumnIndex": 10
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": "=\"Total\""
                    }
                },
                "fields": "userEnteredValue"
            }
        }
    ]


def get_formatting_button_left_tabs(line: int):
    return [
        {
            "updateDimensionProperties": {
                "range": {
                    "dimension": "COLUMNS",
                    "startIndex": 11,
                    "endIndex": 17
                },
                "properties": {
                    "pixelSize": 160
                },
                "fields": "pixelSize"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1,
                    "startColumnIndex": 11,
                    "endColumnIndex": 17
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "RIGHT",
                        "verticalAlignment": "MIDDLE",
                        "textFormat": {
                            "fontSize": 11,
                            "bold": "true"
                        },
                        "numberFormat": {
                            "type": "CURRENCY",
                            "pattern": "[Black][>0]### ### ### €;[Color15][<=0]0 €;[Red]\"0 €\""
                        }
                    }
                },
                "fields": "userEnteredFormat.numberFormat"
            }
        },
        {
            "updateBorders": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 2,
                    "startColumnIndex": 11,
                    "endColumnIndex": 17
                },
                "top": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                },
                "bottom": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                },
                "innerHorizontal": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                },
                "innerVertical": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                }
            }
        },
        {
            "updateBorders": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 2,
                    "startColumnIndex": 17,
                    "endColumnIndex": 1
                },
                "innerVertical": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                }
            }
        },
    ]


def get_formatting_button_tabs(line: int):
    return [
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line,
                    "endRowIndex": line + 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "LEFT",
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "WRAP",
                        "textFormat": {
                            "fontSize": 12,
                            "bold": "true"
                        }
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            },
        },
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": line + 1,
                    "endRowIndex": line + 2
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "LEFT",
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "WRAP",
                        "textFormat": {
                            "fontSize": 11,
                            "bold": "true"
                        }
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            }
        },
        {
            "updateBorders": {
                "range": {
                    "startRowIndex": line + 1,
                    "endRowIndex": line + 5,
                    "endColumnIndex": 10
                },
                "top": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                },
                "bottom": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                },
                "innerHorizontal": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                },
                "innerVertical": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                }
            }
        },
        {
            "updateBorders": {
                "range": {
                    "startRowIndex": line + 1,
                    "endRowIndex": line + 5,
                    "endColumnIndex": 11
                },
                "innerVertical": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                }
            }
        },
    ]


def generate_style_all_tabs(max_rows_first_tab: int):
    """
            params : length ligne table
            params : current first year off tabs
        """
    json_data = []
    k = 0
    for x in range(0, max_rows_first_tab - 1):
        json_data.append(get_formatting_button_tabs(max_rows_first_tab + 3 + k)[0])
        json_data.append(get_formatting_button_tabs(max_rows_first_tab + 3 + k)[1])
        json_data.append(get_formatting_button_tabs(max_rows_first_tab + 3 + k)[2])

        json_data.append(get_formatting_button_left_tabs(max_rows_first_tab + 4 + k)[0])
        json_data.append(get_formatting_button_left_tabs(max_rows_first_tab + 4 + k)[1])
        json_data.append(get_formatting_button_left_tabs(max_rows_first_tab + 4 + k)[2])

        json_data.append(get_title_button_tabs(max_rows_first_tab + 4 + k)[0])
        json_data.append(get_title_button_tabs(max_rows_first_tab + 4 + k)[1])
        json_data.append(get_title_button_tabs(max_rows_first_tab + 4 + k)[2])
        json_data.append(get_title_button_tabs(max_rows_first_tab + 4 + k)[3])
        json_data.append(get_title_button_tabs(max_rows_first_tab + 4 + k)[4])
        json_data.append(get_title_button_tabs(max_rows_first_tab + 4 + k)[5])
        json_data.append(get_title_button_tabs(max_rows_first_tab + 4 + k)[6])
        json_data.append(get_title_button_tabs(max_rows_first_tab + 4 + k)[7])
        json_data.append(get_title_button_tabs(max_rows_first_tab + 4 + k)[8])

        json_data.append(get_title_button_left_tabs(max_rows_first_tab + 5 + k, 'A$2')[0])
        json_data.append(get_title_button_left_tabs(max_rows_first_tab + 5 + k, 'A$2')[1])
        json_data.append(get_title_button_left_tabs(max_rows_first_tab + 5 + k, 'A$2')[2])
        k = k + 6

    return json_data


def get_one_query_value_first(letter: [], y_cell: int, cel1: int, cel2: int, ligne_max: int, current_year: int):
    """
        params : letter == column
        params : (letter[0], y_cell) : position to update
        params : Cellule du Titre du Bilan => YY année
        params : Cellule du Titre du tableau de l'année => YY année
        params : max ligne
        params : current first year off table
        Exemple in for Bilan 2010 in H$31 : =IF(REGEXMATCH(MID($A$31,9,2), H$32), "", INDEX(query($A$1:$J$9 ,"select I where A=2019"),2,0))
    """
    return {
               "repeatCell": {
                   "range": {
                       "startRowIndex": y_cell - 1,
                       "endRowIndex": y_cell,
                       "startColumnIndex": letter[1] - 1,
                       "endColumnIndex": letter[1]
                   },
                   "cell": {
                       "userEnteredFormat": {
                           "horizontalAlignment": "RIGHT",
                           "verticalAlignment": "MIDDLE",
                           "textFormat": {
                               "fontSize": 11,
                               "bold": "true"
                           },
                           "numberFormat": {
                               "type": "CURRENCY",
                               "pattern": "[Black][>0]### ### ### €;[Color15][<=0]0 €;[Red]\"0 €\""
                           }
                       },
                       "userEnteredValue": {
                           "formulaValue": "=IF(REGEXMATCH(MID($A$" + str(cel1) + ", 9, 2), " + letter[0] + "$" + str(
                               cel2) + "), \"\", INDEX(query($A$1:$J$" + str(ligne_max) + ", \"select " + letter[
                                               2] + " where A=" + str(
                               current_year) + "\"), 2, 0)) "
                       }
                   },
                   "fields": "userEnteredValue,userEnteredFormat.numberFormat"
               },
           },


def get_one_query_value_seconde(letter: [], y_cell: int, cel1: int, cel2: int, current_year: int):
    """
        params : letter == column
        params : (letter[0], y_cell) : position to update
        params : Cellule du Titre du Bilan => YY année
        params : Cellule du Titre du tableau de l'année => YY année
        params : max ligne
        params : current first year off table
        Exemple in for Bilan 2010 in H$31 : =IF(REGEXMATCH(MID($A$31,9,2), H$32), "", INDEX(query($A$1:$J$9 ,"select I where A=2019"),2,0))
    """
    return {
               "repeatCell": {
                   "range": {
                       "startRowIndex": y_cell - 1,
                       "endRowIndex": y_cell,
                       "startColumnIndex": letter[1] - 1,
                       "endColumnIndex": letter[1]
                   },
                   "cell": {
                       "userEnteredFormat": {
                           "horizontalAlignment": "RIGHT",
                           "verticalAlignment": "MIDDLE",
                           "textFormat": {
                               "fontSize": 11,
                               "bold": "true"
                           },
                           "numberFormat": {
                               "type": "CURRENCY",
                               "pattern": "[Black][>0]### ### ### €;[Color15][<=0]0 €;[Red]\"0 €\""
                           }
                       },
                       "userEnteredValue": {
                           "formulaValue": "=IF(REGEXMATCH(MID($A$" + str(cel1-1) + ", 9, 2), " + letter[0] + "$" + str(
                               cel2-1) + "), \"\", INDEX(query($A$1:$J$9 ,\"select G where A="+str(current_year)+"\"),2,0))"
                       }
                   },
                   "fields": "userEnteredValue,userEnteredFormat.numberFormat"
               },
           },


def get_one_query_total_value(y_cell: int):
    return {
               "repeatCell": {
                   "range": {
                       "startRowIndex": y_cell - 1,
                       "endRowIndex": y_cell,
                       "startColumnIndex": 9,
                       "endColumnIndex": 10
                   },
                   "cell": {
                       "userEnteredFormat": {
                           "horizontalAlignment": "RIGHT",
                           "verticalAlignment": "MIDDLE",
                           "textFormat": {
                               "fontSize": 11,
                               "bold": "true"
                           },
                           "numberFormat": {
                               "type": "CURRENCY",
                               "pattern": "[Black][>0]### ### ### €;[Color15][<=0]0 €;[Red]\"0 €\""
                           }
                       },
                       "userEnteredValue": {
                           "formulaValue": "=SUM(B" + str(y_cell) + ":I" + str(y_cell) + ")"
                       }
                   },
                   "fields": "userEnteredValue,userEnteredFormat.numberFormat"
               }
           },


def generate_all_value_for_letter(letter: [], max_rows_first_tab: int, first_year: int):
    """
        params : letter == column
        params : length ligne table
        params : current first year off tabs
    """
    json_data = []
    k = 0
    for x in range(0, max_rows_first_tab - 1):
        json_data.append(get_one_query_value_first(letter, max_rows_first_tab + 6 + k, max_rows_first_tab + 4 + k,
                                                   max_rows_first_tab + 5 + k, max_rows_first_tab, first_year + x))
        json_data.append(get_one_query_total_value(max_rows_first_tab + 6 + k))

        json_data.append(get_one_query_value_seconde(letter, max_rows_first_tab + 6 + k + 1, max_rows_first_tab + 4 + k + 1,
                                                     max_rows_first_tab + 5 + k + 1, first_year + x))
        json_data.append(get_one_query_total_value(max_rows_first_tab + 6 + k + 1))
        k = k + 6

    return json_data


# Formatting first table for receipt export
def basic_formatting_receipt(session: str, spreadsheet_id: str, max_rows_first_tab: int):
    headers = {'Authorization': f'Bearer {session}'}

    json_data = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": 0,
                        "endRowIndex": 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "LEFT",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "WRAP",
                            "textFormat": {
                                "fontSize": 11,
                                "bold": "true"
                            }
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                }
            },
            {
                "updateBorders": {
                    "range": {
                        "startRowIndex": 0,
                        "endRowIndex": max_rows_first_tab,
                        "endColumnIndex": 10
                    },
                    "top": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {
                            "red": 0,
                            "green": 0,
                            "blue": 0
                        }
                    },
                    "bottom": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {
                            "red": 0,
                            "green": 0,
                            "blue": 0
                        }
                    },
                    "innerHorizontal": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {
                            "red": 0,
                            "green": 0,
                            "blue": 0
                        }
                    },
                    "innerVertical": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {
                            "red": 0,
                            "green": 0,
                            "blue": 0
                        }
                    }
                }
            },
            {
                "updateBorders": {
                    "range": {
                        "startRowIndex": 0,
                        "endRowIndex": max_rows_first_tab,
                        "endColumnIndex": 11
                    },
                    "innerVertical": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {
                            "red": 0,
                            "green": 0,
                            "blue": 0
                        }
                    }
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 16
                    },
                    "properties": {
                        "pixelSize": 160
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": 0,
                        "endRowIndex": max_rows_first_tab,
                        "startColumnIndex": 1,
                        "endColumnIndex": 10
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "RIGHT",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "WRAP",
                            "numberFormat": {
                                "type": "CURRENCY",
                                "pattern": "[Black][>0]### ### ### €;[Color15][<=0]0 €;[Red]\"0 €\""
                            }
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat"
                }
            },
            {
                "setBasicFilter": {
                    "filter": {
                        "range": {
                            "startRowIndex": 0,
                            "endRowIndex": max_rows_first_tab,
                            "endColumnIndex": 10
                        }
                    }
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": max_rows_first_tab,
                        "endRowIndex": max_rows_first_tab + 1,
                        "startColumnIndex": 1,
                        "endColumnIndex": 10
                    },
                    "cell": {
                        "userEnteredValue": {
                            "formulaValue": "=SUM(B2:B9)"
                        }
                    },
                    "fields": "userEnteredValue"
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": max_rows_first_tab,
                        "endRowIndex": max_rows_first_tab + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "RIGHT",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "WRAP",
                            "textFormat": {
                                "fontSize": 11,
                                "bold": "true"
                            }
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                }
            },
            generate_style_all_tabs(max_rows_first_tab),
            generate_all_value_for_letter(['B', 2, 'C'], max_rows_first_tab, 2016),
            generate_all_value_for_letter(['C', 3, 'D'], max_rows_first_tab, 2016),
            generate_all_value_for_letter(['D', 4, 'E'], max_rows_first_tab, 2016),
            generate_all_value_for_letter(['E', 5, 'F'], max_rows_first_tab, 2016),
            generate_all_value_for_letter(['F', 6, 'G'], max_rows_first_tab, 2016),
            generate_all_value_for_letter(['G', 7, 'H'], max_rows_first_tab, 2016),
            generate_all_value_for_letter(['H', 8, 'I'], max_rows_first_tab, 2016),
            generate_all_value_for_letter(['I', 9, 'J'], max_rows_first_tab, 2016)

        ]
    }

    r = requests.post(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate', headers=headers,
                      data=json.dumps(json_data))

    return r.status_code
