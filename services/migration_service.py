import os
import subprocess


class MigrationService:

    @staticmethod
    def run_alembic(db_url: str) -> str:
        env = os.environ.copy()
        env["DATABASE_URL"] = db_url
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=project_dir,
            env=env,
            capture_output=True,
            text=True,
        )

        output = result.stderr.strip()
        if result.returncode != 0:
            raise RuntimeError(
                f"Помилка alembic:\n{output}\n{result.stdout}"
            )
        return output
