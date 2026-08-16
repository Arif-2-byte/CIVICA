from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Session(Base):
    __tablename__ = "sessions"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # User Relationship
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Security
    token_hash = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    # Device Information
    device_name = Column(String(255), nullable=True)
    ip_address = Column(String(100), nullable=True)
    user_agent = Column(String(500), nullable=True)

    # Session Status
    is_revoked = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Expiration
    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Audit Fields
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    last_used_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship
    user = relationship(
        "User",
        back_populates="sessions",
    )