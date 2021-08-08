"""Server configuration."""

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="",
    settings_files=["settings.toml", ".secrets.toml"],
)
