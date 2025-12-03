from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Update this with your real Postgres connection string
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/lawtech_claims"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    from fastapi import Depends
    from sqlalchemy.orm import Session

    def _get_db():
        db: Session = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    return Depends(_get_db)
