from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'wind_data',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('weather_id', sa.Integer(),
                  sa.ForeignKey('weather_data.id'),
                  nullable=False, unique=True),
        sa.Column('wind_degree', sa.Integer()),
        sa.Column('wind_kph', sa.Float()),
        sa.Column('wind_mph', sa.Float()),
        sa.Column('wind_direction', sa.String(10)),
        sa.Column('gust_mph', sa.Float()),
        sa.Column('gust_kph', sa.Float()),
    )

    op.execute(
        "INSERT INTO wind_data "
        "(weather_id, wind_degree, wind_kph, wind_mph, wind_direction, gust_mph, gust_kph) "
        "SELECT id, wind_degree, wind_kph, wind_mph, wind_direction, gust_mph, gust_kph "
        "FROM weather_data"
    )


def downgrade():
    op.execute(
        "UPDATE weather_data SET "
        "wind_degree = (SELECT wd.wind_degree FROM wind_data wd WHERE wd.weather_id = weather_data.id), "
        "wind_kph = (SELECT wd.wind_kph FROM wind_data wd WHERE wd.weather_id = weather_data.id), "
        "wind_mph = (SELECT wd.wind_mph FROM wind_data wd WHERE wd.weather_id = weather_data.id), "
        "wind_direction = (SELECT wd.wind_direction FROM wind_data wd WHERE wd.weather_id = weather_data.id), "
        "gust_mph = (SELECT wd.gust_mph FROM wind_data wd WHERE wd.weather_id = weather_data.id), "
        "gust_kph = (SELECT wd.gust_kph FROM wind_data wd WHERE wd.weather_id = weather_data.id)"
    )
    op.drop_table('wind_data')
