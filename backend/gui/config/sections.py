# dictionary for splitting the model into sections
# keys: sections
# values: list of fields that belong to this section
#         make sure the values are equal to the models.py variable names
# the sorting here determines the sorting in the sample tracking table

section_dict = {
    "recruiter": [
        "recruiting_site",
        "patient_identifier",
        "sex",
        "died",
        "saturn3_sample_code",
        "note",
        "sampling_date",
        "tissue_type",
        "type_of_intervention",
        "localisation",
        "corresponding_organoid",
        "grading"],

    "tum": [
        "tissue_quality",
        "tumor_cell_content",
        "percent_avital_cells",
        "comment_tumor_cell_content"],

    "spl": [
        "spl_received",
        "spl_status",
        "spl_sequencing_type"],

    "scopenlab": [
        "sclab_received",
        "sclab_extraction_date",
        "sclab_nuclei_yield",
        "sclab_nuclei_size",
        "sclab_status",
        "sclab_sequencing_type",
        "sclab_sorting",
        "sclab_pool",
        "rna_isle_id",
        "atac_isle_id",
        "sclab_comment"],

    "spatial": [
        "spatial_method",
        "spatial_status",
        "xenium_run_date",
        "xenium_slide_id",
        "xenium_run_id",
        "xenium_panel_id",
        "merscope_run_date",
        "merscope_run_id",
        "merscope_panel_id",
        "dv_200",
        "spatial_comment"],

    "liquidbiopsy": [
        "lb_analyte_type",
        "lb_panel_r1",
        "lb_panel_r2",
        "lb_sequencing_status",
        "lb_received",
        "lb_sample_volume",
        "lb_date_of_isolation",
        "lb_total_isolated_cfdna",
        "lb_status"],

    "omicspath": [
        "request_execution_of",
        "cell_ranger_arc_run",
        "sc_analysis_status",
        "s3_bucket_status",
        "scrna_r1",
        "scrna_r2",
        "scatac_r1",
        "scatac_r2",
        "scatac_i2",
        "wgs_r1",
        "wgs_r2",
        "wgs_bam",
        "wgs_vcf",
        "wgs_ref"],
}

# which data is patient specific and independent of sample data
patient_data_fields = ["recruting_site", "patient_identifier", "sex", "died"]

# display names of sections in UI
verbose_section_names = {
    "recruiter": "Recruiter",
    "tum": "TUM",
    "spl": "SPL",
    "scopenlab": "ScLab",
    "spatial": "Spatial",
    "liquidbiopsy": "LB",
    "omicspath": "ODCF"
    }

# hide sections' fields instead of only disabling
# them in the sample tracking form for unauthorized users
hidden_sections = ["omicspath"]
