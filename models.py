from database import Base
from sqlalchemy import String, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    published: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )
