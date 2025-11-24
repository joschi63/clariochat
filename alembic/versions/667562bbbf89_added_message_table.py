"""Added Message table

Revision ID: 667562bbbf89
Revises: c8d808448317
Create Date: 2025-11-23 16:56:12.028047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '667562bbbf89'
down_revision: Union[str, Sequence[str], None] = "c8d808448317"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("content", sa.String, nullable=False),
        sa.Column("changed", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("read", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("deleted", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("sender_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("chat_id", sa.Integer, sa.ForeignKey("chats.id"), nullable=False),
        sa.Column("sended_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()"), onupdate=sa.text("now()")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("messages")
