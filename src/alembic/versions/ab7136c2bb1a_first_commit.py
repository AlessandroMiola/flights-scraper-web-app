"""first commit

Revision ID: ab7136c2bb1a
Revises:
Create Date: 2023-09-11 12:49:43.468279

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ab7136c2bb1a'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'flights',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('is_round_trip', sa.Boolean(), nullable=False),
        sa.Column('departure_location', sa.String(), nullable=False),
        sa.Column('arrival_location', sa.String(), nullable=False),
        sa.Column('departure_location_comeback', sa.String(), nullable=True),
        sa.Column('arrival_location_comeback', sa.String(), nullable=True),
        sa.Column('departure_date', sa.DateTime(), nullable=False),
        sa.Column('arrival_date', sa.DateTime(), nullable=False),
        sa.Column('departure_date_comeback', sa.DateTime(), nullable=True),
        sa.Column('arrival_date_comeback', sa.DateTime(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('luggage_type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'parameters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('is_round_trip', sa.Boolean(), nullable=False),
        sa.Column('departure_location', sa.String(), nullable=False),
        sa.Column('arrival_location', sa.String(), nullable=False),
        sa.Column('departure_location_comeback', sa.String(), nullable=True),
        sa.Column('arrival_location_comeback', sa.String(), nullable=True),
        sa.Column('departure_date', sa.Date(), nullable=False),
        sa.Column('departure_date_comeback', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parameters')
    op.drop_table('flights')
    # ### end Alembic commands ###
