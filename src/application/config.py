from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix=False,
    environments=True,
    settings_files=["settings.yml"],
)

DB_URL_WITH_ALEMBIC = (
    f"postgresql+{settings.POSTGRES.dialect}://{settings.POSTGRES.login}:{settings.POSTGRES.password}@"
    f"{settings.POSTGRES.host}:{settings.POSTGRES.port}/{settings.POSTGRES.database}"
)
