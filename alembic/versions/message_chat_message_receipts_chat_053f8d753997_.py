"""message, chat, message_receipts, chat_participants

Revision ID: 053f8d753997
Revises: 02cf96158a57
Create Date: 2026-04-17 12:22:05.337518

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "053f8d753997"
down_revision: Union[str, Sequence[str], None] = "02cf96158a57"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "chat_participants",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("participant_fk", sa.Uuid(), nullable=False),
        sa.Column("chat_fk", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chat_fk"],
            ["chat.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["participant_fk"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "message_receipts",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_fk", sa.Uuid(), nullable=False),
        sa.Column("message_fk", sa.Uuid(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["message_fk"],
            ["message.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_fk"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("message_receipts")
    op.drop_table("chat_participants")
