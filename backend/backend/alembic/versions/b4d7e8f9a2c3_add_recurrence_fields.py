# [Task]: T110 [US11] | Add recurrence fields to tasks table
"""Add recurrence_pattern, recurrence_parent_id, due_date to tasks table.

Revision ID: b4d7e8f9a2c3
Revises: a5b6c7d8e9f0
Create Date: 2026-02-12

Changes:
- Add recurrence_pattern VARCHAR(10) nullable column
- Add recurrence_parent_id INTEGER nullable FK to tasks(id)
- Add due_date TIMESTAMP nullable column
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "b4d7e8f9a2c3"
down_revision: Union[str, None] = "a5b6c7d8e9f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("recurrence_pattern", sa.String(10), nullable=True))
    op.add_column("tasks", sa.Column("recurrence_parent_id", sa.Integer(), nullable=True))
    op.add_column("tasks", sa.Column("due_date", sa.DateTime(), nullable=True))
    op.create_foreign_key(
        "fk_tasks_recurrence_parent_id",
        "tasks",
        "tasks",
        ["recurrence_parent_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_tasks_recurrence_pattern", "tasks", ["recurrence_pattern"])


def downgrade() -> None:
    op.drop_index("ix_tasks_recurrence_pattern", table_name="tasks")
    op.drop_constraint("fk_tasks_recurrence_parent_id", "tasks", type_="foreignkey")
    op.drop_column("tasks", "due_date")
    op.drop_column("tasks", "recurrence_parent_id")
    op.drop_column("tasks", "recurrence_pattern")
