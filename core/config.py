SECRET_KEY: str = 'secret_key!'

SQLALCHEMY_DATABASE_URI: str = 'postgresql://postgres:postgres@localhost/bitly_alter'
SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

LONG_URL_MAX_LENGTH: int = 160
SHORT_URL_LENGTH: int = 8

REDIS_HOST: str = 'localhost'
REDIS_PORT: int = 6379
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
