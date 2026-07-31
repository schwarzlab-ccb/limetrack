from sqlalchemy import Select, create_engine, select, func, case, INT
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import datetime
from dash_app_2.app import CONFIG
import pandas as pd

Base = declarative_base()


class Sample(Base):
    __tablename__ = "gui_histopathologicalsample"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_identifier: Mapped[str]
    saturn3_sample_code: Mapped[str]
    tissue_type: Mapped[str]
    recruiting_site: Mapped[str]
    sex: Mapped[str]
    spl_status: Mapped[str]
    sclab_status: Mapped[str]
    sampling_date: Mapped[datetime]
    localisation: Mapped[str]
    type_of_intervention: Mapped[str]
    tumor_cell_content: Mapped[int]


def get_data(stmt: Select) -> pd.DataFrame:
    engine = create_engine(CONFIG.connection_string)

    with engine.connect() as connection:
        cursor = connection.execute(stmt)
        fields = list(cursor.keys())
        results = cursor.all()

    df = pd.DataFrame(results, columns=fields)

    return df

def get_patient_timepoint_data() -> pd.DataFrame:
    stmt = select(
        Sample.id,
        Sample.patient_identifier,
        Sample.recruiting_site,
        Sample.sex,
        Sample.spl_status,
        Sample.sclab_status,
        Sample.sampling_date,
        Sample.localisation,
        Sample.type_of_intervention,
        Sample.tissue_type,
        Sample.saturn3_sample_code,
        case(
            (Sample.tumor_cell_content.is_(None), -1),
            else_=Sample.tumor_cell_content
        ).label("tumor_cell_content"),
        case(
            (Sample.saturn3_sample_code.regexp_match(r"^S3C"), "CRC"),
            (Sample.saturn3_sample_code.regexp_match(r"^S3M"), "BC"),
            (Sample.saturn3_sample_code.regexp_match(r"^S3P"), "PDAC"),
            else_="Other"
        ).label("entity"),
        Sample.tissue_type,
        func.split_part(Sample.saturn3_sample_code, "-", 3).label("timepoint")
    )

    df = get_data(stmt)
    df["timepoint"] = df.timepoint.apply(int)
    df.fillna("NA", inplace=True)

    return df