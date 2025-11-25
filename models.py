from database import Base
from sqlalchemy import String, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    published: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
