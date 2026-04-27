from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from business import ImportService
from data_access import SqlAlchemyDataAccess
from interfaces import IImportService


def build_import_service(db_url: str) -> IImportService:
    engine = create_engine(db_url, future=True)
    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    data_access = SqlAlchemyDataAccess(engine, session_factory)
    return ImportService(data_access)
