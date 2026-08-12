import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime

def patient_journey_samples_and_therapies(
    patient: str,
    selected_y_axis: str,
    df_redcap: pd.DataFrame,
    df_patient: pd.DataFrame,
) -> go.Figure:
    df_patient_filtered = df_patient[
        df_patient["patient_identifier"] == patient
    ].sort_values("sampling_date")

    death_dates = df_patient_filtered[(df_patient_filtered["died"] != "NA")]["died"]
    if len(death_dates) > 0:
        death_date = death_dates.iloc[0]
    else:
        death_date = None
    

    df_patient_therapies = df_redcap[
        (df_redcap["patient_identifier"] == patient) & 
        (df_redcap["therapy_kind"] != "Operation") & 
        (df_redcap["therapy_start"] != "") & 
        (df_redcap["therapy_start"] != df_redcap["therapy_end"])
    ].sort_values("therapy_start")


    one_day_therapies_df = df_redcap[
        (df_redcap["patient_identifier"] == patient) & 
        (df_redcap["therapy_kind"] != "Operation") &
        (df_redcap["therapy_start"] == df_redcap["therapy_end"]) &
        (df_redcap["therapy_start"] != "")
    ].sort_values("therapy_start")


    operation_df = df_redcap[
        (df_redcap["patient_identifier"] == patient) & 
        (df_redcap["therapy_kind"] == "Operation")
    ].sort_values("therapy_start")
    
    samples = go.Scatter(
        x=df_patient_filtered["sampling_date"],
        y=df_patient_filtered[selected_y_axis],
        mode="markers",
        marker=dict(size=12),
        name="Samples"
    )
    
    operations = go.Scatter(
            x=operation_df["therapy_start"],
            y=[f"Surgery {i}" for i in range(1, len(operation_df) + 1)],
            mode="markers",
            marker=dict(symbol="x", size=14),
            name="Surgery")

    one_day_therapies = go.Scatter(
            x=one_day_therapies_df["therapy_start"],
            y=[f"One day therapy {i}" for i in range(1, len(one_day_therapies_df) + 1)],
            mode="markers",
            marker=dict(symbol="hexagon", size=14),
            name="One day therapy")

    therapies_timeline = px.timeline(
        df_patient_therapies,
        x_start="therapy_start",
        x_end="therapy_end",
        color="therapy_kind",
        color_discrete_map={"Radiotherapie": "#2E8B57", "Chemotherapie": "#DC143C"},
        hover_data={"therapy_kind": False, "therapy_start": True, "therapy_end": True, "therapy_detail": True},
        y=[f"Therapy {i}" for i in range(1, len(df_patient_therapies) + 1) ],
        opacity=0.7,
    )

    data = [samples, operations, one_day_therapies, *[trace for trace in therapies_timeline.data]]

    layout = go.Layout(
        legend=dict(
            traceorder="reversed"
        ),
        title=dict(
            text="Patient History")
    )

    fig = go.Figure(data=data, layout=layout)

    if death_date:
        fig.add_vline(x=death_date, line_dash="dash", annotation_text=f"Date of death: {death_date}")

    fig.update_xaxes(
        # tickformat="%d.%m.%Y",
        hoverformat="%Y-%m-%d")

    return fig


def patient_samples_tumor_cell_content(patient: str, df_patient: pd.DataFrame) -> go.Figure:
    verbose_name_mapping = {
        "id": "ID",
        "recruiting_site": "Recruiting Site",
        "patient_identifier": "Patient Identifier",
        "sex": "Sex",
        "died": "Died",
        "saturn3_sample_code": "SATURN3 Sample Code",
        "note": "Note",
        "sampling_date": "Sampling Date",
        "tissue_type": "Tissue Type",
        "type_of_intervention": "Type of Intervention",
        "localisation": "Localisation",
        "corresponding_organoid": "Corresponding Organoid",
        "grading": "Grading",
        "tissue_quality": "Tissue Quality",
        "tumor_cell_content": "Tumor Cell Content [%]",
        "percent_avital_cells": "Avital Cells [%]",
        "comment_tumor_cell_content": "Comment Tumor Cell Content",
        "spl_received": "SPL Date Received",
        "spl_status": "SPL Status",
        "spl_sequencing_type": "SPL Analysis Type",
        "sclab_received": "ScLab Date Received",
        "sclab_extraction_date": "ScLab Extraction Date",
        "sclab_nuclei_yield": "ScLab Nuclei Yield",
        "sclab_nuclei_size": "ScLab Particles Above 5 µm [%]",
        "sclab_status": "ScLab Status",
        "sclab_sequencing_type": "ScLab Sequencing Type",
        "sclab_sorting": "ScLab Sorting",
        "sclab_pool": "ScLab Pool",
        "rna_isle_id": "RNA ILSE ID",
        "atac_isle_id": "ATAC ILSE ID",
        "sclab_comment": "ScLab Comment",
        "spatial_method": "Spatial Method",
        "spatial_status": "Spatial Status",
        "xenium_run_date": "Xenium Run Date",
        "xenium_slide_id": "Xenium Slide ID",
        "xenium_run_id": "Xenium Run ID",
        "xenium_panel_id": "Xenium Panel ID",
        "merscope_run_date": "Merscope Run Date",
        "merscope_run_id": "Merscope Run ID",
        "merscope_panel_id": "Merscope Panel ID",
        "dv_200": "DV200",
        "spatial_comment": "Spatial Comment",
        "lb_analyte_type": "LB Analyte Type",
        "lb_panel_r1": "LB Panel R1",
        "lb_panel_r2": "LB Panel R2",
        "lb_sequencing_status": "LB Sequencing Status",
        "lb_received": "LB Date Received",
        "lb_sample_volume": "LB Sample Volume [ml]",
        "lb_date_of_isolation": "LB Date of Isolation",
        "lb_total_isolated_cfdna": "LB Total Isolated cfDNA [ng]",
        "lb_status": "LB Status",
        "request_execution_of": "Request Execution of",
        "cell_ranger_arc_run": "Cellranger-arc Run",
        "sc_analysis_status": "ScAnalysis Status",
        "s3_bucket_status": "S3 Bucket Status",
        "scrna_r1": "ScRNA R1",
        "scrna_r2": "ScRNA R2",
        "scatac_r1": "ScATAC R1",
        "scatac_r2": "ScATAC R2",
        "scatac_i2": "ScATAC I2",
        "wgs_r1": "WGS R1",
        "wgs_r2": "WGS R2",
        "wgs_bam": "WGS bam",
        "wgs_vcf": "WGS vcf",
        "wgs_ref": "WGS Reference",
    }

    patient_df = df_patient[
        df_patient.patient_identifier == patient
    ].sort_values("sampling_date")

    fig = px.bar(patient_df, 
                 x="saturn3_sample_code", y="tumor_cell_content",
                 title="Samples",
                 labels=verbose_name_mapping)
    
    fig.update_yaxes(range=[0, 100], minallowed=0, maxallowed=100)

    return fig
