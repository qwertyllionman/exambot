from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:1@localhost:5432/postgres")
Session = sessionmaker(engine)
Base = declarative_base()


class Orders(Base):
    __tablename__ = "orders"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    category : Mapped[str]
    author : Mapped[str]
    price : Mapped[int]

Base.metadata.create_all(bind=engine)

