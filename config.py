from environs import Env

env = Env()
env.read_env()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigDevelopment(Config):
    SQLALCHEMY_DATABASE_URI = env("URI_DEV_DB")
    JWT_SECRET_KEY = env("JWT_SECRET_KEY")


class ConfigProduction(Config):
    ...


class ConfigTest(Config):
    ...


selector_config = {
    "development": ConfigDevelopment,
    "production": ConfigProduction,
    "test": ConfigTest,
}
