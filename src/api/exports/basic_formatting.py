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


# Formatting first table for receipt export
def basic_formatting_receipt(session: str, spreadsheet_id: str):
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
                        "endRowIndex": 8,
                        "endColumnIndex": 9
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
                        "endRowIndex": 8,
                        "endColumnIndex": 10
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
                        "endIndex": 9
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
                        "endRowIndex": 8,
                        "startColumnIndex": 1,
                        "endColumnIndex": 9
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
                            "endRowIndex": 1
                        }
                    }
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": 11,
                        "endRowIndex": 12
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
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": 12,
                        "endRowIndex": 13
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
                        "startRowIndex": 12,
                        "endRowIndex": 16,
                        "endColumnIndex": 9
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
                        "startRowIndex": 12,
                        "endRowIndex": 16,
                        "endColumnIndex": 10
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
                        "startIndex": 10,
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
                        "startRowIndex": 13,
                        "endRowIndex": 14,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 12,
                        "endRowIndex": 14,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 12,
                        "endRowIndex": 14,
                        "startColumnIndex": 9,
                        "endColumnIndex": 12
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
                        "startRowIndex": 12,
                        "endRowIndex": 14,
                        "startColumnIndex": 10,
                        "endColumnIndex": 17
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 17,
                        "endRowIndex": 18
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
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": 18,
                        "endRowIndex": 19
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
                        "startRowIndex": 18,
                        "endRowIndex": 22,
                        "endColumnIndex": 9
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
                        "startRowIndex": 18,
                        "endRowIndex": 22,
                        "endColumnIndex": 10
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 19,
                        "endRowIndex": 20,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 18,
                        "endRowIndex": 20,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 18,
                        "endRowIndex": 20,
                        "startColumnIndex": 9,
                        "endColumnIndex": 12
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
                        "startRowIndex": 18,
                        "endRowIndex": 20,
                        "startColumnIndex": 10,
                        "endColumnIndex": 17
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 23,
                        "endRowIndex": 24
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
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": 24,
                        "endRowIndex": 25
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
                        "startRowIndex": 24,
                        "endRowIndex": 28,
                        "endColumnIndex": 9
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
                        "startRowIndex": 24,
                        "endRowIndex": 28,
                        "endColumnIndex": 10
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 25,
                        "endRowIndex": 26,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 24,
                        "endRowIndex": 26,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 24,
                        "endRowIndex": 26,
                        "startColumnIndex": 9,
                        "endColumnIndex": 12
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
                        "startRowIndex": 24,
                        "endRowIndex": 26,
                        "startColumnIndex": 10,
                        "endColumnIndex": 17
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 29,
                        "endRowIndex": 30
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
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": 30,
                        "endRowIndex": 31
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
                        "startRowIndex": 30,
                        "endRowIndex": 34,
                        "endColumnIndex": 9
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
                        "startRowIndex": 30,
                        "endRowIndex": 34,
                        "endColumnIndex": 10
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 31,
                        "endRowIndex": 32,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 30,
                        "endRowIndex": 32,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 30,
                        "endRowIndex": 32,
                        "startColumnIndex": 9,
                        "endColumnIndex": 12
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
                        "startRowIndex": 30,
                        "endRowIndex": 32,
                        "startColumnIndex": 10,
                        "endColumnIndex": 17
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 35,
                        "endRowIndex": 36
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
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": 36,
                        "endRowIndex": 37
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
                        "startRowIndex": 36,
                        "endRowIndex": 40,
                        "endColumnIndex": 9
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
                        "startRowIndex": 36,
                        "endRowIndex": 40,
                        "endColumnIndex": 10
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 37,
                        "endRowIndex": 38,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 36,
                        "endRowIndex": 38,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 36,
                        "endRowIndex": 38,
                        "startColumnIndex": 9,
                        "endColumnIndex": 12
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
                        "startRowIndex": 36,
                        "endRowIndex": 38,
                        "startColumnIndex": 10,
                        "endColumnIndex": 17
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 41,
                        "endRowIndex": 42
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
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": 42,
                        "endRowIndex": 43
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
                        "startRowIndex": 42,
                        "endRowIndex": 46,
                        "endColumnIndex": 9
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
                        "startRowIndex": 42,
                        "endRowIndex": 46,
                        "endColumnIndex": 10
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 43,
                        "endRowIndex": 44,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 42,
                        "endRowIndex": 44,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 42,
                        "endRowIndex": 44,
                        "startColumnIndex": 9,
                        "endColumnIndex": 12
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
                        "startRowIndex": 42,
                        "endRowIndex": 44,
                        "startColumnIndex": 10,
                        "endColumnIndex": 17
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 47,
                        "endRowIndex": 48
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
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "startRowIndex": 48,
                        "endRowIndex": 49
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
                        "startRowIndex": 48,
                        "endRowIndex": 52,
                        "endColumnIndex": 9
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
                        "startRowIndex": 48,
                        "endRowIndex": 52,
                        "endColumnIndex": 10
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
                "repeatCell": {
                    "range": {
                        "startRowIndex": 49,
                        "endRowIndex": 50,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 48,
                        "endRowIndex": 50,
                        "startColumnIndex": 10,
                        "endColumnIndex": 16
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
                        "startRowIndex": 48,
                        "endRowIndex": 50,
                        "startColumnIndex": 9,
                        "endColumnIndex": 12
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
                        "startRowIndex": 48,
                        "endRowIndex": 50,
                        "startColumnIndex": 10,
                        "endColumnIndex": 17
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
            }
        ]
    }

    r = requests.post(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate', headers=headers,
                      data=json.dumps(json_data))

    return r.status_code
