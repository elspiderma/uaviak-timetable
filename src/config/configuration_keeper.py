from config import Configuration


class ConfigurationNotSaved(Exception):
    pass


class ConfigurationKeeper:
    _configuration: Configuration = None

    @classmethod
    def save_configuration(cls, config: Configuration) -> None:
        cls._configuration = config

    @classmethod
    def get_configuration(cls) -> Configuration:
        if cls._configuration is None:
            raise ConfigurationNotSaved('first you need execute save_configuration')

        return cls._configuration
