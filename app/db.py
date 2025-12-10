from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
)

engine = create_engine("sqlite:///./sales_workflow.db", echo=True)
db = sessionmaker(engine, future=True)



def get_db_sync():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    metadata = MetaData()
    
def create_db_and_tables():
    import app.model as models  # noqa: F401

    Base.metadata.create_all(bind=engine)