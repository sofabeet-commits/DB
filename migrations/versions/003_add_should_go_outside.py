from alembic import op
import sqlalchemy as sa

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'wind_data',
        sa.Column('should_go_outside', sa.Boolean(),
                  server_default='1', nullable=False)
    )


def downgrade():
    op.drop_column('wind_data', 'should_go_outside')
