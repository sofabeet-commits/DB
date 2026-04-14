from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'weather_data',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('country', sa.String(255), nullable=False),
        sa.Column('location_name', sa.String(255)),
        sa.Column('last_updated', sa.DateTime()),
        sa.Column('sunrise', sa.Time()),
        sa.Column('sunset', sa.Time()),
        sa.Column('latitude', sa.Float()),
        sa.Column('longitude', sa.Float()),
        sa.Column('timezone', sa.String(100)),
        sa.Column('temperature_celsius', sa.Float()),
        sa.Column('condition_text', sa.String(255)),
        sa.Column('humidity', sa.Integer()),
        sa.Column('pressure_mb', sa.Float()),
        sa.Column('visibility_km', sa.Float()),
        sa.Column('wind_degree', sa.Integer()),
        sa.Column('wind_kph', sa.Float()),
        sa.Column('wind_direction', sa.String(10)),
        sa.Column('wind_mph', sa.Float()),
        sa.Column('gust_mph', sa.Float()),
        sa.Column('gust_kph', sa.Float()),
    )


def downgrade():
    op.drop_table('weather_data')
