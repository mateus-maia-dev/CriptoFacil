from environs import Env

env = Env()
env.read_env()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env("JWT_SECRET_KEY")


class ConfigDevelopment(Config):
    SQLALCHEMY_DATABASE_URI = env("URI_DEV_DB")


class ConfigProduction(Config):
    SQLALCHEMY_DATABASE_URI = env("URI_PROD_DB")
    ...


class ConfigTest(Config):
    SQLALCHEMY_DATABASE_URI = env("URI_TEST_DB")
    DEBUG = True
    TESTING = True


selector_config = {
    "development": ConfigDevelopment,
    "production": ConfigProduction,
    "test": ConfigTest,
}
