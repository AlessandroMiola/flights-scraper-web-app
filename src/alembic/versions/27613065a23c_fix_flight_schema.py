"""Fix flight schema

Revision ID: 27613065a23c
Revises: 7372020f0ccb
Create Date: 2023-10-08 22:18:22.595152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27613065a23c'
down_revision: Union[str, None] = '7372020f0ccb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flights', sa.Column('airline', sa.String(), nullable=False))
    op.add_column(
        'flights',
        sa.Column('airline_comeback', sa.String(), nullable=True)
    )
    op.add_column(
        'flights',
        sa.Column('flight_length', sa.String(), nullable=False)
    )
    op.add_column(
        'flights',
        sa.Column('flight_length_comeback', sa.String(), nullable=True)
    )
    op.add_column(
        'flights',
        sa.Column('trip_type', sa.String(), nullable=False)
    )
    op.add_column(
        'flights',
        sa.Column('trip_type_comeback', sa.String(), nullable=True)
    )
    op.add_column(
        'flights',
        sa.Column('currency', sa.String(), nullable=False)
    )
    op.add_column(
        'flights',
        sa.Column('luggage_type_comeback', sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flights', 'luggage_type_comeback')
    op.drop_column('flights', 'currency')
    op.drop_column('flights', 'trip_type_comeback')
    op.drop_column('flights', 'trip_type')
    op.drop_column('flights', 'flight_length_comeback')
    op.drop_column('flights', 'flight_length')
    op.drop_column('flights', 'airline_comeback')
    op.drop_column('flights', 'airline')
    # ### end Alembic commands ###