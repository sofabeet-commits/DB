from config.database import get_session, DB_URL, CSV_PATH
from repositories import WeatherRepository
from services import CsvService, MigrationService


class CLI:

    @staticmethod
    def _build_services(db_url=None):
        session, engine = get_session(db_url)
        weather_repo = WeatherRepository(session)
        csv_service = CsvService(weather_repo)
        return session, csv_service

    @staticmethod
    def cmd_migrate():
        print(f"База даних: {DB_URL}")
        output = MigrationService.run_alembic(DB_URL)
        print(output)
        print("Мiграцiї успiшно застосованi!")

    @staticmethod
    def cmd_load():
        session, csv_service = CLI._build_services()
        try:
            count = csv_service.load_csv(CSV_PATH)
            print(f"Завантажено {count} записiв в weather_data")
        except FileNotFoundError as e:
            print(str(e))
        finally:
            session.close()

    @staticmethod
    def cmd_info():
        session, csv_service = CLI._build_services()
        try:
            weather_repo = WeatherRepository(session)
            print(f"weather_data: {weather_repo.count()} записiв")
        finally:
            session.close()

    @staticmethod
    def print_usage():
        print("Мiграцiя погодної бази даних")
        print("Категорiя: 1 (вiтер)")
        print()
        print("Використання:")
        print("  python main.py migrate  - накотити мiграцiї")
        print("  python main.py load     - завантажити CSV")
        print("  python main.py info     - статистика бази")
