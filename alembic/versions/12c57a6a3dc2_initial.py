"""Initial

Revision ID: 12c57a6a3dc2
Revises: 
Create Date: 2020-09-09 15:13:24.888540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12c57a6a3dc2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cache_photo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_file', sa.String(), nullable=True),
    sa.Column('id_vk', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cache_photo_name_file'), 'cache_photo', ['name_file'], unique=True)
    op.create_table('notify',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_vk', sa.Integer(), nullable=True),
    sa.Column('is_group', sa.Boolean(), nullable=True),
    sa.Column('search_text', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notify_id_vk'), 'notify', ['id_vk'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_notify_id_vk'), table_name='notify')
    op.drop_table('notify')
    op.drop_index(op.f('ix_cache_photo_name_file'), table_name='cache_photo')
    op.drop_table('cache_photo')
