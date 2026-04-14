from config.database import get_session, DB_URL, CSV_PATH
from repositories import WeatherRepository, WindRepository
from services import CsvService, WeatherService, MigrationService


class CLI:

    @staticmethod
    def _build_services(db_url=None):
        session, engine = get_session(db_url)
        weather_repo = WeatherRepository(session)
        wind_repo = WindRepository(session)
        weather_service = WeatherService(weather_repo, wind_repo)
        csv_service = CsvService(weather_repo)
        return session, weather_service, csv_service

    @staticmethod
    def cmd_migrate():
        print(f"База даних: {DB_URL}")
        output = MigrationService.run_alembic(DB_URL)
        print(output)
        print("Мiграцiї успiшно застосованi!")

    @staticmethod
    def cmd_load():
        session, weather_service, csv_service = CLI._build_services()
        try:
            count = csv_service.load_csv(CSV_PATH)
            print(f"Завантажено {count} записiв в weather_data")
        except FileNotFoundError as e:
            print(str(e))
        finally:
            session.close()

    @staticmethod
    def cmd_fill():
        session, weather_service, csv_service = CLI._build_services()
        try:
            updated, total = weather_service.fill_should_go_outside()
            print(f"Оновлено {updated} з {total} записiв у wind_data")
        except RuntimeError as e:
            print(str(e))
        finally:
            session.close()

    @staticmethod
    def cmd_info():
        session, weather_service, csv_service = CLI._build_services()
        try:
            stats = weather_service.get_statistics()

            print(f"weather_data: {stats['weather_count']} записiв")

            if stats["wind_count"] is not None:
                print(f"wind_data:    {stats['wind_count']} записiв")
                print(f"  безпечно виходити:   {stats['safe_count']}")
                print(f"  краще не виходити:   {stats['danger_count']}")
            else:
                print("wind_data: таблиця ще не створена")
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
        print("  python main.py fill     - заповнити should_go_outside")
        print("  python main.py info     - статистика бази")
