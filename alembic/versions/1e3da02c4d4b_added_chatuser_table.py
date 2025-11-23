"""Added ChatUser table

Revision ID: 1e3da02c4d4b
Revises: 
Create Date: 2025-11-23 16:35:09.718986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e3da02c4d4b'
down_revision: Union[str, Sequence[str], None] = "667562bbbf89"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
            "chat_users",
            sa.Column("chat_id", sa.Integer, sa.ForeignKey("chats.id"), primary_key=True),
            sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
            sa.Column("role", sa.String, nullable=False, server_default="member"),
            sa.Column("joined_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("chat_users")
