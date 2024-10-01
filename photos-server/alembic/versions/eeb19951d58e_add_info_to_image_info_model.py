"""Add info to image info model

Revision ID: eeb19951d58e
Revises: 55d2ee8631e2
Create Date: 2024-10-01 22:44:31.085346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eeb19951d58e'
down_revision: Union[str, None] = '55d2ee8631e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('relative_path', sa.String(), nullable=False))
    op.add_column('images', sa.Column('hash', sa.String(), nullable=False))
    op.add_column('images', sa.Column('exif', sa.JSON(), nullable=True))
    op.create_index(op.f('ix_images_filename'), 'images', ['filename'], unique=False)
    op.create_index(op.f('ix_images_id'), 'images', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_images_id'), table_name='images')
    op.drop_index(op.f('ix_images_filename'), table_name='images')
    op.drop_column('images', 'exif')
    op.drop_column('images', 'hash')
    op.drop_column('images', 'relative_path')
    # ### end Alembic commands ###