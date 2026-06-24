from sqlalchemy import Select, create_engine, select, func, distinct, case
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from dash_app.app import CONFIG
import pandas as pd

Base = declarative_base()


class Sample(Base):
    __tablename__ = "gui_histopathologicalsample"

    id: Mapped[int] = mapped_column(primary_key=True)
    saturn3_sample_code: Mapped[str]
    patient_identifier: Mapped[str]
    recruiting_site: Mapped[str]
    localisation: Mapped[str]


def get_data(stmt: Select) -> pd.DataFrame:
    engine = create_engine(CONFIG.connection_string)

    with engine.connect() as connection:
        cursor = connection.execute(stmt)
        fields = list(cursor.keys())
        results = cursor.all()

    df = pd.DataFrame(results, columns=fields)

    return df

def get_amount_patients() -> int:
    stmt = select(
        func.count(
            distinct(Sample.patient_identifier)
        ).label("n_patients")
    )

    result = get_data(stmt).n_patients.apply(int)[0]
    
    return result

def get_amount_samples() -> int:
    stmt = select(
        func.count(
            Sample.id
        ).label("n_samples")
    )

    result = get_data(stmt).n_samples.apply(int)[0]

    return result

def get_amount_recruiting_sites() -> int:
    stmt = select(
        func.count(
            distinct(
                Sample.recruiting_site
            )
        ).label("n_recruiting_sites")
    )
    
    result = get_data(stmt).n_recruiting_sites.apply(int)[0]

    return result

def get_sample_localisations() -> pd.DataFrame:
    stmt = select(
        Sample.localisation,
        func.count(Sample.localisation).label("n_samples")
    ).group_by(
        Sample.localisation
    )
    df = get_data(stmt)

    return df

def get_sample_entites() -> pd.DataFrame:
    stmt_subq = select(
        case(
            (Sample.saturn3_sample_code.regexp_match(r"^S3C"), "CRC"),
            (Sample.saturn3_sample_code.regexp_match(r"^S3M"), "BC"),
            (Sample.saturn3_sample_code.regexp_match(r"^S3P"), "PDAC"),
            else_="Other"
        ).label("entity")
    ).subquery()

    stmt = select(
        stmt_subq.c.entity,
        func.count(stmt_subq.c.entity).label("n_samples")
    ).group_by(
        stmt_subq.c.entity
    )

    df = get_data(stmt)

    return df