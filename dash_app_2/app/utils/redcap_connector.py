from dash_app_2.app import CONFIG
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

def get_redcap_base_data() -> pd.DataFrame:
    data = {
        "content": "record",
        "action": "export",
        "format": "json",
        "type": "flat",
        "csvDelimiter": "",
        "fields[0]": "pid",
        "fields[1]": "mh_age",
        "fields[2]": "dm_sex",
        "fields[3]": "mh_icd10_c",
        "fields[5]": "ende_saturn3_complete",
        "rawOrLabel": "label",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "false",
        "exportDataAccessGroups": "false",
        "returnFormat": "json"
    }
    df = get_data(data)
    df["mh_age"] = df.mh_age.apply(int)
    sex_mappings = {
        "Männlich": "male",
        "Weiblich": "female",
        "Divers": "divers",
        "Nicht festgelegt / Unbestimmt": "unassigned",
        "Unbekannt": "unknown",
    }
    column_mapping = {
        "mh_age": "age_at_diagnosis",
        "dm_sex": "sex",
        "mh_icd10_c": "icd10",
        "ende_saturn3_complete": "documentation_complete"
    }
    df["dm_sex"] = df.dm_sex.apply(lambda v: sex_mappings.get(v, "NA"))
    df.columns = [
        column_mapping.get(column, column)
        for column in df.columns
    ]
    df_filtered = df.loc[
        :, 
        ["pid", "age_at_diagnosis", "sex", "icd10", "documentation_complete"]
    ]
    
    return df_filtered

def get_therapies_start_to_end() -> pd.DataFrame:
    data = {
        "content": "record",
        "action": "export",
        "format": "json",
        "type": "flat",
        "csvDelimiter": "",
        "fields[0]": "pid",
        'fields[1]': 'th_details',
        "fields[2]": "th_start_d",
        "fields[3]": "th_end_d",
        "rawOrLabel": "label",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "false",
        "exportDataAccessGroups": "false",
        "returnFormat": "json"
    }
    df = get_data(data)
    df.reset_index(inplace=True)
    
    df = df.loc[:, ["pid", "th_details", "th_start_d", "th_end_d"]]
    df.columns = ["patient_identifier", "therapy_kind", "therapy_start", "therapy_end"]

    return df

def get_therapy_data() -> pd.DataFrame:
    data = {
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'fields[0]': 'pid',
        'forms[0]': 'therapie',
        'rawOrLabel': 'label',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }

    df = get_data(data)
    df = df.loc[
        df.redcap_repeat_instrument == "Therapie",
        [
            "pid",
            "th_num",
            "th_therapie",
            "th_details",
            "th_start_d",
            "th_end_d",
            "th_trt_c",
            "th_resp",
            "th_resp_txt",
            "th_pd_start_d",
            "th_trt_end_reas",
            "th_dth_d",
            "therapie_complete"
        ]
    ]

    return df

def get_samples() -> pd.DataFrame:
    data = {
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'fields[0]': 'pid',
        'forms[0]': 'tumorprobe',
        'rawOrLabel': 'label',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }

    df = get_data(data)
    df = df.loc[
        df.redcap_repeat_instrument == "Tumorprobe",
        [
            "pid",
            "tr_s3finding",
            "tr_visit_d",
            "tr_orig",
            "tr_orig_txt",
            "tr_histology_c",
            "tr_tzg",
            "tr_tissue_oth",
            "tumorprobe_complete"
        ]
    ]

    return df