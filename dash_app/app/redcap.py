from dash_app.app import CONFIG
import pandas as pd
import httpx


def get_data(data: dict) -> pd.DataFrame:
    data.update({
        "token": CONFIG.api_token
    })
    response = httpx.post(CONFIG.api_url, data=data)
    result = pd.DataFrame()

    if response.is_success:
        result = pd.DataFrame.from_records(response.json())

    return result

def get_amount_patients() -> int:
    data = {
        "content": "record",
        "action": "export",
        "format": "json",
        "type": "flat",
        "csvDelimiter": "",
        "fields[0]": "pid",
        "rawOrLabel": "raw",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "false",
        "exportDataAccessGroups": "false",
        "returnFormat": "json"
    }
    df = get_data(data)
    n_patients = df.shape[0]

    return n_patients

def get_amount_samples() -> int:
    data = {
        "content": "record",
        "action": "export",
        "format": "json",
        "type": "flat",
        "csvDelimiter": "",
        "fields[0]": "tr_s3finding",
        "rawOrLabel": "raw",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "false",
        "exportDataAccessGroups": "false",
        "returnFormat": "json"
    }
    df = get_data(data)
    n_samples = df.shape[0]

    return n_samples

def get_amount_therapies() -> int:
    data = {
        "content": "record",
        "action": "export",
        "format": "json",
        "type": "flat",
        "csvDelimiter": "",
        "fields[0]": "pid",
        "forms[0]": "therapie",
        "rawOrLabel": "raw",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "false",
        "exportDataAccessGroups": "false",
        "returnFormat": "json"
    }
    df = get_data(data)
    n_therapies = df.shape[0]

    return n_therapies

def get_therapy_kinds() -> pd.DataFrame:
    data = {
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'fields[0]': 'th_therapie',
        'fields[1]': 'th_details',
        'rawOrLabel': 'label',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    df = get_data(data)
    df_grouped = df.groupby(by="th_details").count()
    df_grouped.reset_index(inplace=True)
    df_grouped.columns = ["therapy_kind", "n_therapies"]

    return df_grouped

def get_therapy_goals() -> pd.DataFrame:
    data = {
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'fields[0]': 'th_therapie',
        'fields[1]': 'th_details',
        'rawOrLabel': 'label',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    df = get_data(data)
    df_grouped = df.groupby(by="th_therapie").count()
    df_grouped.reset_index(inplace=True)
    df_grouped.columns = ["therapy_goal", "n_therapies"]

    return df_grouped
