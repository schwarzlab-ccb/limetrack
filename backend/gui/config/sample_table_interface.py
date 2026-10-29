# Lists of model fields for the column filters that are not filtering model
# sections but custom views of the table.
column_filters_no_group = {
    "scmultiome": ["sclab_pool",
                   "s3_bucket_status",
                   "scrna_r1", "scrna_r2",
                   "scatac_r1", "scatac_r2",
                   "scatac_i2"],

    "wgs": ["wgs_r1", "wgs_r2",
            "wgs_bam", "wgs_vcf", "wgs_ref"],

    "variantcalling": ["wgs_r1", "wgs_r2",
                       "wgs_bam", "wgs_ref"]
}

# display names for custom column filters
column_filters_verbose_names = {
    "scmultiome": "ScMultiome",
    "wgs": "WGS",
    "variantcalling": "Variant Calling"
}


# Custom group filters
# If groups want to have fields displayed in the table,
# that don't belong to this group these fields can be added here.
group_filter_extra_fields = {
    "omicspath": ["localisation"]
}

exclude_from_ui = ["id", "created"]
