import pandas as pd

redcap_column_mapping = {
        "pid": "Patient Identifier",
        "age_at_diagnosis": "Age at Diagnosis",
        "sex": "Sex",
        "icd10": "ICD10",
        "documentation_complete": "Documentation complete",
        "th_details": "Therapy kind", 
        "th_start_d": "Therapy start",
        "th_end_d": "Therapy end",
        "th_trt_c": "Therapy detail",
        "mh_diagnosis_d": "First diagnosis date",
        "th_num": "Therapy number",
        "th_therapie": "Therapy goal",
        "th_resp": "Therapy response",
        "th_resp_txt": "Other therapy response",
        "th_pd_start_d": "Date of progression",
        "th_trt_end_reas": "End of therapy reason",
        "th_dth_d": "Death date",
        "therapie_complete": "Therapy complete",
        "tr_s3finding": "SATURN3 Sample Code",
        "tr_visit_d": "Tissue sampling date",
        "tr_orig": "Type of intervention",
        "tr_orig_txt": "Other type of intervention",
        "tr_histology_c": "Histology",
        "tr_tzg": "Tumor cell content",
        "tr_tissue_oth": "Other relevant tissue structures",
        "tumorprobe_complete": "Sample complete"
        }

def map_columns(df: pd.DataFrame):

    return [
        redcap_column_mapping.get(column, column)
        for column in df.columns
    ]

def get_simple_ag_grid_column_defs(df: pd.DataFrame):
    return [ 
            {"field": column,
             "headerName": redcap_column_mapping.get(column)}
             for column in df.columns
    ]


def get_clinical_patients_ag_grid_column_defs(df: pd.DataFrame):
    return [ 
            {
            "field": column, 
            "headerName": redcap_column_mapping.get(column),
            "filter": "agNumberColumnFilter", 
            "filterParams": {
                "buttons": ["reset", "apply"],
            },
        }
        if column == "age_at_diagnosis"
        else {
            "field": column,
            "headerName": redcap_column_mapping.get(column),
            "filterParams": {
                "buttons": ["reset", "apply"],
            },
        }
        for column in df.columns
    ]