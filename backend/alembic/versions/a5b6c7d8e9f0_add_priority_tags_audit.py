# [Task]: T017, T018, T019 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""Add priority, tags, and audit_log tables for Phase 5.

Revision ID: a5b6c7d8e9f0
Revises: f3c8d9e0a1b2
Create Date: 2026-01-30

Changes:
- Add priority column to tasks table
- Create tags table
- Create task_tags junction table
- Create audit_logs table
- Seed default tags
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5b6c7d8e9f0'
down_revision: Union[str, None] = 'f3c8d9e0a1b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add priority column to tasks table
    op.add_column(
        'tasks',
        sa.Column('priority', sa.String(2), nullable=False, server_default='P2')
    )
    op.create_index('ix_tasks_priority', 'tasks', ['priority'])

    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('color', sa.String(7), nullable=False, server_default='#808080'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_tags_name', 'tags', ['name'])

    # Create task_tags junction table
    op.create_table(
        'task_tags',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('task_id', 'tag_id')
    )

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.String(50), nullable=False),
        sa.Column('event_type', sa.String(20), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=True),
        sa.Column('data', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id')
    )
    op.create_index('ix_audit_logs_event_id', 'audit_logs', ['event_id'])
    op.create_index('ix_audit_logs_event_type', 'audit_logs', ['event_type'])
    op.create_index('ix_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('ix_audit_logs_task_id', 'audit_logs', ['task_id'])
    op.create_index('ix_audit_logs_timestamp', 'audit_logs', ['timestamp'])

    # Seed default tags (T019)
    op.execute("""
        INSERT INTO tags (name, color) VALUES
        ('Work', '#3B82F6'),
        ('Personal', '#10B981'),
        ('Shopping', '#F59E0B'),
        ('Health', '#EF4444'),
        ('Finance', '#8B5CF6')
    """)


def downgrade() -> None:
    # Drop audit_logs table
    op.drop_index('ix_audit_logs_timestamp', table_name='audit_logs')
    op.drop_index('ix_audit_logs_task_id', table_name='audit_logs')
    op.drop_index('ix_audit_logs_user_id', table_name='audit_logs')
    op.drop_index('ix_audit_logs_event_type', table_name='audit_logs')
    op.drop_index('ix_audit_logs_event_id', table_name='audit_logs')
    op.drop_table('audit_logs')

    # Drop task_tags junction table
    op.drop_table('task_tags')

    # Drop tags table
    op.drop_index('ix_tags_name', table_name='tags')
    op.drop_table('tags')

    # Remove priority column from tasks
    op.drop_index('ix_tasks_priority', table_name='tasks')
    op.drop_column('tasks', 'priority')
