from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Table, Column, String, Boolean


class Person(Base):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    plus_hash: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    checked_in: Mapped[bool] = mapped_column(db.Boolean,nullable=False,default=False)