import pandas as pd

redcap_column_mapping = {
        "pid": "Patient Identifier",
        "age_at_diagnosis": "Age at Diagnosis",
        "sex": "Sex",
        "icd10": "ICD10",
        "documentation_complete": "Documentation Complete",
        "th_details": "Therapy Type", 
        "th_start_d": "Therapy Start",
        "th_end_d": "Therapy End",
        "th_trt_c": "Therapy Detail",
        "mh_diagnosis_d": "Date Initial Diagnosis",
        "th_num": "Therapy Line",
        "th_therapie": "Therapy Goal",
        "th_resp": "Therapy Response",
        "th_resp_txt": "Other Therapy Response",
        "th_pd_start_d": "Date of Progression",
        "th_trt_end_reas": "End of Therapy Reason",
        "th_dth_d": "Date of Death",
        "therapie_complete": "Therapy Complete",
        "tr_s3finding": "SATURN3 Sample Code",
        "tr_visit_d": "Tissue Sampling Date",
        "tr_orig": "Type of Intervention",
        "tr_orig_txt": "Other Type of Intervention",
        "tr_histology_c": "Histology",
        "tr_tzg": "Tumor Cell Content",
        "tr_tissue_oth": "Other Relevant Tissue Structures",
        "tumorprobe_complete": "Sample Complete"
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