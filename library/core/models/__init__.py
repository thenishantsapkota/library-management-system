from sqlmodel import SQLModel, create_engine

from library.core.models.database import Books

engine = create_engine("sqlite:///database.db", echo=True)


def migrate():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    migrate()

__all__ = ["Books"]
